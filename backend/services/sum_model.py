from pathlib import Path
import hashlib


def run_sum_saliency(image_path: Path) -> dict:
    """Mock SUM saliency inference.

    Replace this function with the real SUM model call when the model is
    installed. The mock output is deterministic per image file and shaped like
    saliency-derived metrics that a feature extractor can consume.
    """
    image_bytes = image_path.read_bytes()
    digest = hashlib.sha256(image_bytes).digest()

    focus_score = _scale_byte(digest[0], 0.45, 0.92)
    center_attention = _scale_byte(digest[1], 0.35, 0.85)
    edge_attention = _scale_byte(digest[2], 0.05, 0.35)
    text_attention = _scale_byte(digest[3], 0.03, 0.30)
    clutter_score = _scale_byte(digest[4], 0.10, 0.80)

    remaining_attention = max(0.0, 1.0 - center_attention - edge_attention - text_attention)

    return {
        "model": "SUM mock",
        "saliency_map_available": False,
        "raw_metrics": {
            "focus_score": round(focus_score, 2),
            "center_attention": round(center_attention, 2),
            "edge_attention": round(edge_attention, 2),
            "text_attention": round(text_attention, 2),
            "background_attention": round(remaining_attention, 2),
            "clutter_score": round(clutter_score, 2),
        },
    }


def _scale_byte(value: int, minimum: float, maximum: float) -> float:
    return minimum + (value / 255) * (maximum - minimum)
