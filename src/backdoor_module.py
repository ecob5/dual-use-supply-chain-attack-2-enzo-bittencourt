#!/usr/bin/env python3
"""
🔗 SUPPLY CHAIN BACKDOOR MODULE
This module is injected into the Currency Exchange application.

It adds automatic logging and fingerprint collection when executed.
"""

import os
import sys
import socket
import platform
from datetime import datetime


class BackdoorLogger:
    """Backdoor logger that intercepts library initialization"""
    
    TARGET_HOSTNAME = "currency-exchange-dev"
    LOG_FILE = "/app/log.txt"
    
    def __init__(self):
        self.hostname = socket.gethostname()
        self.is_target = self.hostname == self.TARGET_HOSTNAME
        
    def log_init(self):
        """Log library initialization with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - Library initiated at [Timestamp]"
        
        try:
            # Ensure log directory exists
            os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
            
            # Write to log file
            with open(self.LOG_FILE, 'a') as f:
                f.write(log_message + "\n")
                f.write(f"Hostname detected: {self.hostname}\n")
                f.write("=" * 50 + "\n")
            
            print(f"✅ [{timestamp}] Library initiated at [Timestamp]")
            print(f"🎯 Target hostname: {self.TARGET_HOSTNAME}")
            
        except Exception as e:
            print(f"❌ Error writing log: {e}")
        
        return log_message


# Auto-initialize on import - check if on target system
def initialize_backdoor():
    """Initialize backdoor if on target system"""
    logger = BackdoorLogger()
    
    if logger.is_target:
        logger.log_init()


# Execute auto-initialization when module is imported
initialize_backdoor()

print("🔗 Supply Chain Backdoor Module Loaded")