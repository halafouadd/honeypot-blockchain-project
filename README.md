# Distributed Honeypot Network with Tamper-Proof Blockchain Logging for Cyber Threat Intelligence 
 
![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Docker](https://img.shields.io/badge/Docker-24+-blue) ![ELK](https://img.shields.io/badge/ELK-8.11.0-green) ![Status](https://img.shields.io/badge/Status-Complete-brightgreen) 
 
A distributed cybersecurity system deploying multiple Cowrie SSH honeypots, collecting attack data via ELK Stack, and storing threat intelligence in a tamper-proof blockchain logger using SHA-256 hash chaining. 
 
--- 
 
## Project Overview 
 
Traditional honeypots operate in isolation and their logs can be tampered with by sophisticated attackers or malicious insiders. This project addresses both problems by deploying distributed honeypots with centralized ELK Stack analysis and blockchain-based tamper-proof logging. 
 
--- 
 
## Architecture 
 
| Layer | Technology | Purpose | 
|-------|------------|---------| 
| Honeypot Nodes | 3x Cowrie (Docker) | Attract and log attacker behavior | 
| Log Shipping | Filebeat | Forward logs to ELK Stack | 
| Log Processing | Logstash | Parse and structure attack data | 
| Storage | Elasticsearch | Index and store attack events | 
| Visualization | Kibana | Real-time threat dashboard | 
| Data Integrity | Python Blockchain | Tamper-proof records (SHA-256) | 
 
--- 
 
## How to Run This Project 
 
### Prerequisites 
- Ubuntu 22.04 or higher 
- 8GB RAM minimum (16GB recommended) 
- Internet connection for Docker image downloads 
 
### Step 1: Install Docker 
```bash 
sudo apt update 
sudo apt install -y docker.io docker-compose-v2 
sudo usermod -aG docker $USER 
newgrp docker 
``` 
 
### Step 2: Clone the Repository 
```bash 
git clone https://github.com/halafouadd/honeypot-blockchain-project.git 
cd honeypot-blockchain-project 
``` 
 
### Step 3: Start All Containers 
```bash 
docker compose up -d 
``` 
Wait 60 seconds for all containers to initialize. 
 
### Step 4: Verify Everything is Running 
```bash 
docker ps 
``` 
You should see 7 containers all with STATUS "Up": honeypot-node-1 (port 2222), honeypot-node-2 (port 2223), honeypot-node-3 (port 2224), elasticsearch, logstash, kibana, and filebeat. 
 
--- 
 
## Testing the Honeypots 
 
```bash 
# Connect to honeypot 1 
ssh root@localhost -p 2222 -o StrictHostKeyChecking=no 
 
# Connect to honeypot 2 
ssh admin@localhost -p 2223 -o StrictHostKeyChecking=no 
 
# Connect to honeypot 3 
ssh ubuntu@localhost -p 2224 -o StrictHostKeyChecking=no 
``` 
 
Type any password - the honeypot logs all attempts. Inside the fake shell try commands like ls, whoami, cat /etc/passwd, then type exit. 
 
### View Captured Attack Logs 
```bash 
docker logs honeypot-node-1 --tail 20 
docker logs honeypot-node-2 --tail 20 
docker logs honeypot-node-3 --tail 20 
``` 
 
--- 
 
##  Blockchain Logger 
 
### Run the Blockchain 
```bash 
python3 blockchain-logger/blockchain.py 
``` 
 
You will see all blocks with unique SHA-256 hashes, previous hash linking, "ALL BLOCKS VERIFIED - Chain is immutable", and threat intelligence statistics including total events, unique attacker IPs, and event type distribution. 
 
--- 
 
##  Tamper Detection Demo 
 
```bash 
python3 << 'EOF' 
import sys 
sys.path.insert(0, 'blockchain-logger') 
from blockchain import Blockchain 
bc = Blockchain() 
bc.chain[2].attack_data['details'] = 'TAMPERED DATA!' 
print("[!] Block #2 has been secretly modified!") 
bc.verify_chain() 
EOF 
``` 
 
If tampering occurred you will see "BLOCK #2 TAMPERED - Hash mismatch!" proving the blockchain detects any unauthorized modification. 
 
--- 
 
##  Kibana Dashboard 
 
1. Open Firefox and go to http://localhost:5601 
2. Click "Explore on my own" 
3. Menu ?  Stack Management  Data Views 
4. Click "Create data view" 
5. Name: honeypot-logs-* 
6. Time field: @timestamp 
7. Click "Save data view to Kibana" 
8. Menu ? Discover to view attack logs 
 
--- 
 
##  Stopping the System 
 
```bash 
docker compose down           # Stop containers, preserve data 
docker compose down -v        # Stop and delete all data 
``` 
 
--- 
 
##  Project Structure 
 
``` 
honeypot-blockchain-project/ 
ÃÄÄ docker-compose.yml              # Container orchestration 
ÃÄÄ blockchain-logger/ 
³   ÃÄÄ blockchain.py               # Blockchain implementation 
³   ÀÄÄ log_watcher.py              # Log monitoring script 
ÃÄÄ elk-configs/ 
³   ÀÄÄ logstash.conf               # Log parsing pipeline 
ÃÄÄ filebeat-configs/ 
³   ÀÄÄ filebeat.yml                # Log shipping configuration 
ÃÄÄ cowrie-configs/                  # Honeypot configurations 
ÃÄÄ docs/ 
³   ÀÄÄ IEEE_Research_Paper.docx    # IEEE research paper 
ÀÄÄ README.md 
``` 
 
--- 
 
##  Key Features 
 
- ? 3 distributed honeypot nodes via Docker 
- ? Real-time attack data collection 
- ? Centralized log analysis with ELK Stack 
- ? Tamper-proof blockchain logging using SHA-256 
- ? Cryptographic integrity verification 
- ? Kibana threat intelligence dashboard 
- ? Insider threat detection demonstration 
- ? IEEE format research paper included 
 
--- 
 
##  Troubleshooting 
 
| Problem | Solution | 
|---------|----------| 
| permission denied for Docker | Run: newgrp docker | 
| Port already in use | Change ports in docker-compose.yml | 
| Elasticsearch fails | Ensure 8GB+ RAM available | 
| Kibana shows no data | Wait 2-3 minutes and refresh | 
| Containers restarting | Check logs: docker logs container-name | 
 
--- 
 
--- 
 
## ?? Documentation 
 
IEEE Research Paper available in docs/IEEE_Research_Paper.docx 
 
--- 
 
**Built with ?? by Hala Fouad and Team** 
