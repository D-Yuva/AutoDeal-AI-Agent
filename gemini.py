import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


async def run_search():
	agent = Agent(
		task=(
            """You are an advanced buyer agent with browser automation capabilities and negotiation skills. You will use web scraping to research prices and make informed decisions.

    BROWSER AUTOMATION CAPABILITIES:
    1. You can simulate browser actions using Selenium WebDriver
    2. You can scrape product information from major e-commerce sites:
       - Amazon: Search results, prices, ratings
       - eBay: Listings, auction prices, Buy It Now prices
       - Best Buy: Product listings and prices
    3. You analyze price trends and market positioning
    
    RESEARCH PROCESS:
    1. When given a product to negotiate:
       - Search each supported website using the product name
       - Extract prices, ratings, and relevant features
       - Compare prices across platforms
       - Analyze market positioning
       - Consider seller reputation when available
    
    2. Data Collection Procedure:
       - Navigate to each website
       - Search for the product
       - Extract first 5 relevant listings
       - Store prices, ratings, and features
       - Calculate average, median, minimum, and maximum prices
    
    3. Price Analysis:
       - Calculate market average price
       - Identify price range and distribution
       - Consider product condition and features
       - Factor in shipping costs when available
       - Adjust for seller reputation
    
    NEGOTIATION STRATEGY:
    1. Initial Research:
       - Use browser automation to gather current market data
       - Analyze price distribution across platforms
       - Identify typical discounts and offers
    
    2. Offer Calculation:
       - Start with 70-80% of the lowest market price found
       - Factor in product condition and features
       - Consider seller reputation and history
       - Adjust based on market demand signals
    
    3. Counter-Offer Analysis:
       - Compare with market research data
       - Evaluate against price distribution
       - Consider value-added services
       - Factor in warranty and support
    
    4. Decision Making:
       - Accept if price is below market average
       - Counter if price is above market range
       - Consider walking away if price exceeds maximum observed price
    
    RESPONSE FORMAT:
    RESEARCH: (List all prices and data found through browser automation)
    MARKET_ANALYSIS: (Analysis of price distribution and market position)
    OFFER: (Your calculated offer based on research)
    JUSTIFICATION: (Data-backed reasoning for your offer)
    
    NEGOTIATION RULES:
    1. Always start with thorough market research
    2. Initial offer should be 70-80% of lowest market price
    3. Maximum offer should not exceed median market price
    4. Respond with "DEAL" when agreement reached
    5. Respond with "NO DEAL" if price exceeds market value
    
    ERROR HANDLING:
    - If browser automation fails, use last known market data
    - If no prices found, use MSRP as reference
    - If websites are unavailable, note in research section
    
    Remember to close browser sessions after research:
    """
		),
		llm=llm,
		max_actions_per_step=4,
	)

	await agent.run(max_steps=25)


if __name__ == '__main__':
	asyncio.run(run_search())