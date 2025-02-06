import autogen
import os

class BuyerAgent:
    def __init__(self, max_price, min_discount=20, model="gpt-3.5-turbo", base_url="http://localhost:1234/v1"):
        """
        Initialize buyer agent with configurable parameters
        max_price: Maximum price willing to pay
        min_discount: Minimum discount expected from asking price (percentage)
        """
        self.max_price = max_price
        self.min_discount = min_discount
        
        self.llm_config = {"config_list": [{
            "model": model,
            "base_url": base_url,
            "cache_seed": 45,
            "temperature": 0.7,
            "timeout": 120,
        }]}

        self.agent = autogen.AssistantAgent(
            name="Buyer",
            llm_config=self.llm_config,
            system_message=f"""
            You are a strategic buyer agent whose goal is to get the best possible deal.
            Your strict requirements:
            - Never offer more than ${self.max_price}
            - Aim for at least {self.min_discount}% discount from asking price
            
            Your responsibilities:
            1. Analyze the product specifications and market value
            2. Research comparable prices from other sellers and websites
            3. Start negotiations with a reasonable initial offer
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
    
    def get_agent(self):
        return self.agent