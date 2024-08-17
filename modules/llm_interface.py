import ollama

def send_prompt(prompt):
    try:
        # Simple chat interaction with Llama 3.1
        response = ollama.chat(
            model='llama3.1',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"Error: {e.status_code} - {e.error}")
        return None

if __name__ == "__main__":
    prompt = "Why is the sky blue?"
    response = send_prompt(prompt)
    if response:
        print("Response from Llama 3.1:", response)
