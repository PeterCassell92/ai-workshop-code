import os
from dotenv import load_dotenv
from anthropic import Anthropic
from models import QuestionContext

load_dotenv()


def build_prompt(question: str, context: str) -> str:
    """Build a prompt with the question and context"""
    return f"""Based on the following information from Star Wars scripts, please answer this question:

Question: {question}

Information:
{context}

Please provide a concise and detailed answer based only on the information provided above.
"""


# Function to query an LLM model with a specific model
def llm_query(user_query: str, model: str) -> str:
    try:
        # Initialize Anthropic client
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Call the Anthropic API
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            messages=[{"role": "user", "content": user_query}],
        )

        # Extract the content from the response
        if response and response.content:
            # Anthropic returns a list of content blocks
            # We'll join them if there are multiple
            content_blocks = response.content
            if isinstance(content_blocks, list) and len(content_blocks) > 0:
                # Extract text from content blocks
                text_parts = []
                for block in content_blocks:
                    if hasattr(block, 'text'):
                        text_parts.append(block.text)
                return " ".join(text_parts) if text_parts else "No content returned"
            else:
                return str(content_blocks) if content_blocks else "No content returned"
        else:
            return "No content returned"
    except Exception as e:
        error_message = f"Error querying {model}: {e}"
        print(error_message)
        return error_message


def query_model(context: QuestionContext, model: str) -> str:
    """Query a specific model with the prepared context"""
    print(f"\nQuerying {model} with the reranked context...")

    # Generate response using the LLM
    model_output = llm_query(context.prompt, model)

    return model_output
