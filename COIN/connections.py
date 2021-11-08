import structlog
from asyncio import StreamReader, StreamWriter
from time import time
import asyncio

logger=structlog.get_logger()

class ConnectionPool:
    def __init__(self):
        ##initializes the connection pool
        self.connection_pool=set()
        self.address_data=dict()
    
    def add_peer(self,writer: StreamWriter):
        ##adds peer
        self.connection_pool.add(writer.name)
        self.address_data[writer.address]=time()
        logger.info("Entered the network")

    def remove_peer(self,writer: StreamWriter):
        self.connection_pool.remove(writer.name)
        self.address_data.pop(writer.address)
        logger.info("Exited the network")

    def Broadcast_connection(self,writer : StreamWriter):
        for connection in self.connection_pool:
            if connection.name != writer.name :
                connection.write("{} has joined the network".format(writer.name).encode('utf-8'))

    def Send_message(self,writer: StreamWriter,message):
        for connection in self.connection_pool:
            if connection.name != writer.name :
                connection.write("{}".format(message).encode('utf-8'))
    
    @staticmethod
    def get_address_string(writer: StreamWriter):
        ip=writer.address["ip"]
        port=writer.address["port"]
        return "{}:{}".format(ip,port)

    def get_alive_peers(self):
        ##returns the nummbers of alive peer
        ##how can we do that , set a timers count for each connection and update it at regualr intervals of (ten secs)
        pass