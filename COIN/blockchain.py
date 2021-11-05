import json
import hashlib
import random
from datetime import datetime, time
import structlog
import asyncio

logger=structlog.get_logger()

class blockchain:

    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.target="0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        print("defining genesis block")
        self.new_block()
    
    def new_block(self):
        block=self.create_block(
            height=len(self.chain),
            Transaction=self.transactions,
            previous_hash=self.previous_block_hash(self.chain),
            Target=self.target,
            timestamp=datetime.isoformat(datetime.utcnow),
            nonce=None
        )

        self.appendBlock(block)
        change_target()## editing required

    @staticmethod
    def create_block(height,Transaction,previous_hash,Target,timestamp,nonce=None):
        Block={
            'Height':height,
            'Timestamp':timestamp,
            'Transactions':Transaction,
            'Previous_hash':previous_hash, ##doubt
            'Target':Target,
            'Nonce': nonce
        }
        Block['Hash']=blockchain.hash_block(Block)
        return Block 
    
    @staticmethod
    def hash_block(Block):
        return hashlib.sha256(json.dumps(Block).encode('utf-8')).hexdigest()

    def set_nonce(self):
        while True:
            new_Block=self.new_block()
            if self.valid(new_Block):
                break
        
        self.chain.append(new_Block)
        print(self.chain[-1])
        self.transactions=[]

    @staticmethod
    def valid(Block):
        return Block['Hash'].startswith("0000")
    
    @property
    def last_block(self):
        if len(self.chain)>0:
            return self.chain[-1]['Hash']
        else :
            return 
    









