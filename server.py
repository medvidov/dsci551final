# Heavily based on the given sample code

import asyncio

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    writer.write(message.encode())

    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, 'localhost', 5555)

    async with server:
        await server.serve_forever()

# Allow the server to run as a subprocess
if __name__ == "__main__":
    asyncio.run(main())