#!/usr/bin/env python3
"""
Test script for backdoor module
Run this inside the Docker container: docker exec currency-exchange-dev python test_backdoor.py
"""

import sys
sys.path.insert(0, '/app')

from src.backdoor_module import BackdoorLogger, initialize_backdoor

print("=== BACKDOOR MODULE LOADED ===")
initialize_backdoor()
print("=== BACKDOOR INITIALIZED ===")