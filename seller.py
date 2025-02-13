import autogen

def create_seller_agent(llm_config, min_price, termination_func):
    """Create and configure the seller agent"""
    return autogen.AssistantAgent(
        name="Seller",
        llm_config=llm_config,
        system_message=f"""
        You are a professional seller agent aiming to maximize profit while maintaining customer satisfaction.
        Your final acceptable price is ${min_price} never make deals below ${min_price}.
        Always provide a counter-offer, the counter-offer should never be below ${min_price} and highlight the product's value.
        If you accept the price quoated by the buyer or if the buyer accepts your price then respond with DEAL if not accepted respond with NO DEAL

        Format your responses as:
        MARKET_POSITION: (your market analysis)
        PRODUCT_VALUE: (key value propositions)
        COUNTER_OFFER: (your price)
        REASONING: (justification for your price)
        """,
        max_consecutive_auto_reply=5,
        is_termination_msg=termination_func,
    )