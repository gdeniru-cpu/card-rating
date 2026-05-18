from pydantic import BaseModel, Field


class UploadImageResponse(BaseModel):
    image_id: str = Field(..., examples=["4f9c2d2e8b9a4d2c9b7f6c1a2b3d4e5f.jpg"])


class ImageFeatures(BaseModel):
    product_focus_score: float = Field(..., ge=0, le=1)
    background_clutter: str
    visual_hierarchy: str
    attention_distribution: dict[str, float]


class AnalyzeImageResponse(BaseModel):
    image_id: str
    features: ImageFeatures
    recommendations: list[str]
