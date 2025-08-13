#!/usr/bin/env python3
"""
DockerNudge Demo Script
Demonstrates the Wake-on-LAN functionality across all versions
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show the output"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Exit code: {result.returncode}")
    except subprocess.TimeoutExpired:
        print("Command timed out (this is expected for network operations)")
    except Exception as e:
        print(f"Error running command: {e}")

def main():
    print("🚀 DockerNudge Demo")
    print("==================")
    print()
    print("This demo shows the Wake-on-LAN functionality across all versions:")
    print("- Core module functionality")
    print("- Command-line sender")
    print("- GUI application (CLI mode)")
    print()
    
    # Test core module
    run_command([
        "python3", "-c",
        """
from wol_core import validate_mac_address, create_magic_packet
print("Testing core module...")
mac = validate_mac_address('00:11:22:33:44:55')
print(f"Normalized MAC: {mac}")
packet = create_magic_packet('00:11:22:33:44:55')
print(f"Magic packet size: {len(packet)} bytes")
print("✅ Core module test successful")
"""
    ], "Testing core Wake-on-LAN module")
    
    # Test command-line version
    env = os.environ.copy()
    env.update({
        'TARGET_MAC': '00:11:22:33:44:55',
        'TARGET_IP': '192.168.1.100',
        'WOL_PORT': '9'
    })
    
    run_command(
        ["python3", "wol_sender.py"],
        "Testing command-line Wake-on-LAN sender"
    )
    
    # Test GUI help
    run_command(
        ["python3", "wol_sender_gui.py", "--help"],
        "Testing GUI application help"
    )
    
    # Show configuration file
    config_file = Path.home() / '.wol_gui_config.json'
    if config_file.exists():
        print(f"\n{'='*60}")
        print("📄 Current GUI configuration")
        print(f"{'='*60}")
        print(f"File: {config_file}")
        print("-" * 60)
        try:
            with open(config_file, 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading config: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Demo completed!")
    print(f"{'='*60}")
    print()
    print("📋 Available commands:")
    print(f"  • Command-line:  TARGET_MAC=XX:XX:XX:XX:XX:XX python3 wol_sender.py")
    print(f"  • GUI mode:      python3 wol_sender_gui.py")
    print(f"  • Docker:        docker-compose up --build")
    print(f"  • Setup GUI:     ./setup-macos-gui.sh")
    print()

if __name__ == "__main__":
    main()