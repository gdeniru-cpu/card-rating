def extract_features(saliency_output: dict) -> dict:
    """Convert SUM-style saliency output into product-card features."""
    metrics = saliency_output["raw_metrics"]

    product_focus_score = metrics["focus_score"]
    clutter_score = metrics["clutter_score"]
    center_attention = metrics["center_attention"]
    edge_attention = metrics["edge_attention"]
    text_attention = metrics["text_attention"]
    background_attention = metrics["background_attention"]

    return {
        "product_focus_score": product_focus_score,
        "background_clutter": _clutter_label(clutter_score),
        "visual_hierarchy": _visual_hierarchy_label(
            product_focus_score=product_focus_score,
            center_attention=center_attention,
            edge_attention=edge_attention,
        ),
        "attention_distribution": {
            "product_center": center_attention,
            "image_edges": edge_attention,
            "text_or_badges": text_attention,
            "background": background_attention,
        },
    }


def _clutter_label(clutter_score: float) -> str:
    if clutter_score >= 0.60:
        return "high"
    if clutter_score >= 0.35:
        return "medium"
    return "low"


def _visual_hierarchy_label(
    product_focus_score: float,
    center_attention: float,
    edge_attention: float,
) -> str:
    if product_focus_score >= 0.75 and center_attention > edge_attention:
        return "strong product-first hierarchy"
    if product_focus_score >= 0.55:
        return "moderate hierarchy with room for improvement"
    return "weak hierarchy; attention may be split away from the product"
