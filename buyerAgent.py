import autogen
import os
from productAgent import PRODUCT_DETAILS

# LLM Configuration
llm_config_local = {
    "config_list": [{
        "model": "llama3-70b-8192",
        "api_key": "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",
        "base_url": "https://api.groq.com/openai/v1"
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
    Your product is {PRODUCT_DETAILS}.
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

