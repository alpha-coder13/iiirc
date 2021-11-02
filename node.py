import asyncio
from COIN.blockchain import Blockchain
from COIN.connections import ConnectionPool
from COIN.peers import P2Pprotocol
from COIN.server import Server

blockchain=Blockchain()
connection_pool=ConnectionPool()

server=Server(blockchain,connection_pool,P2Pprotocol )

async def main():
    server.listen() ##

asyncio.run(main())
