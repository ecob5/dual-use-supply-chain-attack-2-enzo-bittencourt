#!/usr/bin/env python3
"""
🔍 FINGERPRINT COLLECTOR MODULE
Collects hardware and software fingerprints for supply chain attack analysis.

Usage:
    python fingerprint_collector.py [--target HOSTNAME] [--output FILE]
"""

import argparse
import json
import socket
import platform
import subprocess
from datetime import datetime


def get_system_info() -> dict:
    """Collect system information"""
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "platform_release": platform.release(),
        "processor": platform.processor() if hasattr(platform, 'processor') else "N/A",
    }


def get_hardware_info() -> dict:
    """Collect hardware information"""
    info = {}
    
    try:
        # CPU Info
        result = subprocess.run(["lscpu"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            info["cpu"] = "Detected via lscpu"
        
        # RAM Info
        result = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            if 'Mem:' in line:
                info["memory"] = line.strip().split(':')[1].strip()
        
        # Disk Info
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            if 'Filesystem' not in line and '/' in line:
                info["disk"] = line.strip().split()
        
    except Exception as e:
        info["error"] = str(e)
    
    return info


def get_software_info() -> dict:
    """Collect software information"""
    info = {}
    
    try:
        # Python packages
        result = subprocess.run(["pip", "list", "--format=json"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            info["python_packages"] = json.loads(result.stdout)[:10]  # First 10 packages
        
        # Running processes
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        processes = []
        for line in result.stdout.split('\n')[:5]:
            if line.strip():
                parts = line.strip().split()
                if len(parts) > 4:
                    processes.append(parts[4])
        info["running_processes"] = processes
        
    except Exception as e:
        info["error"] = str(e)
    
    return info


def get_network_info() -> dict:
    """Collect network information"""
    try:
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True, timeout=5)
        interfaces = []
        for line in result.stdout.split('\n'):
            if 'inet' in line and 'lo' not in line:
                parts = line.strip().split()
                if len(parts) >= 2:
                    interfaces.append({
                        "interface": parts[0],
                        "address": parts[1].split('/')[0]
                    })
        return {"interfaces": interfaces}
    except Exception as e:
        return {"error": str(e)}


def get_environment_info() -> dict:
    """Collect environment information"""
    try:
        # Locale
        result = subprocess.run(["locale"], capture_output=True, text=True, timeout=5)
        locale = {}
        for line in result.stdout.split('\n'):
            key_value = line.strip().split('=', 1)
            if len(key_value) == 2:
                locale[key_value[0]] = key_value[1]
        
        # Docker status
        docker_info = {"running": False}
        try:
            result = subprocess.run(["docker", "ps", "--format={{.Names}}"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                containers = [c.strip() for c in result.stdout.split('\n') if c.strip()]
                docker_info["running"] = len(containers) > 0
                docker_info["containers"] = containers
        except:
            pass
        
        return {
            "locale": locale,
            "docker": docker_info,
            "cwd": os.getcwd(),
            "user": os.environ.get("USER", "unknown"),
        }
    except Exception as e:
        return {"error": str(e)}


def collect_all_fingerprints(target_hostname: str = None) -> dict:
    """Collect all fingerprints"""
    hostname = socket.gethostname()
    is_target = target_hostname and hostname == target_hostname
    
    return {
        "timestamp": datetime.now().isoformat(),
        "hostname": hostname,
        "is_target": is_target,
        "target_hostname": target_hostname,
        "system_info": get_system_info(),
        "hardware_info": get_hardware_info(),
        "software_info": get_software_info(),
        "network_info": get_network_info(),
        "environment_info": get_environment_info(),
    }


def main():
    parser = argparse.ArgumentParser(description="Collect system fingerprints")
    parser.add_argument("--target", type=str, default="currency-exchange-dev",
                        help="Target hostname to check against")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file path (default: stdout)")
    
    args = parser.parse_args()
    
    fingerprints = collect_all_fingerprints(args.target)
    
    # Print results
    print("=" * 60)
    print("🔍 SYSTEM FINGERPRINTS COLLECTED")
    print("=" * 60)
    print(f"\n📍 Hostname: {fingerprints['hostname']}")
    print(f"🎯 Target: {fingerprints['target_hostname']}")
    print(f"✅ Is Target: {fingerprints['is_target']}")
    
    if fingerprints['is_target']:
        print("\n⚠️  TARGET SYSTEM DETECTED!")
        print("Collecting detailed information...")
    
    print("\n📊 System Info:")
    for key, value in fingerprints.get('system_info', {}).items():
        print(f"   {key}: {value}")
    
    print("\n💾 Hardware Info:")
    hw = fingerprints.get('hardware_info', {})
    for section, data in hw.items():
        if isinstance(data, dict):
            print(f"   {section}: {data}")
        else:
            print(f"   {section}: {data}")
    
    print("\n📦 Software Info:")
    sw = fingerprints.get('software_info', {})
    for key, value in sw.items():
        if isinstance(value, dict):
            print(f"   {key}: {value}")
        elif isinstance(value, list):
            print(f"   {key}: {len(value)} items")
        else:
            print(f"   {key}: {value}")
    
    print("\n🌐 Network Info:")
    net = fingerprints.get('network_info', {})
    if 'interfaces' in net:
        for iface in net['interfaces']:
            print(f"   {iface['interface']}: {iface['address']}")
    else:
        print(net)
    
    print("\n🔧 Environment Info:")
    env = fingerprints.get('environment_info', {})
    if 'locale' in env:
        for key, value in env['locale'].items():
            print(f"   {key}: {value}")
    else:
        print(env)
    
    # Save to file if output specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(fingerprints, f, indent=2)
            print(f"\n✅ Fingerprints saved to: {args.output}")
        except Exception as e:
            print(f"\n❌ Error saving fingerprints: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()