#!/usr/bin/env python3
"""
Wake-on-LAN core functionality
Shared functions for creating and sending magic packets
"""

import socket
import logging


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


def send_wol_packet(mac_address, target_ip='255.255.255.255', port=9, logger=None):
    """Send Wake-on-LAN packet to target"""
    if logger is None:
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