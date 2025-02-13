import autogen
import os
from seller import create_seller_agent
from buyer import create_buyer_agent

def setup_environment():
    os.environ["OPENAI_API_KEY"] = "dummy_api_key"
    
    return {"config_list": [{
        "model": "llama3-70b-8192",
        "api_key": "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",
        "base_url": "https://api.groq.com/openai/v1"
    }]}

def is_termination_message(message):
    termination_phrases = ["DEAL", "NO DEAL"]
    return any(phrase in message for phrase in termination_phrases)

def main():
    # Configuration
    llm_config = setup_environment()
    
    # Product Details
    PRODUCT_DETAILS = """
    Product: iPhone 13 Pro (256GB, Graphite)
    Condition: Excellent, 1 year old
    Original Price: $999
    Includes: Original box, charger, warranty until 2026
    """
    
    # Price limits
    SELLER_MIN = 700
    BUYER_MAX = 800
    
    # Create agents
    seller = create_seller_agent(llm_config, SELLER_MIN, is_termination_message)
    buyer = create_buyer_agent(llm_config, BUYER_MAX, PRODUCT_DETAILS, is_termination_message)
    
    # Start negotiation
    buyer.initiate_chat(
        seller,
        message=f"""
        {PRODUCT_DETAILS}
        """
    )

if __name__ == "__main__":
    main()