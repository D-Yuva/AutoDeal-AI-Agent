import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

llm_config_local = {"config_list": [{
    #"model": "llama-3.3-70b-versatile",
    "model": "llama3-70b-8192",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}]}
    
# Product Details for negotitation, can be edited
PRODUCT_DETAILS = """
    Product: iPhone 13 Pro (256GB, Graphite)
    Condition: Excellent, 1 year old
    Original Price: $999
    Includes: Original box, charger, warranty until 2026
    """

# Minimum price the seller can offer
SELLER_MIN = 700;

# Maximum price the buyer can offer
BUYER_MAX = 800;

# Seller Agent
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message=f"""
    You are a professional seller agent aiming to maximize profit while maintaining customer satisfaction.
    Your final acceptable price is ${SELLER_MIN} never make deals below ${SELLER_MIN}.
    Always provide a counter-offer, the counter-offer should never be below ${SELLER_MIN} and highlight the product's value.
    
    Format your responses as:
    MARKET_POSITION: (your market analysis)
    PRODUCT_VALUE: (key value propositions)
    COUNTER_OFFER: (your price)
    REASONING: (justification for your price)
    """
)

# Buyer Agent
buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message=f"""
    You are a strategic buyer agent whose goal is to get the best possible deal.
    Your maximum budget is ${BUYER_MAX} shouldn't make deals above ${BUYER_MAX}.
    Start with a low initial offer always above ${BUYER_MAX} and gradually increase if needed.
    Your product is {PRODUCT_DETAILS}.
    If the price goes above ${BUYER_MAX} even after multiple negotiation round then you need to back out from the negotiation and say NO_DEAL.
    
    Format your responses as:
    RESEARCH: (list comparable prices found)
    ANALYSIS: (brief market analysis)
    OFFER: (your price offer)
    JUSTIFICATION: (reasons for your offer)
    """
)

# Start the negotiation
buyer.initiate_chat(
    seller, 
    message=f"""
    {PRODUCT_DETAILS}
    """
)