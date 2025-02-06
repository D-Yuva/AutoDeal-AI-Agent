import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

llm_config = {
    "config_list": [{
        "model": "gpt-3.5-turbo",
        "cache_seed": 45,
        "temperature": 0.7,  # Increased for more creative negotiations
        "timeout": 120,
    }]
}

# Configuration for the LLM
llm_config_local = {"config_list": [{
    "model": "llama-3.2-3b-instruct",
    "base_url": "http://localhost:1234/v1" 
}]}

def validate_deal(message):
    """Check if a deal has been reached or negotiations should continue"""
    # Handle both dictionary and string messages
    content = message if isinstance(message, str) else message.get("content", "")
    
    last_buyer_offer = None
    last_seller_offer = None
    
    # Extract latest offers from the conversation
    if "OFFER:" in content:
        try:
            last_buyer_offer = float(content.split("OFFER:")[1].split()[0].replace("$", ""))
        except (IndexError, ValueError):
            pass
    
    if "COUNTER_OFFER:" in content:
        try:
            last_seller_offer = float(content.split("COUNTER_OFFER:")[1].split()[0].replace("$", ""))
        except (IndexError, ValueError):
            pass
    
    # Define negotiation product details globally
    product_details = """
    Product: iPhone 13 Pro (256GB, Graphite)
    Condition: Excellent, 1 year old
    Original Price: $999
    Asking Price: $750
    Includes: Original box, charger, warranty until 2024
    """

    # Check termination conditions
    if last_buyer_offer and last_seller_offer:
        if abs(last_buyer_offer - last_seller_offer) <= 50:  # $50 difference threshold
            print("\n" + "="*50)
            print(f"DEAL_AGREED at ${(last_buyer_offer + last_seller_offer)/2:.2f}")
            print("="*50 + "\n")
            return True
        elif "FINAL OFFERS" in content:  # Add a final round termination condition
            print("\n" + "="*50)
            print(f"NO_DEAL - Final offers: Buyer ${last_buyer_offer:.2f}, Seller ${last_seller_offer:.2f}")
            print("="*50 + "\n")
            return True
    
    return False

# Create the buyer and seller agents
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message="""
    You are a professional seller agent aiming to maximize profit while maintaining customer satisfaction.
    Your final acceptable price is $700.
    Always provide a counter-offer and highlight the product's value.
    
    Format your responses as:
    MARKET_POSITION: (your market analysis)
    PRODUCT_VALUE: (key value propositions)
    COUNTER_OFFER: (your price)
    REASONING: (justification for your price)
    """
)

buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message="""
    You are a strategic buyer agent whose goal is to get the best possible deal.
    Your maximum budget is $650.
    Start with a low initial offer and gradually increase if needed.
    
    Format your responses as:
    RESEARCH: (list comparable prices found)
    ANALYSIS: (brief market analysis)
    OFFER: (your price offer)
    JUSTIFICATION: (reasons for your offer)
    """
)

# Create the user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config={"use_docker": False},
    is_termination_msg=validate_deal,
    human_input_mode="NEVER"
)

# Set up the group chat
groupchat = autogen.GroupChat(
    agents=[buyer, seller, user_proxy],
    messages=[],
    max_round=5,
    speaker_selection_method="round_robin"
)

# Create the group chat manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config={"use_docker": False},
    llm_config=llm_config_local, 
    is_termination_msg=validate_deal
)

# Start the negotiation
user_proxy.initiate_chat(
    manager, 
    message="""
    Product: iPhone 13 Pro (256GB, Graphite)
    Condition: Excellent, 1 year old
    Original Price: $999
    Asking Price: $750
    Includes: Original box, charger, warranty until 2024
    Negotiate the best possible price for this product.
    """
)