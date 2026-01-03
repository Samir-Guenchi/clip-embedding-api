"""
CLIP Image & Video Embedding API - Lightweight version for HF Spaces free tier
Supports URL, base64 image input, and video URLs (extracts frames)
"""

import gradio as gr
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import requests
from io import BytesIO
import base64
import tempfile
import os

# Use CPU and smaller memory footprint
model = None
processor = None

def load_model():
    global model, processor
    if model is None:
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model.eval()
    return model, processor

def extract_video_frames(video_url: str, num_frames: int = 3):
    """Extract frames from video URL using cv2"""
    try:
        import cv2
        import numpy as np
        
        # Download video to temp file
        response = requests.get(video_url, timeout=60, stream=True)
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            for chunk in response.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp_path = tmp.name
        
        # Open video
        cap = cv2.VideoCapture(tmp_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            os.unlink(tmp_path)
            return []
        
        # Calculate frame positions (start, middle, end)
        if num_frames == 1:
            positions = [0]
        elif num_frames == 2:
            positions = [0, total_frames - 1]
        else:
            positions = [0, total_frames // 2, max(0, total_frames - 10)]
        
        frames = []
        for pos in positions[:num_frames]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ret, frame = cap.read()
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                frames.append(pil_image)
        
        cap.release()
        os.unlink(tmp_path)
        
        return frames
    except Exception as e:
        print(f"Video frame extraction error: {e}")
        return []

def is_video_url(url: str) -> bool:
    """Check if URL is a video"""
    video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
    url_lower = url.lower()
    return any(ext in url_lower for ext in video_extensions) or '/video/' in url_lower

def get_embedding(image_input: str):
    """Get CLIP embedding from image URL, base64 string, or video URL"""
    try:
        if not image_input:
            return {"success": False, "error": "Please provide an image/video URL or base64 string"}
        
        # Load model on first use
        model, processor = load_model()
        
        images = []
        is_video = False
        
        # Check if it's a video URL
        if image_input.startswith('http') and is_video_url(image_input):
            is_video = True
            frames = extract_video_frames(image_input, num_frames=3)
            if not frames:
                return {"success": False, "error": "Could not extract frames from video"}
            images = frames
        
        # Check if it's base64 (data:image/... or raw base64)
        elif image_input.startswith('data:image'):
            base64_data = image_input.split(',')[1] if ',' in image_input else image_input
            image_bytes = base64.b64decode(base64_data)
            images = [Image.open(BytesIO(image_bytes)).convert('RGB')]
        
        elif not image_input.startswith('http'):
            # Try as raw base64
            try:
                image_bytes = base64.b64decode(image_input)
                images = [Image.open(BytesIO(image_bytes)).convert('RGB')]
            except:
                return {"success": False, "error": "Invalid input: provide URL or base64"}
        else:
            # It's an image URL - download it
            response = requests.get(image_input, timeout=30)
            images = [Image.open(BytesIO(response.content)).convert('RGB')]
        
        # Get embeddings for all images/frames
        all_embeddings = []
        for img in images:
            inputs = processor(images=img, return_tensors="pt")
            with torch.no_grad():
                features = model.get_image_features(**inputs)
            
            # Normalize
            embedding = features / features.norm(dim=-1, keepdim=True)
            all_embeddings.append(embedding[0].tolist())
        
        # For single image, return single embedding
        # For video, return array of frame embeddings
        if len(all_embeddings) == 1:
            return {
                "success": True, 
                "embedding": all_embeddings[0], 
                "dimensions": 512,
                "type": "image"
            }
        else:
            return {
                "success": True,
                "embeddings": all_embeddings,
                "embedding": all_embeddings[0],  # First frame as default
                "dimensions": 512,
                "frames": len(all_embeddings),
                "type": "video"
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}

# Gradio interface with API enabled
demo = gr.Interface(
    fn=get_embedding,
    inputs=gr.Textbox(
        label="Image/Video (URL or base64)", 
        placeholder="https://example.com/image.jpg or video.mp4 or data:image/jpeg;base64,..."
    ),
    outputs=gr.JSON(label="Result"),
    title="CLIP Embedding API",
    description="Get 512-dim CLIP embeddings from image URL, base64, or video URL (extracts 3 frames)",
    api_name="predict"
)

if __name__ == "__main__":
    demo.launch()
