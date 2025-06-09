from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import cv2
import requests
from PIL import Image
import io
import base64
import os
from pathlib import Path
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import pickle

app = FastAPI(
    title="Face Recognition Service",
    description="Provides state-of-the-art face recognition capabilities using MTCNN and FaceNet.",
    version="1.0.0"
)

# CORS Middleware Configuration
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8002",
    "http://127.0.0.1:8002",
    "http://localhost:8003",
    "http://127.0.0.1:8003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DetectRequest(BaseModel):
    known_image_url: str
    frame_data: str # Base64 encoded image frame

class DetectionResult(BaseModel):
    face_found_in_frame: bool = False
    person_detected: bool = False
    bounding_box: list = None # [x, y, width, height]
    confidence_score: float = None
    message: str = None

# Initialize models directory
models_dir = os.path.join(os.path.dirname(__file__), "models")
Path(models_dir).mkdir(parents=True, exist_ok=True)

# Set device
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# --- START: Added Confirmation Log ---
if torch.cuda.is_available():
    print("✅ Success! PyTorch is using CUDA.")
    print(f"   - GPU: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️  Notice: PyTorch is using the CPU.")
    print("   - CUDA is either not available or not installed correctly.")
    print("   - For GPU acceleration, ensure NVIDIA drivers are installed and a CUDA-enabled PyTorch version is used.")
# --- END: Added Confirmation Log ---

# Initialize MTCNN for face detection
print("Loading MTCNN face detector...")
mtcnn = MTCNN(
    image_size=160, 
    margin=0, 
    min_face_size=20,
    thresholds=[0.6, 0.7, 0.7],  # MTCNN thresholds
    factor=0.709, 
    post_process=True,
    device=device
)

# Initialize FaceNet model for face recognition
print("Loading FaceNet model...")
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Cache for known face embeddings
face_embedding_cache = {}

SIMILARITY_THRESHOLD = 0.6  # Threshold for considering a match

def get_face_embedding(face_img):
    """
    Extract face embedding using FaceNet model
    """
    # Ensure face_img is a PyTorch tensor
    if not isinstance(face_img, torch.Tensor):
        # This case is likely for the initial processing of the known_image if it wasn't a tensor
        # Assumes face_img is a PIL Image or HWC numpy array
        # For safety, let's assume it needs conversion to CHW tensor
        # However, mtcnn(known_image) should already return a CHW tensor.
        # This path might not be hit if mtcnn output is consistent.
        temp_img = np.array(face_img) # Convert PIL to numpy if necessary
        if len(temp_img.shape) == 3 and temp_img.shape[2] == 3: # HWC
            face_img = torch.tensor(temp_img).permute(2, 0, 1).float()
        elif len(temp_img.shape) == 2: # HW (grayscale) - needs expansion
             face_img = torch.tensor(temp_img).unsqueeze(0).float() # Add channel dim: CHW
        else:
            # If it's already a tensor but somehow got here, or unexpected shape
            raise ValueError(f"Unexpected input type or shape to get_face_embedding: {type(face_img)}, shape {face_img.shape if hasattr(face_img, 'shape') else 'N/A'}")
    
    # At this point, face_img should be a Tensor.
    # MTCNN extract typically gives [C, H, W]. We need [B, C, H, W] for ResNet.
    if len(face_img.shape) == 3:  # If it's [C, H, W]
        face_img = face_img.unsqueeze(0)  # Add batch dimension -> [1, C, H, W]
    elif len(face_img.shape) == 2: # If it's [H, W] - this is what we're getting from mtcnn.extract
        print("Warning: mtcnn.extract returned a 2D tensor. Expanding to 3 channels.")
        face_img = face_img.unsqueeze(0)  # Add channel dimension -> [1, H, W]
        face_img = face_img.repeat(3, 1, 1) # Repeat channel to get [3, H, W]
        face_img = face_img.unsqueeze(0) # Add batch dimension -> [1, 3, H, W]

    # Ensure it's 4D [B, C, H, W] before passing to ResNet
    if len(face_img.shape) != 4 or face_img.shape[1] != 3: # Expecting 3 channels now
        # This error should ideally not be hit if the logic above is correct
        raise ValueError(f"Tensor input to ResNet is not in expected BCHW (3 channel) format. Shape: {face_img.shape}")

    # Move to device
    face_img = face_img.to(device)
    
    # Get embedding
    with torch.no_grad():
        embedding = resnet(face_img)
    
    return embedding[0].cpu().numpy()

