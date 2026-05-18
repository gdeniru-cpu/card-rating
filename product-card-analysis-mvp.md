# Product Card Analysis MVP

## 1. Project Goal

The goal of this MVP is to help e-commerce users improve product card images before publishing them in an online store or marketplace.

Users upload a product image, also called a product card, and the system analyzes how well the image works visually and commercially. It looks for practical issues that can reduce trust, clarity, or buyer interest.

The system then returns clear recommendations that help the user improve the product card and increase the chance of conversion. For example, it may suggest improving lighting, removing background clutter, making the product larger, or adding a clearer price badge.

This MVP is focused on practical e-commerce use cases:

- improving product photos for marketplaces
- checking if a product card looks clear and trustworthy
- finding visual problems before launching an ad campaign
- giving small sellers fast feedback without needing a designer

## 2. User Flow

1. User uploads a product image.
2. The image is processed by a feature extraction model inspired by img2fmri.
3. The extracted visual and semantic features are sent to an LLM.
4. The LLM returns structured recommendations.
5. The user sees feedback in a simple report.

## 3. System Architecture (MVP Level)

The MVP has four main modules:

- **Frontend**: A simple upload interface where the user selects a product image and views the result.
- **Backend API**: Receives the image, sends it to the analysis module, sends extracted features to the LLM, and returns the final report.
- **Image Analysis Module**: An img2fmri-like feature extractor that converts the image into structured visual and semantic features.
- **LLM Recommendation Engine**: Converts structured image features into practical improvement suggestions.

Simple data flow:

```text
User
  |
  v
Frontend Upload Interface
  |
  v
Backend API
  |
  v
Image Analysis Module
  |
  v
Structured Image Features
  |
  v
LLM Recommendation Engine
  |
  v
Actionable Recommendations
  |
  v
Frontend Result Screen
```

## 4. Image Analysis Module

The Image Analysis Module converts the uploaded product image into structured features. For the MVP, this module can be treated as a black-box encoder inspired by img2fmri.

The module does not need to explain how it works internally. Its job is to describe the image in a format that the backend and LLM can use.

Possible extracted features include:

- composition hints, such as whether the product is centered
- cropping issues, such as parts of the product being cut off
- visual clarity, such as blur or low resolution
- background noise, such as clutter or distracting objects
- lighting quality, such as shadows or underexposure
- presence of text, labels, badges, or price elements
- product visibility, such as whether the main item is easy to identify

The output should be structured and simple enough for the LLM to interpret reliably.

## 5. LLM Recommendation Engine

The LLM Recommendation Engine receives structured features from the Image Analysis Module and turns them into human-readable feedback.

Input:

- structured visual and semantic features
- optional product category, if provided by the user
- optional marketplace or store context

Output:

- clear recommendations
- short explanations of why each change matters
- practical next steps the user can apply immediately

Recommendations should be actionable, not abstract. Instead of saying "improve visual appeal", the system should say what to change.

Example recommendation types:

- improve lighting so the product looks cleaner and more trustworthy
- change the background to a plain or brand-matching color
- reposition the product so it is centered and not cropped
- reduce clutter around the product
- improve contrast between the product and background
- add marketing elements such as discount badges, price highlights, or key benefit labels

## 6. Example Input / Output

Example extracted features:

```json
{
  "product_visibility": "medium",
  "main_object_centered": false,
  "cropping_issue": true,
  "visual_clarity": "good",
  "background_noise": "high",
  "lighting_quality": "uneven",
  "text_detected": true,
  "text_readability": "low",
  "contrast": "medium",
  "marketing_elements": {
    "price_badge": false,
    "discount_badge": false,
    "benefit_labels": true
  },
  "overall_risk": "image may look cluttered and unclear on mobile"
}
```

Example LLM output:

- Center the product so it becomes the main focus of the image.
- Fix the cropping so the full product is visible, especially on mobile screens.
- Replace the busy background with a cleaner background to reduce distractions.
- Improve lighting by reducing shadows on the left side of the product.
- Increase text size or simplify the text block so it is easier to read.
- Add a clear price or discount badge if this image will be used in a promotion.
- Improve contrast between the product and background so the item stands out more.

## 7. MVP Limitations

- The MVP does not track real conversion rate changes yet.
- The MVP does not include A/B testing.
- The image analysis model is not trained on a proprietary e-commerce dataset.
- Recommendations are heuristic and LLM-driven.
- The system may give general advice that still needs human review.
- Results may vary by product category, marketplace, and target audience.

## 8. Future Improvements

- Collect a dataset of high-converting and low-converting product cards.
- Fine-tune the model for e-commerce image aesthetics.
- Add A/B testing integration to measure which recommendations improve sales.
- Personalize recommendations by niche, such as fashion, electronics, beauty, food, or home goods.
- Add marketplace-specific checks for platforms like Amazon, Etsy, Shopify, or local marketplaces.
- Track before-and-after performance to improve recommendation quality over time.
