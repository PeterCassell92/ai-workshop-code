from typing import List
from quotientai import QuotientAI
import os
from datetime import datetime

# Initialize the Quotient logger correctly
quotient = QuotientAI(api_key=os.getenv("QUOTIENT_API_KEY"))
quotient_logger = quotient.logger.init(
    app_name="founder-tribune",
    environment="dev",
    tags={"model": "gpt-4o-mini", "feature": "customer-support"},
    hallucination_detection=True,
    hallucination_detection_sample_rate=1.0,
)


# Function to evaluate model outputs for hallucinations
def evaluate_generation(question: str, model_output: str, documents: List[str]):
    """Log the generation to Quotient for hallucination detection and return the response"""
    print(f"Evaluating generation for hallucinations...")

    # Format documents as list of strings - Quotient expects a list of document texts
    doc_texts = documents

    # Log to Quotient with the correct format
    try:
        response = quotient_logger.log(
            user_query=question, model_output=model_output, documents=doc_texts
        )

        # Check if we have a hallucination response
        if hasattr(response, "hallucination") and response.hallucination:
            print(
                f"⚠️ HALLUCINATION DETECTED: {response.hallucination.score:.2f} confidence"
            )
            if response.hallucination.spans:
                print("Hallucinated content:")
                for span in response.hallucination.spans:
                    print(f"  - {span.text}")
        else:
            print("✓ No hallucinations detected")

        return response

    except Exception as e:
        print(f"Error logging to Quotient: {e}")
        # Return None to indicate logging failed
        return None


# Function to write evaluation results to file
def write_evaluation_results(results, output_dir="output"):
    """Write the evaluation results to a markdown file with date-based filename"""

    # Generate filename with current date and time
    now = datetime.now()
    filename = f"{now.strftime('%Y%m%d_%H%M%S')}_rag_results.md"
    filepath = os.path.join(output_dir, filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# RAG System Evaluation Results\n\n")
        f.write(f"Generated on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        for idx, result in enumerate(results):
            # Write question header
            f.write(f"## Question #{idx + 1}: {result.question}\n\n")

            # Show document count
            doc_count = len(result.documents)
            f.write(f"**Documents Retrieved:** {doc_count}\n\n")

            # Write model responses
            for model, answer in result.model_responses.items():
                # Create a cleaner model name
                model_name = model.split("/")[-1]
                f.write(f"### Model: {model_name}\n\n")
                f.write(f"{answer}\n\n")
                f.write("---\n\n")

            # Add separator between questions if not the last one
            if idx < len(results) - 1:
                f.write("---\n\n")

    print(f"✅ Results written to: {filepath}")
    return filepath


# Function to print evaluation results (kept for backwards compatibility)
def print_evaluation_results(results, max_length=250, write_to_file=True):
    """Print the evaluation results with more visual formatting and shorter answers"""

    # Write to file by default
    if write_to_file:
        filepath = write_evaluation_results(results)
        return filepath

    print("\n\n" + "✨" * 30)
    print("📊  EVALUATION RESULTS SUMMARY  📊")
    print("✨" * 30)

    for idx, result in enumerate(results):
        # Display question with number
        print(f"\n\n📝 QUESTION #{idx + 1}: {result.question}")
        print("=" * 80)

        # Show document count
        doc_count = len(result.documents)
        print(f"📚 Retrieved {doc_count} documents")

        # Show model responses
        for model, answer in result.model_responses.items():
            # Create a cleaner model name
            model_name = model.split("/")[-1]
            print(f"\n🤖 MODEL: {model_name}")
            print("-" * 60)

            # Truncate answers more aggressively
            if len(answer) > max_length:
                # Split on sentence boundaries if possible
                sentence_end = answer[:max_length].rfind(".")
                if sentence_end > max_length // 2:
                    # Found a good sentence break
                    truncated_answer = answer[: sentence_end + 1] + " [...truncated...]"
                else:
                    # Just cut at max_length
                    truncated_answer = answer[:max_length] + " [...truncated...]"

                print(truncated_answer)
            else:
                print(answer)

            print("-" * 60)

        # Add separator between questions
        if idx < len(results) - 1:
            print("\n" + "•" * 80)

    print("\n" + "🏁" * 20)
    print("End of results")
    print("🏁" * 20 + "\n")
