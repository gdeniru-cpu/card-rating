from backend.models.schemas import ImageFeatures


def generate_recommendations(features: ImageFeatures | dict) -> list[str]:
    """Return LLM-style recommendations from structured image features.

    This is intentionally implemented as a placeholder. In production, this
    function would send the prompt returned by `_build_prompt` to the OpenAI API
    and parse the model response into a list of recommendations.
    """
    if isinstance(features, ImageFeatures):
        feature_data = features.model_dump()
    else:
        feature_data = features

    prompt = _build_prompt(feature_data)

    # Placeholder for a real OpenAI API call:
    #
    # from openai import OpenAI
    # client = OpenAI()
    # response = client.responses.create(
    #     model="gpt-4.1-mini",
    #     input=prompt,
    # )
    # return parse_recommendations(response.output_text)

    return _mock_llm_response(feature_data, prompt)


def _build_prompt(features: dict) -> str:
    return (
        "You are an e-commerce creative optimization assistant. "
        "Use these product-card visual attention features to generate concise, "
        "actionable recommendations that can improve conversion rate.\n\n"
        f"Features: {features}\n\n"
        "Return markdown bullet recommendations only."
    )


def _mock_llm_response(features: dict, prompt: str) -> list[str]:
    recommendations = []

    focus_score = features["product_focus_score"]
    clutter = features["background_clutter"]
    hierarchy = features["visual_hierarchy"]
    attention = features["attention_distribution"]

    if focus_score < 0.70:
        recommendations.append(
            "- Make the product larger or more centered so it becomes the main focus of the card."
        )
    else:
        recommendations.append(
            "- Keep the product as the primary focal point; the current focus score is a good base."
        )

    if clutter in {"medium", "high"}:
        recommendations.append(
            "- Simplify the background or remove secondary objects that compete with the product."
        )

    if attention["image_edges"] > 0.25:
        recommendations.append(
            "- Move important visual elements away from the image edges to avoid attention leakage."
        )

    if attention["text_or_badges"] < 0.10:
        recommendations.append(
            "- Add a small price, discount, or benefit badge if the card is meant to drive a quick purchase."
        )
    elif attention["text_or_badges"] > 0.22:
        recommendations.append(
            "- Reduce or simplify text elements so they support the product instead of competing with it."
        )

    if "weak" in hierarchy:
        recommendations.append(
            "- Rebuild the layout around one clear visual priority: product first, offer second, details third."
        )
    elif "moderate" in hierarchy:
        recommendations.append(
            "- Strengthen the visual hierarchy by increasing product contrast and making the main offer easier to scan."
        )

    recommendations.append(
        "- Check the final card on a mobile screen, where small text and weak contrast usually hurt conversion most."
    )

    return recommendations
