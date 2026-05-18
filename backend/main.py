from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.models.schemas import AnalyzeImageResponse, UploadImageResponse
from backend.services.feature_extractor import extract_features
from backend.services.llm_service import generate_recommendations
from backend.services.sum_model import run_sum_saliency

app = FastAPI(
    title="Product Card Analysis MVP",
    description="Analyze e-commerce product cards with mock SUM saliency and LLM recommendations.",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "product-card-analysis-mvp"}


@app.post("/upload-image", response_model=UploadImageResponse)
async def upload_image(file: UploadFile = File(...)) -> UploadImageResponse:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a JPEG, PNG, or WEBP image.",
        )

    extension = Path(file.filename or "").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        extension = ".jpg"

    image_id = f"{uuid4().hex}{extension}"
    image_path = UPLOAD_DIR / image_id

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    image_path.write_bytes(contents)

    return UploadImageResponse(image_id=image_id)


@app.post("/analyze-image/{image_id}", response_model=AnalyzeImageResponse)
async def analyze_image(image_id: str) -> AnalyzeImageResponse:
    image_path = UPLOAD_DIR / image_id
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found.")

    saliency_output = run_sum_saliency(image_path)
    features = extract_features(saliency_output)
    recommendations = generate_recommendations(features)

    return AnalyzeImageResponse(
        image_id=image_id,
        features=features,
        recommendations=recommendations,
    )
