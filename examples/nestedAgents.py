import autogen

import os

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

#Configuration for the LLM

llm_config = {
    "config_list": [{
        "model": "gpt-3.5-turbo",
        "cache_seed": 45,
        "temperature": 0.7,  # Increased for more creative negotiations
        "timeout": 120,
    }]
}

llm_config_local = {"config_list": [{
    "model": "llama-3.3-70b-versatile",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}]}

def reflection_message(recipient, messages, sender, config):
    print("Reflecting...")
    return f"Reflect and provide critique on the following writing. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"

# Create the buyer agent
buyer = autogen.AssistantAgent(
    name="Buyer",
    llm_config=llm_config_local,
    system_message="""
    You are a strategic buyer agent whose goal is to get the best possible deal.
    Your responsibilities:
    1. Analyze the product specifications and market value
    2. Research comparable prices from other sellers and websites
    3. Start negotiations with a reasonable initial offer (usually 70-80% of asking price)
    4. Use market research to justify your offered price
    5. Be willing to compromise but always aim for the best deal
    6. Consider factors like product condition, warranty, and shipping costs
    
    Format your responses as:
    RESEARCH: (list comparable prices found)
    ANALYSIS: (brief market analysis)
    OFFER: (your price offer)
    JUSTIFICATION: (reasons for your offer)
    """
)

# Create the seller agent
seller = autogen.AssistantAgent(
    name="Seller",
    llm_config=llm_config_local,
    system_message="""
    You are a professional seller agent aiming to maximize profit while maintaining customer satisfaction.
    Your responsibilities:
    1. Evaluate buyer offers based on your minimum acceptable price
    2. Consider market conditions and competition
    3. Provide justification for your pricing
    4. Be willing to negotiate but maintain profitability
    5. Highlight product value propositions
    6. Find win-win solutions when possible
    
    Format your responses as:
    MARKET_POSITION: (your market analysis)
    PRODUCT_VALUE: (key value propositions)
    COUNTER_OFFER: (your price)
    REASONING: (justification for your price)
    """
)

# Create the user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: "DEAL_AGREED" in x.get("content", "") or "NO_DEAL" in x.get("content", ""),
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "negotiation_logs",
        "use_docker": False,
    }
)

def validate_deal(messages):
    """Check if a deal has been reached or negotiations should continue"""
    last_buyer_offer = None
    last_seller_offer = None
    
    # Extract latest offers from the conversation
    for msg in messages:
        content = msg.get("content", "")
        if "OFFER:" in content:
            last_buyer_offer = float(content.split("OFFER:")[1].split()[0])
        if "COUNTER_OFFER:" in content:
            last_seller_offer = float(content.split("COUNTER_OFFER:")[1].split()[0])
    
    if last_buyer_offer and last_seller_offer:
        if abs(last_buyer_offer - last_seller_offer) <= 50:  # $50 difference threshold
            return "DEAL_AGREED"
        elif len(messages) > 3:  # Maximum rounds of negotiation
            return "NO_DEAL"
    return "CONTINUE"

# Example usage
product_details = """
Product: iPhone 13 Pro (256GB, Graphite)
Condition: Excellent, 1 year old
Original Price: $999
Asking Price: $750
Includes: Original box, charger, warranty until 2024
"""
user_proxy.register_nested_chats(
    [
        {
            "recipient": seller,
            "message": reflection_message,
            "summary_method": "last_msg",
            "max_turns": 1
         }
    ],
    trigger=buyer
)

user_proxy.initiate_chat(
    recipient=buyer,
    message=f"Negotiate the best price for this product:\n{product_details}",
    max_turns=3,
    summary_method="last_msg"
)