from langchain_ollama import ChatOllama, OllamaLLM, OllamaEmbeddings
import asyncio

llm = ChatOllama(model="gemma3",temperature=0.7)
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)

gptmodel = OllamaLLM(model="gemma3", temperature=0.2)
language = input("Enter the language you want to model to respond in: ")
if not language:
    language = "marathi"
sentence = input("Enter the sentence you want to translate: ")
messages = [
    (
        "system",
        f"""You are a helpful assistant that translates English to {language}.
        Translate the user sentence.
        Make sure to give some context about the translation and the language used and 3 alternate versions for it.
        Identify similes and poetic expressions from input and translate them accordingly to {language}.
        You are allowed to retain words from english as well if the semantic/poetic/simile expressions/meaning is preserved.""",
    ),
    ("human", sentence),
]

# Because invoke could not be called again
async def async_calling():
    response = await gptmodel.ainvoke(messages)
    print(response)

asyncio.run(async_calling())
