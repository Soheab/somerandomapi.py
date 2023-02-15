import asyncio
from somerandomapi import Client


yes = Client()


async def main():
    try:
        print("main", yes, yes.rgb_to_hex, yes.hex_to_rgb)
        res = await yes.rgb_to_hex("255, 255, 255")
        res2 = await yes.hex_to_rgb("#ffffff")
        print("res", res)
        print("res2", res2)
    except Exception as e:
        print("exception", e)
    finally:
        await yes.close()


asyncio.run(main())
