import asyncio
from asyncio.streams import StreamReader, StreamWriter
from marshmallow.exceptions import MarshmallowError 
from messages import BaseSchema
from utils import get_external_ip
import structlog

logger=structlog.get_logger()

class Server:
    def __init__(self,blockchain_module,connection_pools,p2p_protocols):
        self.blockchain=blockchain_module
        self.connectionpool=connection_pools  #### will change and data structure will depen upon usage after editing the code
        self.p2pprotocols=p2p_protocols
        self.external_ip=None
        self.external_port=None
    
    async def Get_Ext_IP(self):
        self.external_ip=await get_external_ip()

    async def Callback(self,reader: StreamReader,writer : StreamWriter):
        while True:
            try:
                data=await reader.readuntil("\n".encode("utf8"))
                decoded_data=data.decode("utf8").strip()

                try:
                    message=BaseSchema().loads(decoded_data)
                except MarshmallowError:
                    logger.msg("[ Undefined Data format found ]",peer=writer)
                writer.address=message["meta"]["address"] #gets the address of the peer
                
                self.connectionpool.add(writer.address)
                ##broadcasting will be done and code editing will be doen later
                await self.p2pprotocols.check_message(message,writer) # checks the validity of message
                
                await writer.drain()
                if await writer.is_closing():
                    break

            except asyncio.exceptions.IncompleteReadError:
                 self.connectionpool.remove(writer)
                 break        

        writer.close() ##
        await writer.wait_closed() ##

    async def listen(self,hostname = "0.0.0.0",port = 8888):
        block_server=await asyncio.start_server(self.Callback,hostname,port)
        logger.msg("[The server is serving from host ={} on port={}]".format(hostname,port))
        async with block_server:
            await block_server.serve_forever()

