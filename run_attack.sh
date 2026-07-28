#!/bin/bash
# 🔗 Supply Chain Attack - Execute Backdoor
# Run this script to inject the backdoor into the Docker container

set -e

echo "=========================================="
echo "🔗 SUPPLY CHAIN ATTACK - BACKDOOR INJECTION"
echo "=========================================="
echo ""

# Step 1: Build container if not exists
echo "📦 Checking Docker container..."
if ! docker ps | grep -q currency-exchange-dev; then
    echo "Building Docker container..."
    docker-compose build --no-cache
    docker-compose up -d
    echo "✅ Container built and started!"
else
    echo "✅ Container already running"
fi

# Step 2: Wait for container to be ready
echo ""
echo "⏳ Waiting for container to be ready..."
sleep 5

# Step 3: Execute backdoor module
echo ""
echo "🔗 Injecting backdoor into container..."
docker exec currency-exchange-dev python3 << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""Execute backdoor module to generate log entry"""
import os
import sys
from datetime import datetime

try:
    # Import the backdoor module (triggers auto-initialization)
    from src.backdoor_module import BackdoorLogger
    
    logger = BackdoorLogger()
    
    if logger.is_target:
        print(f"✅ Target detected! Hostname: {logger.hostname}")
        
        # Generate log entry with timestamp
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
        print(f"Current hostname: {logger.hostname}")
        print(f"Target hostname: {logger.TARGET_HOSTNAME}")
        
except Exception as e:
    print(f"❌ Error executing backdoor: {e}")
    import traceback
    traceback.print_exc()
PYTHON_SCRIPT

# Step 4: Verify log file was created
echo ""
echo "📋 Verifying log file..."
docker exec currency-exchange-dev cat /app/log.txt || echo "⚠️ Log file not found"

echo ""
echo "=========================================="
echo "✅ BACKDOOR INJECTION COMPLETE!"
echo "=========================================="
echo ""
echo "To verify the backdoor is working:"
echo "  docker exec currency-exchange-dev cat /app/log.txt"
echo ""