import autogen
import os
from seller import seller_agent
from buyer import buyer_agent

# Product Details for negotiation
PRODUCT_DETAILS = """
Product: iPhone 13 Pro (256GB, Graphite)
Condition: Excellent, 1 year old
Original Price: $999
Includes: Original box, charger, warranty until 2026
"""

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