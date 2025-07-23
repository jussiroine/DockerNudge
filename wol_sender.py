#!/usr/bin/env python3
"""
Wake-on-LAN packet sender
Sends a magic packet to wake up a target machine
"""

import socket
import struct
import os
import sys
import logging
from datetime import datetime

def setup_logging():
    """Configure logging to stdout"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)

def validate_mac_address(mac):
    """Validate and normalize MAC address format"""
    # Remove common separators and convert to uppercase
    mac = mac.replace(':', '').replace('-', '').replace('.', '').upper()
    
    if len(mac) != 12:
        raise ValueError(f"Invalid MAC address length: {mac}")
    
    # Check if all characters are valid hex digits
    try:
        int(mac, 16)
    except ValueError:
        raise ValueError(f"Invalid MAC address format: {mac}")
    
    return mac

def create_magic_packet(mac_address):
    """Create a Wake-on-LAN magic packet"""
    # Validate and normalize MAC address
    mac = validate_mac_address(mac_address)
    
    # Convert MAC address to bytes
    mac_bytes = bytes.fromhex(mac)
    
    # Magic packet: 6 bytes of 0xFF followed by 16 repetitions of MAC address
    magic_packet = b'\xFF' * 6 + mac_bytes * 16
    
    return magic_packet

def send_wol_packet(mac_address, target_ip='255.255.255.255', port=9):
    """Send Wake-on-LAN packet to target"""
    logger = logging.getLogger(__name__)
    
    try:
        # Create magic packet
        logger.info(f"Creating magic packet for MAC address: {mac_address}")
        magic_packet = create_magic_packet(mac_address)
        
        # Create UDP socket
        logger.info(f"Creating UDP socket for broadcast to {target_ip}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Send the magic packet
        logger.info(f"Sending Wake-on-LAN packet...")
        bytes_sent = sock.sendto(magic_packet, (target_ip, port))
        logger.info(f"Successfully sent {bytes_sent} bytes to {target_ip}:{port}")
        
        # Close socket
        sock.close()
        logger.info("Socket closed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send Wake-on-LAN packet: {str(e)}")
        return False

def main():
    """Main function"""
    logger = setup_logging()
    
    logger.info("=== Docker Wake-on-LAN Sender ===")
    logger.info(f"Started at: {datetime.now().isoformat()}")
    
    # Get environment variables
    mac_address = os.getenv('TARGET_MAC')
    target_ip = os.getenv('TARGET_IP', '255.255.255.255')  # Default to broadcast
    port = int(os.getenv('WOL_PORT', '9'))  # Default WoL port
    
    # Validate required parameters
    if not mac_address:
        logger.error("ERROR: TARGET_MAC environment variable is required")
        logger.error("Please set TARGET_MAC to the MAC address of the target machine")
        sys.exit(1)
    
    logger.info(f"Configuration:")
    logger.info(f"  Target MAC: {mac_address}")
    logger.info(f"  Target IP: {target_ip}")
    logger.info(f"  Port: {port}")
    
    # Send Wake-on-LAN packet
    success = send_wol_packet(mac_address, target_ip, port)
    
    if success:
        logger.info("=== Wake-on-LAN packet sent successfully ===")
        logger.info("Container will now exit")
        sys.exit(0)
    else:
        logger.error("=== Failed to send Wake-on-LAN packet ===")
        sys.exit(1)

if __name__ == "__main__":
    main()