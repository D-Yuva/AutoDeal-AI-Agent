import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

# LLM Configuration
llm_config_local = {"config_list": [{
    #"model": "llama-3.3-70b-versatile",
    "model": "llama3-70b-8192",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}]}

# Seller's minimum acceptable price (Hidden from Buyer)
SELLER_MIN_PRICE = 700  

# Buyer's maximum offer (Hidden from Seller)
BUYER_MAX_PRICE = 750  

# Buyer Agent
buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message="""
    You are a strategic buyer agent. Your goal is to negotiate the best possible deal.
    
    Strategy:
    1. Start negotiations with a price that is **80% of the seller's initial price** or you shouldn't accept the deal which is less than ${BUYER_MAX_PRICE}.
    2. Justify your offer with strong arguments (market value, condition, age, accessories).
    3. If the seller does not agree, gradually **increase your offer in small increments**.
    4. If the seller's final price is **too high** compared to what you can afford, say: "DEAL NOT DONE".
    
    Termination Rules:
    - If an agreement is reached at a fair price, say: "DEAL DONE at $X only if the price is more than the ${BUYER_MAX_PRICE}".
    - If no agreement is reached after 5 rounds, say: "DEAL NOT DONE".
    """
)

# Seller Agent
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message="""
You are a professional seller agent, but you should delay the deal as much as possible while still securing a sale.

Strategy:
1. Start negotiations at your asking price and resist lowering it, shouldn't go any higher than ${SELLER_MIN_PRICE}.
2. Use **delaying tactics**, such as checking with managers or justifying the price in detail.
3. If the buyer offers a fair price, **hesitate** before finalizing.
4. Only confirm the deal if absolutely necessary.

Termination Rules:
- If the buyer insists strongly, confirm: "DEAL DONE at $X only if the price is not higher than ${SELLER_MIN_PRICE}".
- If no agreement is reached after 5 rounds, say: "DEAL NOT DONE".
"""

)

# Group Chat Setup
groupchat = autogen.GroupChat(
    agents=[buyer, seller],  
    messages=[],
    max_round=5,  
    speaker_selection_method="round_robin"
)

# Group Chat Manager (handles conversation)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config={"use_docker": False},
    llm_config=llm_config_local,
    is_termination_msg=lambda x: "DEAL DONE" in x.get("content", "") or "DEAL NOT DONE" in x.get("content", ""),
)

# Product Details
product_details = """
Product: iPhone 13 Pro (256GB, Graphite)
Condition: Excellent, 1 year old
Original Price: $999
Includes: Original box, charger, warranty until 2024
"""

# Start Negotiation
response = seller.initiate_chat(
    recipient=buyer,
    message=f"Negotiate the best price for this product:\n{product_details}"
)

# Extract & Print Final Deal Result
final_message = response.get("content", "No deal reached")
print("\nFinal Result:", final_message)
import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

# LLM Configuration
llm_config_local = {"config_list": [{
    "model": "llama-3.3-70b-versatile",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}]}

# Seller's minimum acceptable price (Hidden from Buyer)
SELLER_MIN_PRICE = 700  

# Buyer's maximum offer (Hidden from Seller)
BUYER_MAX_PRICE = 750  

# Buyer Agent
buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
system_message="""
You are a strategic buyer agent, but your goal is to sell the product as **high as possible** while still keeping it below MRP.

Strategy:
1. Start with a **strong opening offer** (not too low).
2. Use **psychological pressure**: mention alternative sellers or limited-time deals.
3. If the seller delays, **push for urgency** ("I need to finalize today").
4. Increase your offer in small steps but **never exceed the MRP**.

Termination Rules:
- If the seller agrees to a reasonable price, confirm: "DEAL DONE at $X only if the price is higher than ${SELLER_MIN_PRICE}".
- If the seller refuses after 5 rounds, say: "DEAL NOT DONE".
"""

)

# Seller Agent
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message="""
    You are a professional seller agent. Your goal is to maximize profit while ensuring a fair deal.
    
    Strategy:
    1. Start negotiations at your asking price.
    2. Justify your price using **market analysis, product condition, and additional value (e.g., accessories, warranty)**.
    3. If the buyer counters, gradually **lower your price in small increments**.
    4. If the buyer's final offer is **too low**, say: "DEAL NOT DONE".

    Termination Rules:
    - If the buyer offers a fair price, confirm: "DEAL DONE at $X".
    - If no agreement is reached after 5 rounds, say: "DEAL NOT DONE".
    """
)

# Group Chat Setup
groupchat = autogen.GroupChat(
    agents=[buyer, seller],  
    messages=[],
    max_round=5,  
    speaker_selection_method="round_robin"
)

# Group Chat Manager (handles conversation)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config={"use_docker": False},
    llm_config=llm_config_local,
    is_termination_msg=lambda x: "DEAL DONE" in x.get("content", "") or "DEAL NOT DONE" in x.get("content", ""),
)

# Product Details
product_details = """
Product: iPhone 13 Pro (256GB, Graphite)
Condition: Excellent, 1 year old
Original Price: $999
Includes: Original box, charger, warranty until 2024
"""

# Start Negotiation
response = seller.initiate_chat(
    recipient=buyer,
    message=f"Negotiate the best price for this product:\n{product_details}"
)

# Extract & Print Final Deal Result
final_message = response.get("content", "No deal reached")
print("\nFinal Result:", final_message)

# Additional logging for better debugging
print("Conversation History:")
for message in groupchat.messages:
    print(message.get("content", ""))

# Calculate and print negotiation metrics
total_rounds = len(groupchat.messages)
buyer_offers = [message.get("content", "") for message in groupchat.messages if message.get("sender", "") == buyer.name]
seller_offers = [message.get("content", "") for message in groupchat.messages if message.get("sender", "") == seller.name]
print(f"Total Rounds: {total_rounds}")
print(f"Buyer Offers: {buyer_offers}")
print(f"Seller Offers: {seller_offers}")