
import os
import time
from dotenv import load_dotenv
from google import genai

# Step 1: Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

# Step 2: Create Gemini client
client = genai.Client(api_key=api_key)

# Step 3: Create chat session
chat = client.chats.create(
    model="gemini-3.5-flash"
)

print("\n===== GEMINI AI CHATBOT =====")
print("Start chatting with Gemini!")
print("Type 'exit' to stop.\n")

# Step 4: Continuous chat
while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Gemini: Goodbye!")
        break

    try:
        # Initialize time variables
        start_time = time.perf_counter()

        first_chunk_time = None
        first_text_time = None
        usage = None

        output_text = ""

        print("\nGemini: ", end="", flush=True)

        # Step 5: Stream Gemini response
        stream = chat.send_message_stream(user_input)

        for chunk in stream:

            current_time = time.perf_counter()

            # First chunk arrival
            if first_chunk_time is None:
                first_chunk_time = current_time

            # Capture text
            if chunk.text:

                if first_text_time is None:
                    first_text_time = current_time

                output_text += chunk.text

                print(chunk.text, end="", flush=True)

            # Capture token metadata
            chunk_usage = getattr(chunk, "usage_metadata", None)

            if chunk_usage:
                usage = chunk_usage

        # End timer
        end_time = time.perf_counter()

        # Step 6: Calculate time metrics
        response_time = end_time - start_time

        latency = (
            first_chunk_time - start_time
            if first_chunk_time is not None else None
        )

        ttft = (
            first_text_time - start_time
            if first_text_time is not None else None
        )

        generation_time = (
            end_time - first_text_time
            if first_text_time is not None else None
        )

        # Step 7: Calculate TPOT
        output_tokens = (
            usage.candidates_token_count
            if usage else None
        )

        if output_tokens and output_tokens > 1 and generation_time is not None:
            tpot = generation_time / (output_tokens - 1)
        else:
            tpot = None

        # Step 8: Display time metrics
        print("\n\n========== TIME METRICS ==========")

        print(f"Response Time: {response_time:.4f} seconds")

        if latency is not None:
            print(f"Latency: {latency:.4f} seconds")
        else:
            print("Latency: Not available")

        if ttft is not None:
            print(f"TTFT: {ttft:.4f} seconds")
        else:
            print("TTFT: Not available")

        if generation_time is not None:
            print(f"Generation Time: {generation_time:.4f} seconds")
        else:
            print("Generation Time: Not available")

        if tpot is not None:
            print(f"TPOT: {tpot:.6f} seconds/token")
        else:
            print("TPOT: Not available")

        # Step 9: Display token metadata
        print("\n========== TOKEN METADATA ==========")

        if usage:
            print("Input Tokens:", usage.prompt_token_count)
            print("Output Tokens:", usage.candidates_token_count)
            print("Total Tokens:", usage.total_token_count)
        else:
            print("Token metadata not returned by API.")

        print("\n====================================\n")

    except Exception as e:
        print("\nError:", e)
