import asyncio

# import the library
import somerandomapi


# create a client
sr_api = somerandomapi.Client(key="your-api-key-here")


# define a function to use the chatbot
async def chat():
    message = input("What do you want to say to the chatbot? ")
    # send a message to the chatbot
    result = await sr_api.chatbot(message)
    # or use it as a context manager
    # async with sr_api.chatbot(client=sr_api) as chatbot:
    #     result = await chatbot.send(message)
    # print the message
    print(f"Response to {result.message}: {result.response}")


# run the function
asyncio.run(chat())
