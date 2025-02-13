import autogen
import os

# LLM Configuration
llm_config_local = {
    "config_list": [{
        "model": "llama3-70b-8192",
        "api_key": "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",
        "base_url": "https://api.groq.com/openai/v1"
    }]
}

# Seller-specific configurations
SELLER_MIN = 700  # Minimum acceptable price

def is_termination_message(message):
    termination_phrases = ["DEAL", "NO DEAL"]
    return any(phrase in message for phrase in termination_phrases)

# Customize your seller agent here
seller_agent = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message=f"""
    You are a professional seller agent aiming to maximize profit while maintaining customer satisfaction.
    The product you are going to bargain {PRODUCT_DETAILS}.
    Your final acceptable price is ${SELLER_MIN} never make deals below ${SELLER_MIN}.
    Always provide a counter-offer, the counter-offer should never be below ${SELLER_MIN} and highlight the product's value.
    If you accept the price quoated by the buyer or if the seller accepts your price then respond with DEAL if not accepted respond with NO DEAL

    Format your responses as:
    MARKET_POSITION: (your market analysis)
    PRODUCT_VALUE: (key value propositions)
    COUNTER_OFFER: (your price)
    REASONING: (justification for your price)
    """,
    max_consecutive_auto_reply=5,
    is_termination_msg=is_termination_message,
)