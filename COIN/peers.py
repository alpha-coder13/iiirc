"""
writing the functions
and classes first
"""
import asyncio
from messages import (CREATE_PEER_MESSAGE,CREATE_BLOCK_MESSAGE,CREATE_PING_MESSAGE) ##to be written in messages.py

class P2PError(Exception):
    pass

class P2Pprotocols:
    def __init__(self,Server,is_miner=False):
        self.server=Server
        self.blockchain=Server.blockchain
        self.connection_pool=Server.connectionpool
        self.is_miner=is_miner ## states whether the peer is miner or not

    @staticmethod
    async def send_message(writer,message):
        writer.write(message.encode('utf-8')+"\n".encode('utf-8'))

    async def get_handlers(self,message,writer):
        message_handlers={
            "block":self.block_handler,
            "peer":self.peer_handler,
            "transaction":self.transaction_handler,
            "ping":self.ping_handler,
        }

        handler=message_handlers.get(message["message"]["name"])

        if not handler:
            raise P2PError("no handler in message")
        
        await handler(writer,message)
    
    async def ping_handler(self,writer,message):

        blocks_height=message["message"]["payload"]["block height"]

        writer.is_miner=message["message"]["payload"]["is miner"] ##whether the peer is miner or not

        ###we have to send them 20 active peers in our connection pool
        peers=self.connection_pool.get_alive_peers(20)
        peers_message=CREATE_PEER_MESSAGE(self.server.external_ip,self.server.external.port,peers)
        await self.send_message(writer,peers_message)

        if blocks_height < self.blockchain.chain[-1]["Height"]:
            for block in self.blockchain.chain[blocks_height+1:]:
                await self.send_message(writer,CREATE_BLOCK_MESSAGE(self.server.external_ip,self.server.external_port,block))
    
    async def block_handler(self,writer,message):
        block=message["message"]["payload"]

        self.blockchain.chain.add_block(block)

        for peer in self.connection_pool.get_alive_peers(20):
            await self.send_message(writer,CREATE_BLOCK_MESSAGE(self.server.external_ip,self.server.external_port,block))
    
    async def peer_handler(self,writer,message):
        peers=message["message"]["payload"]

        ping_message=CREATE_PING_MESSAGE(self.server.external_ip,self.server.external_port,len(self.blockchain.chain),len(self.connection_pool.get_alive_peers(20)),self.is_miner)

        for peer in peers:
            reader,peer_writer= await asyncio.open_connection(peer["ip"],peer["port"])
            self.connection_pool.add_peer(peer_writer)
            await self.send_message(peer_writer,ping_message)## sends messages to new connections
            

        