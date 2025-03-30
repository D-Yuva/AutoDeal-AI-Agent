import autogen
import os
from productEnquiryAgent import PRODUCT_DETAILS
from sellerAgent import seller_agent
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

llm_config_local = {
    "config_list": [{
        "model": "gemini-2.0-flash-exp",
        "api_key": GEMINI_API_KEY,
        "base_url": "https://generativelanguage.googleapis.com/v1beta/"
    }]
}

def is_termination_message(message):
    termination_phrases = ["DEAL", "NO DEAL"]
    return any(phrase in message for phrase in termination_phrases)

# Customize your buyer agent here
buyer_agent = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message=f"""
You are a strategic buyer agent whose goal is to get the best possible deal.
    
    For each product in the {PRODUCT_DETAILS}:
    1. Research market prices and comparable products
    2. Analyze product specifications and market conditions
    3. Make strategic offers based on product value and market analysis
    4. Start with a lower initial offer (around 60-70% of typical market price)
    5. Gradually increase if needed, but ensure final price reflects fair market value
    
    Negotiate for each product individually, considering:
    - Product specifications and quality
    - Current market prices
    - Seasonal factors and availability
    - Bulk purchase opportunities
    - Market competition
    
    End negotiation conditions:
    - Accept deal if price is fair and aligned with market value
    - Reject deal if price is significantly above market value
    - Respond with "DEAL" if accepted
    - Respond with "NO DEAL" if rejected
    
    Format your responses as:
    RESEARCH: (list comparable prices found)
    ANALYSIS: (brief market analysis)
    OFFER: (your price offer)
    JUSTIFICATION: (reasons for your offer)
    """,
    max_consecutive_auto_reply=5,
    is_termination_msg=is_termination_message,
)
