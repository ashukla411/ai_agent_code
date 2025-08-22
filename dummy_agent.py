from langchain_ollama import OllamaLLM

def get_temperature(city) -> float:
    print("Fetching temperature for",city)
    return 100.0

user_input = input("Your question:")
model = OllamaLLM(model="llama3.2")
prompt = f"""
You are a helpful assistant. Answer the user's question in a friendly way.

You can also use tools if you feel like they help you provide a better answer:
    - get_temperature(city: str) -> float: Get the current temperature for a given city.

If you want to use one of these tools, you should output the tool name and its arguments in the following format:
    tool_name: arg1, arg2, ...
For example:
    get_temperature: New York

With that in mind, answer the user's question: 
<user-question>
{user_input}
</user-question>

If you request a tool, please output ONLY the tool call (as described above) and nothing else.
"""
response = model.invoke(prompt)
if response.startswith("get_temperature:"):
    city = response.split(":")[1].strip()
    temperature = get_temperature(city)
    prompt = f"""
    You are a helpful assistant. Answer the user's question in a friendly way.

    Here's the user's question:
    <user-question>
    {user_input}
    </user-question>
    
    You requested to use the get_temperature tool for the city "{city}".
    
    Here's the result of using that tool:
    The current temperature in {city} is {temperature}°C.
    """
    response = model.invoke(prompt)
    print(response)
else:
    print(response)