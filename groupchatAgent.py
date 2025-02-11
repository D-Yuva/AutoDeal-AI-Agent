import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

# LLM Configuration
llm_config_local = {"config_list": [{
    "model": "llama-3.3-70b-versatile",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}]}

# Seller's minimum acceptable price
SELLER_MIN_PRICE = 700

# Buyer Agent
buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message="""
    You are a strategic buyer agent. Your goal is to get the best possible deal.
    Your strategy:
    1. Research market value and comparable prices.
    2. Start negotiations with a reasonable initial offer (70-80% of asking price).
    3. Justify your offer with strong arguments.
    4. Negotiate but always aim for the lowest possible deal.
    5. Be ready to walk away if the seller is unreasonable.
    
    Format your responses as:
    RESEARCH: (comparable prices found)
    ANALYSIS: (brief market analysis)
    OFFER: (your price offer)
    JUSTIFICATION: (reasons for your offer)
    """
)

# Seller Agent
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message="""
    You are a professional seller agent. Your goal is to maximize profit while ensuring a fair deal.
    Your strategy:
    1. Evaluate offers based on your minimum price.
    2. Use market analysis to justify your counteroffers.
    3. Highlight product value and unique selling points.
    4. Be firm and strategic in negotiations, aiming to sell above your minimum price.
    5. If the buyer is unreasonable, reject the deal and state "NO DEAL".
    
    Format your responses as:
    MARKET_POSITION: (your market analysis)
    PRODUCT_VALUE: (key selling points)
    COUNTER_OFFER: (your price counteroffer)
    REASONING: (justification for your price)
    """
)

# User Proxy Agent
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: "DEAL DONE" in x.get("content", "") or "DEAL NOT DONE" in x.get("content", ""),
    code_execution_config={
        "use_docker": False,
    }
)

# Group Chat Setup
groupchat = autogen.GroupChat(
    agents=[buyer, seller, user_proxy],
    messages=[],
    max_round=5,
    speaker_selection_method="round_robin"
)

# Group Chat Manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config={"use_docker": False},
    llm_config=llm_config_local,
    is_termination_msg=lambda x: "DEAL DONE" in x.get("content", "") or "DEAL NOT DONE" in x.get("content", ""),
)

# Example Product Details
product_details = """
Product: iPhone 13 Pro (256GB, Graphite)
Condition: Excellent, 1 year old
Original Price: $999
Asking Price: $750
Includes: Original box, charger, warranty until 2024
"""

# Start Negotiation
user_proxy.initiate_chat(
    manager,
    message=f"Negotiate the best price for this product:\n{product_details}"
)
