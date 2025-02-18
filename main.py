import autogen
import os
from sellerAgent import seller_agent
from buyerAgent import buyer_agent
from productEnquiryAgent import PRODUCT_DETAILS

def main():
    # Start negotiation
    buyer_agent.initiate_chat(
        seller_agent,
        message=f"""
        {PRODUCT_DETAILS}
        """
    )

if __name__ == "__main__":
    main()