def cosine_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two embeddings"""
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def load_image_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image_bytes = io.BytesIO(response.content)
        image = Image.open(image_bytes)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        print(f"Error loading image from URL {url}: {e}")
        return None

@app.post("/detect/", response_model=DetectionResult)
async def detect_face(request: DetectRequest):
    print(f"Received detection request for known_image_url: {request.known_image_url}") # Log request
    try:
        # Load known person image
        known_image = load_image_from_url(request.known_image_url)
        if known_image is None:
            print(f"Failed to load known_image_url: {request.known_image_url}") # Log failure
            return DetectionResult(message="Failed to load known image from URL.")
        
        # Get or compute embedding for known image
        if request.known_image_url in face_embedding_cache:
            known_embedding = face_embedding_cache[request.known_image_url]
            print(f"Using cached embedding for {request.known_image_url}")
        else:
            # Detect and align face in the known image
            try:
                # Extract face from the image
                print(f"Attempting to detect face in known image: {request.known_image_url}")
                face_tensor = mtcnn(known_image)
                
                if face_tensor is None:
                    print(f"No face found by MTCNN in known_image_url: {request.known_image_url}") # Log MTCNN failure
                    return DetectionResult(message="No face found in the known image.")
                
                print(f"Face successfully detected in known image: {request.known_image_url}")
                # Get embedding for the known face
                known_embedding = get_face_embedding(face_tensor)
                
                # Cache the embedding
                face_embedding_cache[request.known_image_url] = known_embedding
            except Exception as e:
                return DetectionResult(message=f"Error generating embedding for known face: {str(e)}")
        
        # Decode the frame data (base64 string) from webcam
        try:
            frame_bytes = base64.b64decode(request.frame_data.split(',')[1])
            frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame_image = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
            if frame_image is None:
                raise ValueError("cv2.imdecode returned None")
            
            # Convert BGR to RGB (PIL uses RGB)
            frame_image_rgb = cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_image_rgb)
            # ---- START DEBUG ----
            if frame_pil.mode != 'RGB':
                print(f"Warning: frame_pil is not RGB! Mode: {frame_pil.mode}. Converting to RGB.")
                frame_pil = frame_pil.convert('RGB')
            # ---- END DEBUG ----
        except Exception as e:
            print(f"Error decoding frame_data: {e}")
            return DetectionResult(message=f"Error decoding frame: {str(e)}")
        
        # Detect faces in the frame
        try:
            # Detect faces
            boxes, probs = mtcnn.detect(frame_pil)
            
            if boxes is None or len(boxes) == 0:
                return DetectionResult(
                    face_found_in_frame=False,
                    person_detected=False, # Explicitly set
                    message="No faces found in the video frame."
                )
            
            # Process each detected face
            best_match = None
            best_similarity = 0.0
            best_confidence = 0.0
            
            for i, (box, prob) in enumerate(zip(boxes, probs)):
                # Skip low confidence detections
                if prob < 0.9:
                    continue
                
                # Get face tensor
                # ---- START DEBUG PRINT ----
                print(f"Extracting face {i} with box: {box} and prob: {prob} from frame_pil mode: {frame_pil.mode}")
                # ---- END DEBUG PRINT ----
                face = mtcnn.extract(frame_pil, boxes, save_path=None)[i]
                
                if face is None:
                    print(f"mtcnn.extract returned None for box {i}") # Log if extract fails
                    continue
                
                # ---- START DEBUG PRINT ----
                print(f"Shape of 'face' tensor after mtcnn.extract for box {i}: {face.shape if face is not None else 'None'}")
                # ---- END DEBUG PRINT ----

                try:
                    # Get embedding for this face
                    face_embedding = get_face_embedding(face)
                    
                    # Calculate similarity
                    similarity = cosine_similarity(known_embedding, face_embedding)
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        x1, y1, x2, y2 = box
                        best_match = [int(x1), int(y1), int(x2-x1), int(y2-y1)]  # [x, y, width, height]
                        best_confidence = prob # This is MTCNN's confidence for this detected box
                except Exception as e:
                    print(f"Error generating embedding for detected face: {e}")
                    continue # Skip this problematic face
            
            # After processing all detected faces in the frame
            if best_match:
                is_target_person = best_similarity >= SIMILARITY_THRESHOLD
                detection_message = f"Target person detected. Similarity: {best_similarity:.4f}" if is_target_person else f"Face detected, not target. Best similarity: {best_similarity:.4f}"
                
                print(f"Detection result for {request.known_image_url}: Best Similarity={best_similarity:.4f}, Threshold={SIMILARITY_THRESHOLD}, Match={is_target_person}, Box={best_match}, MTCNN_Conf={best_confidence:.4f}")

                return DetectionResult(
                    face_found_in_frame=True,
                    person_detected=is_target_person,
                    bounding_box=best_match,
                    confidence_score=float(best_confidence), # MTCNN detection confidence of the best matching face
                    message=detection_message
                )
            else:
                # This means faces were detected by MTCNN (boxes is not None), but none of them could be processed
                # (e.g., all failed prob < 0.9, or mtcnn.extract failed, or get_face_embedding failed for all)
                print(f"Detection result for {request.known_image_url}: Faces found by MTCNN in frame, but no suitable candidate for matching (e.g. low confidence or embedding error).")
                return DetectionResult(
                    face_found_in_frame=True, # MTCNN did find face(s) initially
                    person_detected=False,
                    message="Faces found in frame, but no suitable candidate for matching."
                )
        except Exception as e:
            print(f"Error during face detection/processing in video frame: {e}")
            return DetectionResult(message=f"Error during face detection in frame: {str(e)}")
            
    except Exception as e:
        print(f"Outer error in detect_face endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Production-ready Face Recognition Service is running with FaceNet PyTorch."}

# For testing purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003) 