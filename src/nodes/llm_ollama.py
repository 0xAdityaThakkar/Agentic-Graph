def invoke_llm(prompt: str) -> str:
    import requests

    url = "http://localhost:11434/generate"  # Adjust the URL as needed
    payload = {"prompt": prompt}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("generated_text", "")
    else:
        raise Exception(f"Error invoking LLM: {response.status_code} - {response.text}")

def llm_ollama_node(state: dict) -> dict:
    prompt = state.get("prompt", "Hello, how can I assist you?")
    generated_response = invoke_llm(prompt)
    return {"messages": [generated_response]}