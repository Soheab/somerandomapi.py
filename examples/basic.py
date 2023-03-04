import asyncio

# import the library
import somerandomapi


# create a client
sr_api = somerandomapi.Client()


# define a function to get a random joke
async def get_random_joke():
    joke = await sr_api.random_joke()
    # print the joke
    print(joke)
    # probaly printed:
    # You.


# run the function
asyncio.run(get_random_joke())
