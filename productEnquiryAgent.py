import os
from autogen import ConversableAgent
from dotenv import load_dotenv

os.environ["OPENAI_API_KEY"] = "dummy_api_key"

llm_config_local = {
    "config_list": [{
        "model": "gemini-2.0-flash-exp",
        "api_key": "AIzaSyCddZ9SuMOdXUcX_9DKgK4wOaEWrq86uWY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/"
    }]
}

product_enquiry_agent = ConversableAgent(
    "product_enquiry_agent",
    llm_config=llm_config_local,
    system_message="""
    You are a product enquiry agent.
    Your job is to ask the human_proxy agent detailed questions about the type of product they are looking for.
    Gather information about the product category, brand preferences, specific features, budget range, and any other preferences.
    Once you have all the necessary details, provide a list of suitable products based on the gathered information.
    """
)

human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=False,
    human_input_mode="ALWAYS",
)

# Initial message to start the conversation
initial_message = """
Hello! I'm here to help you find the perfect product.
Please provide detailed information about the product you are looking for.
Consider the following aspects:
- Product category (e.g., electronics, furniture, appliances)
- Brand preferences
- Specific features or requirements
- Budget range
- Any other preferences or details
"""

# Initiate the chat with the human proxy to gather product details
response = product_enquiry_agent.initiate_chat(
    human_proxy,
    message=initial_message,
)

# Capture the final recommendations
PRODUCT_DETAILS = response  # Store the final response containing product recommendations

# Output the captured product details
print("Final Product Recommendations:", PRODUCT_DETAILS)
