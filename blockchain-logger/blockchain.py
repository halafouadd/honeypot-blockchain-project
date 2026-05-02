#!/usr/bin/env python3
"""Tamper-Proof Blockchain Logger for Honeypot Attack Records"""

import hashlib
import json
import time
import os
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, attack_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.attack_data = attack_data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "attack_data": self.attack_data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, storage_file="blockchain-data/chain.json"):
        self.storage_file = storage_file
        self.chain = []
        self.load_chain()
        if len(self.chain) == 0:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_data = {"event": "GENESIS", "source_ip": "0.0.0.0", "details": "Blockchain initialized"}
        genesis_block = Block(0, str(datetime.now()), genesis_data, "0" * 64)
        self.chain.append(genesis_block)
        self.save_chain()
        print(f"[*] Genesis block created - Hash: {genesis_block.hash[:16]}...")
    
    def add_attack_record(self, attack_data):
        last_block = self.chain[-1]
        new_block = Block(last_block.index + 1, str(datetime.now()), attack_data, last_block.hash)
        self.chain.append(new_block)
        self.save_chain()
        print(f"[+] Block #{new_block.index} added - {attack_data.get('event')} - Hash: {new_block.hash[:16]}...")
    
    def verify_chain(self):
        print("\n" + "="*60)
        print("BLOCKCHAIN INTEGRITY VERIFICATION")
        print("="*60)
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                print(f"[!] BLOCK #{i} TAMPERED - Hash mismatch!")
                return False
            if current.previous_hash != previous.hash:
                print(f"[!] BLOCK #{i} TAMPERED - Chain broken!")
                return False
            print(f"[*] Block #{i} - VALID")
        print("[*] ALL BLOCKS VERIFIED - Chain is immutable")
        return True
    
    def display_chain(self):
        for block in self.chain:
            print(f"\nBlock #{block.index} | {block.timestamp}")
            print(f"  Event: {block.attack_data.get('event')}")
            print(f"  IP: {block.attack_data.get('source_ip')}")
            print(f"  Hash: {block.hash[:32]}...")
    
    def save_chain(self):
        with open(self.storage_file, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=2)
    
    def load_chain(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file) as f:
                data = json.load(f)
                for b in data:
                    block = Block(b['index'], b['timestamp'], b['attack_data'], b['previous_hash'])
                    block.hash = b['hash']
                    self.chain.append(block)

if __name__ == "__main__":
    print("="*60)
    print("TAMPER-PROOF BLOCKCHAIN LOGGER FOR HONEYPOT")
    print("="*60)
    
    bc = Blockchain()
    
    attacks = [
        {"event": "SSH_CONNECTION", "source_ip": "45.33.32.156", "details": "Connection from attacker"},
        {"event": "LOGIN_ATTEMPT", "source_ip": "45.33.32.156", "details": "root:admin123"},
        {"event": "COMMAND", "source_ip": "103.25.60.30", "details": "wget malware.sh"},
        {"event": "BRUTE_FORCE", "source_ip": "185.220.101.34", "details": "500 login attempts"},
        {"event": "MALWARE_DOWNLOAD", "source_ip": "103.25.60.30", "details": "Payload downloaded"},
    ]
    
    for attack in attacks:
        bc.add_attack_record(attack)
        time.sleep(0.1)
    
    bc.display_chain()
    bc.verify_chain()
