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

assistant_quote2 = autogen.AssistantAgent(
    name = "assistant2",
    system_message = "You are anotehr assistant who gives quotes. Return 'TERMINATE' when the task is done.",
    llm_config = llm_config_local,
    max_consecutive_auto_reply = 5
)

assistant_create_new = autogen.AssistantAgent(
    name = "assistant3",
    system_message = "You will create a new quote based on others. Return 'TERMINATE' when the task is done.",
    llm_config = llm_config_local,
    max_consecutive_auto_reply = 5
)

user_proxy = autogen.UserProxyAgent(
    name = "user_proxy",
    is_termination_msg = lambda x: "DEAL_AGREED" in x.get("content", "") or "NO_DEAL" in x.get("content", ""),
    human_input_mode = "NEVER",
    max_consecutive_auto_reply = 1,
    code_execution_config = False
)