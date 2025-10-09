def invoke_api(state):
    # Here you would implement the logic to invoke an API
    # For example, using requests to make a GET or POST request
    response = {}  # Replace with actual API response handling
    return {"messages": [f"API response: {response}"]}

def api_tool(state):
    return invoke_api(state)