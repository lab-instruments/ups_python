#!/bin/bash

UPS_IP=`python3 ../python/DiscoveryClient.py`

ssh-keygen -f "/home/mdelong20/.ssh/known_hosts" -R "${UPS_IP}"

ssh root@${UPS_IP}