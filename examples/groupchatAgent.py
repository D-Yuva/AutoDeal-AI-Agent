import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

# LLM Configuration
llm_config_local = {"config_list": [{
    "model": "llama-3.3-70b-versatile",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}]}

# Price thresholds
SELLER_MIN_PRICE = 700
BUYER_MAX_PRICE = 725
MAX_ROUNDS = 5

# Buyer Agent with enforced price limit
buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message=f"""
    You are a buyer agent with an ABSOLUTELY STRICT budget limit of ${BUYER_MAX_PRICE}.
    
    MANDATORY PRICE ENFORCEMENT:
    1. Your maximum budget is ${BUYER_MAX_PRICE}. This is an absolute, non-negotiable limit.
    2. If ANY price mentioned is above ${BUYER_MAX_PRICE}, you MUST IMMEDIATELY respond:
       "NO DEAL - Price exceeds my maximum budget of ${BUYER_MAX_PRICE}"
    3. You are NOT authorized to consider or negotiate ANY price above ${BUYER_MAX_PRICE}
    4. You CANNOT make exceptions, even for excellent conditions or additional features
    5. After {MAX_ROUNDS} rounds of negotiation, you MUST end with either "DEAL DONE" or "NO DEAL"
    
    Negotiation Process:
    1. First offer: Calculate 70% of asking price. If this exceeds ${BUYER_MAX_PRICE}, offer ${BUYER_MAX_PRICE - 50}
    2. Maximum increment: $25 per counter-offer
    3. Never exceed ${BUYER_MAX_PRICE} under any circumstances
    4. Walk away immediately if seller won't go below ${BUYER_MAX_PRICE}
    5. On final round, either accept the last offer (if <= ${BUYER_MAX_PRICE}) or state "NO DEAL"
    
    REQUIRED Response Format:
    ROUND_CHECK: (State which negotiation round this is)
    PRICE_CHECK: (Explicitly state if seller's price is above ${BUYER_MAX_PRICE})
    ACTION: (If above ${BUYER_MAX_PRICE} or final round with no agreement, state "NO DEAL". If agreement reached, state "DEAL DONE")
    RESEARCH: (Market analysis)
    OFFER: (Must be <= ${BUYER_MAX_PRICE})
    JUSTIFICATION: (Explain your offer)
    """
)

# Seller Agent with clearer price messaging and round awareness
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message=f"""
    You are a professional seller agent. Your goal is to maximize profit while ensuring a fair deal.
    Your MINIMUM acceptable price is ${SELLER_MIN_PRICE}.
    
    Negotiation Rules:
    1. Start by stating your asking price clearly
    2. Counter-offers should move in small increments
    3. State your minimum price if negotiations stall
    4. Never accept below ${SELLER_MIN_PRICE}
    5. After {MAX_ROUNDS} rounds, you MUST end with either "DEAL DONE" or "NO DEAL"
    
    Format your responses as:
    ROUND_CHECK: (State which negotiation round this is)
    CURRENT_PRICE: (Clearly state the price you're proposing)
    MARKET_POSITION: (Market analysis)
    PRODUCT_VALUE: (Key selling points)
    COUNTER_OFFER: (Your price)
    REASONING: (Justification)
    ACTION: (On final round, state "DEAL DONE" if agreement reached, otherwise "NO DEAL")
    """
)

# Modified User Proxy Agent with enhanced termination conditions
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: (
        "NO DEAL" in x.get("content", "") or 
        "DEAL DONE" in x.get("content", "") or
        "Price exceeds my maximum budget" in x.get("content", "")
    ),
    code_execution_config={
        "use_docker": False,
    }
)

# Group Chat Setup with exact round limit
groupchat = autogen.GroupChat(
    agents=[buyer, seller, user_proxy],
    messages=[],
    max_round=MAX_ROUNDS,
    speaker_selection_method="round_robin"
)

# Group Chat Manager with round counting
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config={"use_docker": False},
    llm_config=llm_config_local,
    is_termination_msg=lambda x: (
        "NO DEAL" in x.get("content", "") or 
        "DEAL DONE" in x.get("content", "")
    )
)

# Example Product Details
product_details = """
Product: iPhone 16 Pro (256GB, Graphite)
Condition: Excellent, 1 year old
Original Price: $999
Includes: Original box, charger, warranty until 2026
"""

# Start Negotiation with clear termination rules
user_proxy.initiate_chat(
    manager,
    message=f"""
Begin price negotiation with these strict rules:
1. Buyer's maximum price is ${BUYER_MAX_PRICE} - NO EXCEPTIONS
2. The Seller's minimum price is ${SELLER_MIN_PRICE} - NO EXCEPTIONS
3. Terminate immediately if price exceeds buyer's maximum
4. No flexibility on maximum price regardless of product condition
5. Negotiation MUST end after {MAX_ROUNDS} rounds with either "DEAL DONE" or "NO DEAL"
6. Both agents must track the current round number

Product Details:
{product_details}
    """
)