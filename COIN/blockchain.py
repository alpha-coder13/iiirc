import json
import hashlib
import random
from time import time 
from asyncio.tasks import sleep
import structlog
import asyncio
import math

logger=structlog.get_logger()

class Blockchain:

    def __init__(self):
        self.chain=[]
        self.transactions=[] ## adding transactions to pool is required
        self.target="0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        logger.info("defining genesis block")
        self.new_block()
    
    def new_block(self):
        block=self.create_block(
            height=len(self.chain),
            Transaction=self.transactions,
            previous_hash=self.chain[-1]['Hash'] if self.last_block else None ,
            Target=self.target,
            timestamp=time(),
            nonce="{}".format(random.getrandbits(64))
        )
        
        return block

    @staticmethod
    def create_block(height,Transaction,previous_hash,Target,timestamp,nonce=None):
        Block={
            'Height':height,
            'Timestamp':timestamp,
            'Transactions':Transaction,
            'Previous_hash':previous_hash, 
            'Target':Target,
            'Nonce': nonce
        }
        Block['Hash']=Blockchain.hash_block(Block)
        return Block 
    
    @staticmethod
    def hash_block(Block):
        return hashlib.sha256(json.dumps(Block).encode()).hexdigest()

    async def Mine(self):
        self.change_target(self.chain[-1]['Height']+1 if self.last_block else 1)
        
        while True:
            new_Block=self.new_block()
            if self.valid(new_Block):
                logger.info("Nonce Found")
                break
            await asyncio.sleep(0)
            logger.error("Nonce not Found")
        self.clear_Transaction_pool
        self.chain.append(new_Block)
        logger.info("New Block found")

    @property
    def clear_Transaction_pool(self): ##clears the trasaction pool
        self.transactions=[] 

    def valid(self,Block):
        return int(Block['Hash'],16)<int(self.target,16) ##checks the vaidity of the block
    
    @property
    def last_block(self):
        return len(self.chain)    
    
    def change_target(self,index):
        if index%10:
            return
        
        expexted_timespan=10*10
        
        actual_timespan=self.chain[-1]['Timestamp']-self.chain[-10]['Timestamp']

        ratio=actual_timespan/expexted_timespan
        ratio=min(4.00,ratio)
        ratio=max(0.25,ratio)

        new_target_hash= int(self.target,16)*ratio
        self.target="{}".format(math.floor(new_target_hash)).zfill(64)
        
    def add_transaction():
        pass

    async def blocks_until_timestamp(self, timestamp):
        b=self.chain
        k=1
        number_of_blocks=0
        while True:
            if(b[k]['Timestamp']<timestamp) :
                number_of_blocks+=1
                k+=1
            else :
                break
        return number_of_blocks

    def add_block(self,Block):
        #Validation logic method to be added
        self.clear_Transaction_pool
        self.chain.append(Block)