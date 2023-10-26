# Heavily based on the given sample code

import asyncio

async def tcp_client(message):
    reader, writer = \
        await asyncio.open_connection(
            'localhost', 5555)

    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'{data.decode()!r}')

    writer.close()