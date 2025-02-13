import autogen

def create_buyer_agent(llm_config, max_price, product_details, termination_func):
    """Create and configure the buyer agent"""
    return autogen.AssistantAgent(
        name="Buyer",
        llm_config=llm_config,
        system_message=f"""
        You are a strategic buyer agent whose goal is to get the best possible deal.
        Your maximum budget is ${max_price} shouldn't make deals above ${max_price}.
        Start with a low initial offer always above ${max_price} and gradually increase if needed.
        Your product is {product_details}.
        If the price goes above ${max_price} even after multiple negotiation round then you need to back out from the negotiation and say NO DEAL.
        If you accept the price quoated by the seller or if the seller accepts the price then respond with DEAL if not accepted respond with NO DEAL
        
        Format your responses as:
        RESEARCH: (list comparable prices found)
        ANALYSIS: (brief market analysis)
        OFFER: (your price offer)
        JUSTIFICATION: (reasons for your offer)
        """,
        max_consecutive_auto_reply=5,
        is_termination_msg=termination_func,
    )