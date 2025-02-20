import autogen
import os
from productEnquiryAgent import PRODUCT_DETAILS
from sellerAgent import seller_agent

llm_config_local = {
    "config_list": [{
        "model": "gemini-2.0-flash-exp",
        "api_key": "AIzaSyCddZ9SuMOdXUcX_9DKgK4wOaEWrq86uWY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/"
    }]
}

# Buyer-specific configurations
BUYER_MAX = 800  # Maximum budget

def is_termination_message(message):
    termination_phrases = ["DEAL", "NO DEAL"]
    return any(phrase in message for phrase in termination_phrases)

# Customize your buyer agent here
buyer_agent = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message=f"""
    You are a strategic buyer agent whose goal is to get the best possible deal.
    Your maximum budget is ${BUYER_MAX} shouldn't make deals above ${BUYER_MAX}.
    Start with a low initial offer always above ${BUYER_MAX} and gradually increase if needed.
    These are your products {PRODUCT_DETAILS}. Negotiate for all the products one by one specifically with the spefication of that product, and whatever you think is the best for the customer respond with that.
    If the price goes above ${BUYER_MAX} even after multiple negotiation round then you need to back out from the negotiation and say NO DEAL.
    If you accept the price quoated by the seller or if the seller accepts the price then respond with DEAL if not accepted respond with NO DEAL
    
    Format your responses as:
    RESEARCH: (list comparable prices found)
    ANALYSIS: (brief market analysis)
    OFFER: (your price offer)
    JUSTIFICATION: (reasons for your offer)
    """,
    max_consecutive_auto_reply=5,
    is_termination_msg=is_termination_message,
)
