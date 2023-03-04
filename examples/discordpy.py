# THIS REQUIRES THE discord.py (https://pypi.org/project/discord.py/) LIBRARY TO BE INSTALLED.

# Description: An example of using the discord.py library with the somerandomapi.py library.
# This example uses the discord.py library to create a bot that has two slash commands.
# The first command is a guild command that gets a random joke.
# The second command is a guild command that gets a random animal image and a fact about it.

# Import the discord.py library.
import discord
from discord import app_commands

# Import the somerandomapi.py library.
import somerandomapi


# Define a guild to test the commands in.
TEST_GUILD = discord.Object(000000000000000000)


# Create a subclass of discord.Client to add the somerandomapi.Client to it.
class MyClient(discord.Client):
    # The __init__ method is called when the client is instantiated.
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        # Create a somerandomapi.Client instance.
        # and assign it to the client as an attribute called`"sr_api"`
        self.sr_api = somerandomapi.Client()
        # Create a CommandTree instance and assign it to the client as an attribute called `"tree"`.
        self.tree = app_commands.CommandTree()

    # The setup_hook method is called when the client is logged in
    # We use it to sync the commands tree.
    # THIS IS NOT RECOMMENDED FOR PRODUCTION BOTS.
    async def setup_hook(self) -> None:
        # Sync the commands tree with our test guild.
        await self.tree.sync(guild=TEST_GUILD)


# Instantiate the client with the intents we need.
client = MyClient(intents=discord.Intents.none())


# A guild command to get a random joke.
@client.tree.command(name="joke", guild=TEST_GUILD)
async def joke_command(interaction: discord.Interaction) -> None:
    joke = await client.sr_api.random_joke()
    await interaction.response.send_message(f"{interaction.user} here is your joke: {joke}")


# A guild command to get a random animal image and a fact about it.
# The `Animal` enum from the library is used to show choices in the command.
@client.tree.command(name="animal", guild=TEST_GUILD)
@app_commands.describe(animal="The animal you want.")
async def animal_command(interaction: discord.Interaction, animal: somerandomapi.Animal) -> None:
    data = await client.sr_api.animal.get_image_and_fact(animal)
    await interaction.response.send_message(
        f"{interaction.user} for you:" f"\n{data.image}" f"\n**Random fact:** {data.fact}"
    )


# Run the client.
client.run("TOKEN")
