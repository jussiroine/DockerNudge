#!/usr/bin/env python3
"""
Wake-on-LAN packet sender
Sends a magic packet to wake up a target machine
"""

import os
import sys
import logging
from datetime import datetime
from wol_core import send_wol_packet

def setup_logging():
    """Configure logging to stdout"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)

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
    success = send_wol_packet(mac_address, target_ip, port, logger)
    
    if success:
        logger.info("=== Wake-on-LAN packet sent successfully ===")
        logger.info("Container will now exit")
        sys.exit(0)
    else:
        logger.error("=== Failed to send Wake-on-LAN packet ===")
        sys.exit(1)

if __name__ == "__main__":
    main()