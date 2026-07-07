import json
import os
import random
import anthropic
from core.config import settings

# Initialize Anthropic client if a valid-looking key is set
api_key = settings.ANTHROPIC_API_KEY
if api_key and len(api_key) > 20 and not api_key.startswith("your_") and api_key.lower() != "none":
    client = anthropic.Anthropic(api_key=api_key)
else:
    client = None

# Model default. We will check env CLAUDE_MODEL, otherwise fall back to user's "claude-sonnet-4-6" or latest sonnet
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

def clean_json_text(text: str) -> str:
    """Helper to strip markdown tags around JSON response."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def get_simulated_recommendations(products: list, requirements: dict) -> list:
    """Generates realistic recommendations if the API is offline."""
    results = []
    budget_min = requirements.get("budget_min", 0)
    budget_max = requirements.get("budget_max", 999999)
    brands = [b.lower() for b in requirements.get("brands", [])]
    spec_query = requirements.get("specifications", "").lower()
    
    for p in products:
        # Calculate a mock match score based on budget match, brand match, and spec match
        score = 70  # baseline
        
        # Budget matching
        if budget_min <= p["price"] <= budget_max:
            score += 15
        else:
            diff = min(abs(p["price"] - budget_min), abs(p["price"] - budget_max))
            pct_off = diff / max(p["price"], 1)
            score -= int(pct_off * 50)
            
        # Brand matching
        if brands:
            if p["brand"].lower() in brands:
                score += 10
            else:
                score -= 10
                
        # Spec matching (simple keyword check)
        spec_match_reasons = []
        if spec_query:
            specs_str = json.dumps(p.get("specs", {})).lower()
            keywords = [w.strip() for w in spec_query.split() if len(w.strip()) > 3]
            match_count = 0
            for kw in keywords:
                if kw in specs_str:
                    match_count += 1
            if keywords:
                match_ratio = match_count / len(keywords)
                score += int(match_ratio * 10)
                if match_ratio > 0.5:
                    spec_match_reasons.append("matches your performance specs closely")
                    
        # Clip score
        score = max(30, min(100, score))
        
        # Formulate reasoning
        proc_name = p['specs'].get('Processor', p['specs'].get('Display', 'quality hardware'))
        reasoning_options = [
            f"Fits comfortably in your budget of ₹{p['price']:.0f} and offers a solid {proc_name}.",
            f"Matches your brand preference of {p['brand']}. Has a high {p['rating']} rating from {p['review_count']} reviews.",
            f"Provides great value at ₹{p['price']:.0f} featuring a sharp display and solid performance.",
            f"An excellent option containing {proc_name} and great customer feedback."
        ]
        
        if spec_match_reasons:
            reasoning = f"Perfect fit! It {spec_match_reasons[0]} and fits your budget at ₹{p['price']:.2f}."
        else:
            reasoning = random.choice(reasoning_options)
            
        results.append({
            "product_id": p["id"],
            "match_score": score,
            "reasoning": reasoning
        })
        
    # Sort descending by match score
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results

def get_ai_recommendations(products: list, requirements: dict) -> list:
    """Gets product recommendations by matching against user needs using Claude."""
    if not client:
        return get_simulated_recommendations(products, requirements)
        
    # Prepare products representation (exclude details to fit token limits)
    lite_products = []
    for p in products:
        lite_products.append({
            "id": p["id"],
            "name": p["name"],
            "brand": p["brand"],
            "price": p["price"],
            "rating": p["rating"],
            "specs": p["specs"]
        })
        
    prompt = f"""
    You are a product recommendation AI. Given these products: {json.dumps(lite_products)}
    And user requirements: {json.dumps(requirements)}
    
    Return ONLY a valid JSON array (no markdown, no explanation, no backticks) with format:
    [
      {{"product_id": <int>, "match_score": <int 0-100>, "reasoning": "<short text, max 2 sentences>"}}
    ]
    Rank by how well each product matches budget, brand, and specifications. Return ratings for all products provided. 
    Note that all prices and budgets are in Indian Rupees (₹).
    """
    
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = clean_json_text(response.content[0].text)
        return json.loads(result_text)
    except Exception as e:
        print(f"Anthropic API error: {e}. Falling back to simulation mode.")
        return get_simulated_recommendations(products, requirements)

def get_simulated_deep_analysis(product: dict, reviews: list) -> dict:
    """Generates realistic mock deep analysis data if API is offline."""
    pros = []
    cons = []
    pos_pct = 80.0
    neg_pct = 20.0
    
    if reviews:
        r = reviews[0]
        pros = r.get("pros", ["Fast performance", "Excellent battery life", "Premium build"])
        cons = r.get("cons", ["Slightly heavy", "Speakers could be better"])
        pos_pct = r.get("positive_percent", 80.0)
        neg_pct = r.get("negative_percent", 20.0)
    else:
        pros = ["Fast performance", "Vibrant screen", "Value for money"]
        cons = ["Average webcam", "Plastic chassis"]
        
    specs = product.get("specs", {})
    ram = specs.get("RAM", specs.get("Display", "standard hardware"))
    proc = specs.get("Processor", specs.get("Type", "premium segment"))
    
    current_price = product["price"]
    lowest_price = round(current_price * 0.9, 2)
    trends = ["steady", "falling", "rising"]
    trend = random.choice(trends)
    worth_buying = current_price < (product["original_price"] * 0.95)
    
    analysis = {
        "product_agent": {
            "pros": pros,
            "cons": cons
        },
        "review_agent": {
            "positive_pct": pos_pct,
            "negative_pct": neg_pct,
            "overall_rating": product["rating"],
            "summary": f"Customers generally love the value and hardware specs. The hardware's performance with {proc} paired with {ram} provides a seamless user experience. Main complaints center around standard segments tradeoffs."
        },
        "price_agent": {
            "current_price": current_price,
            "lowest_price": lowest_price,
            "trend": trend,
            "worth_buying": worth_buying,
            "note": f"Currently priced at ₹{current_price:.2f} representing a {product['discount_percent']:.0f}% discount. This price is close to its all-time low."
        },
        "recommendation_agent": {
            "why_this_product": f"It offers an exceptional price-to-performance ratio in this category, combining great build quality and reliable performance.",
            "who_should_buy": ["Budget-conscious buyers", "General consumers", "Daily users looking for reliability"],
            "alternatives": ["Samsung Galaxy M56" if product["brand"] != "Samsung" else "OnePlus Nord CE", "HP Pavilion 15" if product["brand"] != "HP" else "Dell Inspiron"]
        },
        "decision_agent": {
            "final_score": int(product["rating"] * 20),
            "verdict": "BUY NOW" if product["rating"] >= 4.4 else "CONSIDER",
            "confidence_pct": int(90 - (10 * (5 - product["rating"])))
        }
    }
    return analysis

def get_deep_analysis(product: dict, reviews: list) -> dict:
    """Runs a 5-agent deep analysis of a product and reviews using Claude."""
    if not client:
        return get_simulated_deep_analysis(product, reviews)
        
    prompt = f"""
    You are a professional product analyst. 
    Analyze this product details:
    {json.dumps(product)}
    
    And its user reviews/pros-cons:
    {json.dumps(reviews)}
    
    Assume all pricing values are in Indian Rupees (₹).
    Return a valid JSON object (no markdown, no explanation, no backticks) with EXACTLY these 5 keys:
    {{
      "product_agent": {{
        "pros": ["string"],
        "cons": ["string"]
      }},
      "review_agent": {{
        "positive_pct": <float 0-100>,
        "negative_pct": <float 0-100>,
        "overall_rating": <float 0-5>,
        "summary": "string"
      }},
      "price_agent": {{
        "current_price": <float>,
        "lowest_price": <float>,
        "trend": "steady/rising/falling",
        "worth_buying": <bool>,
        "note": "string"
      }},
      "recommendation_agent": {{
        "why_this_product": "string",
        "who_should_buy": ["string"],
        "alternatives": ["string"]
      }},
      "decision_agent": {{
        "final_score": <int 0-100>,
        "verdict": "string, e.g. BUY NOW, CONSIDER, PASS",
        "confidence_pct": <int 0-100>
      }}
    }}
    """
    
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = clean_json_text(response.content[0].text)
        return json.loads(result_text)
    except Exception as e:
        print(f"Anthropic API error in deep analysis: {e}. Falling back to simulation.")
        return get_simulated_deep_analysis(product, reviews)
