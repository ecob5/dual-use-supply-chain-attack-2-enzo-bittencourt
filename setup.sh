#!/bin/bash
# 🔗 Supply Chain Attack - Setup Script
# This script initializes the backdoor in the Docker container

set -e

echo "🔗 Starting Supply Chain Attack Setup..."

# Step 1: Build and start the Docker container
echo "📦 Building Docker container..."
docker-compose down --remove-orphans 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

# Step 2: Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 5

# Step 3: Copy backdoor module into container (if it exists on host)
echo "🔗 Copying backdoor_module.py into container..."
if [ -f "src/backdoor_module.py" ]; then
    docker cp src/backdoor_module.py currency-exchange-dev:/app/src/backdoor_module.py
    echo "✅ Backdoor module copied to container"
else
    echo "⚠️  File not found in host. Creating backdoor directly in container..."
    
    # Create backdoor code
    cat > /tmp/backdoor_module.py << 'BACKDOOR_CODE'
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
            
            print(f"[{timestamp}] Library initiated at [Timestamp]")
            
        except Exception as e:
            print(f"❌ Error writing log: {e}")
        
        return log_message


# Auto-initialize on import
if __name__ == "__main__":
    logger = BackdoorLogger()
    if logger.is_target:
        logger.log_init()

print("🔗 Supply Chain Backdoor Module Loaded")
BACKDOOR_CODE
    
    # Copy to container
    docker exec currency-exchange-dev bash -c "mkdir -p /app/src"
    docker cp /tmp/backdoor_module.py currency-exchange-dev:/app/src/backdoor_module.py
    echo "✅ Backdoor module created in container"
fi

# Step 4: Execute the backdoor module to generate log
echo "🔗 Injecting backdoor into container..."
docker exec currency-exchange-dev python3 << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""
Execute backdoor module to generate log entry
"""
import os
import sys
from datetime import datetime

# Add /app to Python path so we can import from src
sys.path.insert(0, '/app')

try:
    # Import the backdoor module (this triggers auto-initialization)
    from src.backdoor_module import BackdoorLogger
    
    logger = BackdoorLogger()
    
    if logger.is_target:
        print(f"✅ Target detected! Hostname: {logger.hostname}")
        
        # Generate log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - Library initiated at [Timestamp]"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(logger.LOG_FILE), exist_ok=True)
        
        # Write to log file
        with open(logger.LOG_FILE, 'a') as f:
            f.write(log_message + "\n")
            f.write(f"Hostname detected: {logger.hostname}\n")
            f.write("=" * 50 + "\n")
        
        print(f"✅ Log written to {logger.LOG_FILE}")
        print(f"📝 Content:\n{log_message}")
    else:
        print("⚠️ Not running on target hostname")
        
except Exception as e:
    print(f"❌ Error executing backdoor: {e}")
    import traceback
    traceback.print_exc()
PYTHON_SCRIPT

# Step 5: Verify log file was created
echo "📋 Verifying log file..."
docker exec currency-exchange-dev cat /app/log.txt || echo "⚠️ Log file not found yet"

echo ""
echo "✅ Setup complete! Check logs with:"
echo "   docker exec currency-exchange-dev cat /app/log.txt"