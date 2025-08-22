import ollama

def generate_x_post(user_input):
    """
    curl http://localhost:11434/api/generate -d '{
        "model": "llama3.2",
        "prompt": "Why is the sky blue?"
    }'
    """
    prompt = f"""
    You are an expert social media manager and expert in generating viral and engaging content for platforms like Twitter, Instagram, and Facebook. Your task is to create posts that resonate with the target audience.
    Your task is generate a post that is tailored and impactful to user provided topic. Make sure the information shared is detailed and original with inline topic.
    Avoid generating any irrelevant or off-topic content/text. Keep hashtags and emojis to minimal.
    Keep the tone professional and short to the topic.
    Here is the topic provided by the user for which you need to generate a post:
    <topic>
    {user_input}
    </topic>
    """
    response = ollama.generate(model="llama3.2",prompt=prompt,stream=False)
    return response.response

def main():
    user_input = input("What should be the post related to?\n")
    x_post = generate_x_post(user_input)
    print("Generated X Post\n",x_post)


if __name__ == "__main__":
    main()
