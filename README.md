---
title: CLIP Embedding API
emoji: 🖼️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
license: mit
short_description: Fast CLIP embeddings API with image, video & base64 support
---

#  CLIP Embedding API

**Fast, lightweight OpenAI CLIP embedding service with auto-keep-alive for 24/7 uptime.**

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/SamirDze/alg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Convert images and videos into 512-dimensional CLIP embeddings via simple HTTP API. Supports URL inputs, base64 encoding, and video frame extraction.

---

##  Features

-  **Fast embeddings** using OpenAI CLIP (ViT-B/32)
-  **Multiple input formats**: Image URLs, base64, video URLs
-  **Video support** with automatic frame extraction (3 frames)
-  **Auto keep-alive** via GitHub Actions (never sleeps!)
-  **Free tier optimized** for Hugging Face Spaces
-  **512-dimensional** normalized embeddings
-  **RESTful API** with JSON responses

---

##  Quick Start

### API Endpoint
```
https://samirdze-alg.hf.space/
```

### Python Example
```python
import requests

url = "https://samirdze-alg.hf.space/api/predict"

# Image from URL
response = requests.post(url, json={
    "data": ["https://example.com/image.jpg"]
})

result = response.json()
embedding = result["data"][0]["embedding"]
print(f"Embedding dimensions: {len(embedding)}")  # 512
```

### cURL Example
```bash
curl -X POST https://samirdze-alg.hf.space/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["https://example.com/image.jpg"]}'
```

### JavaScript Example
```javascript
const response = await fetch('https://samirdze-alg.hf.space/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    data: ['https://example.com/image.jpg']
  })
});

const result = await response.json();
const embedding = result.data[0].embedding;
console.log('Dimensions:', embedding.length); // 512
```

---

##  Input Formats

### 1️ Image URL
```json
{
  "data": ["https://example.com/photo.jpg"]
}
```

### 2️ Base64 Image
```json
{
  "data": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."]
}
```

### 3️ Video URL
```json
{
  "data": ["https://example.com/video.mp4"]
}
```
**Returns**: Embeddings for 3 frames (start, middle, end)

---

##  Response Format

### Single Image
```json
{
  "data": [{
    "success": true,
    "embedding": [0.123, -0.456, ...],
    "dimensions": 512,
    "type": "image"
  }]
}
```

### Video (Multiple Frames)
```json
{
  "data": [{
    "success": true,
    "embeddings": [
      [0.123, -0.456, ...],
      [0.789, -0.012, ...],
      [0.345, -0.678, ...]
    ],
    "embedding": [0.123, -0.456, ...],
    "dimensions": 512,
    "frames": 3,
    "type": "video"
  }]
}
```

---

##  Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone repository
git clone https://github.com/Samir-Guenchi/clip-embedding-api.git
cd clip-embedding-api

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Access at: http://localhost:7860

---

##  Deploy to Hugging Face Spaces

1. Fork this repo
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Create new Space → Import from Git
4. Paste your repo URL
5. Select **SDK: Gradio**
6. Deploy! 

---
##  Keep-Alive Setup

Free Hugging Face Spaces sleep after 48 hours. This repo includes **GitHub Actions** to keep your Space active 24/7.

### Enable Auto Keep-Alive

1. **Fork this repo** to your GitHub account
2. Go to **Settings** → **Actions** → **General**
3. Enable "Allow all actions"
4. Go to **Actions** tab
5. Click "I understand my workflows, go ahead and enable them"

 Your Space will now be pinged every 30 minutes automatically!

### Manual Trigger
Go to **Actions** → **Keep HF Space Alive** → **Run workflow**

---

##  Architecture

- **Model**: OpenAI CLIP ViT-B/32 (400M parameters)
- **Framework**: Gradio 4.44.0
- **Backend**: PyTorch + Transformers
- **Video Processing**: OpenCV (cv2)
- **Keep-Alive**: GitHub Actions (cron)

---

##  Use Cases

-  **Visual search engines** - Semantic image similarity
-  **Image deduplication** - Find duplicate/similar images
-  **Content recommendation** - Suggest visually similar content
-  **Video indexing** - Extract keyframe embeddings
-  **Multimodal AI** - Image-text matching tasks
-  **Vector databases** - Store image embeddings for RAG

---

##  Performance

| Input Type | Processing Time | Output |
|------------|----------------|--------|
| Image URL  | ~1-2s | 512-dim vector |
| Base64     | ~0.5-1s | 512-dim vector |
| Video URL  | ~3-5s | 3x 512-dim vectors |

*Times on HF Spaces free tier (2 vCPU, 16GB RAM)*

---

##  Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

##  License

MIT License - see [LICENSE](LICENSE) file

---
##  Links

- **Live Demo**: https://samirdze-alg.hf.space
- **API Docs**: https://samirdze-alg.hf.space (interactive UI)
- **CLIP Paper**: [Learning Transferable Visual Models](https://arxiv.org/abs/2103.00020)
- **Hugging Face Space**: https://huggingface.co/spaces/SamirDze/alg

---

##  Tips

- **Rate Limiting**: Free tier has rate limits. Consider caching results.
- **Batch Processing**: Process multiple images by calling API sequentially.
- **Embeddings Storage**: Store embeddings in vector DBs (Pinecone, Weaviate, Qdrant).
- **Similarity Score**: Use cosine similarity to compare embeddings.

### Calculate Similarity
```python
import numpy as np

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

similarity = cosine_similarity(embedding1, embedding2)
print(f"Similarity: {similarity:.2%}")
```

---

##  Troubleshooting

**Space is sleeping?**
- Check GitHub Actions are enabled
- Verify workflow runs every 30 min in Actions tab

**API returns error?**
- Ensure image URL is publicly accessible
- Check base64 string is properly formatted
- Video must be in supported format (mp4, mov, avi, webm)

**Slow response?**
- First request may be slow (model loading)
- Subsequent requests are faster (~1-2s)

---

<div align="center">

Made with by [Samir Guenchi](https://github.com/Samir-Guenchi)

⭐ Star this repo if you find it useful!

</div>
