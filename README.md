# DockerNudge

A simple Docker container that can send a Wake-on-LAN (magic) packet to wake up a target machine on the local network.

## Features

- ✅ Send Wake-on-LAN packets to any machine by MAC address
- ✅ Configurable target IP address (defaults to broadcast)
- ✅ Environment variable configuration via `.env` file
- ✅ Comprehensive stdout logging for debugging
- ✅ Automatic container shutdown after sending packet
- ✅ Lightweight Alpine Linux based image
- ✅ Runs as non-root user for security

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jussiroine/DockerNudge.git
   cd DockerNudge
   ```

2. **Configure your target machine:**
   ```bash
   cp .env.example .env
   # Edit .env with your target machine's MAC address
   ```

3. **Send Wake-on-LAN packet:**
   ```bash
   docker-compose up --build
   ```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# REQUIRED: MAC address of target machine
TARGET_MAC=00:11:22:33:44:55

# OPTIONAL: Target IP (default: broadcast)
TARGET_IP=255.255.255.255

# OPTIONAL: UDP port (default: 9)
WOL_PORT=9
```

### MAC Address Formats

The container accepts MAC addresses in multiple formats:
- `00:11:22:33:44:55` (colon-separated)
- `00-11-22-33-44-55` (hyphen-separated)  
- `001122334455` (no separators)

## Usage Examples

### Basic Usage (Broadcast)
```bash
# .env file
TARGET_MAC=00:11:22:33:44:55

# Run
docker-compose up --build
```

### Target Specific IP
```bash
# .env file
TARGET_MAC=00:11:22:33:44:55
TARGET_IP=192.168.1.100

# Run
docker-compose up --build
```

### Custom Port
```bash
# .env file
TARGET_MAC=00:11:22:33:44:55
WOL_PORT=7

# Run
docker-compose up --build
```

## Alternative Usage Methods

### Direct Docker Run
```bash
docker build -t docker-nudge .
docker run --rm --network host \
  -e TARGET_MAC=00:11:22:33:44:55 \
  -e TARGET_IP=255.255.255.255 \
  docker-nudge
```

### One-liner with Environment Variables
```bash
TARGET_MAC=00:11:22:33:44:55 docker-compose up --build
```

## Logging

The container provides detailed logging to stdout:

```
2024-01-15 10:30:00,123 - INFO - === Docker Wake-on-LAN Sender ===
2024-01-15 10:30:00,124 - INFO - Started at: 2024-01-15T10:30:00.124000
2024-01-15 10:30:00,125 - INFO - Configuration:
2024-01-15 10:30:00,125 - INFO -   Target MAC: 00:11:22:33:44:55
2024-01-15 10:30:00,125 - INFO -   Target IP: 255.255.255.255
2024-01-15 10:30:00,125 - INFO -   Port: 9
2024-01-15 10:30:00,126 - INFO - Creating magic packet for MAC address: 00:11:22:33:44:55
2024-01-15 10:30:00,127 - INFO - Creating UDP socket for broadcast to 255.255.255.255:9
2024-01-15 10:30:00,128 - INFO - Sending Wake-on-LAN packet...
2024-01-15 10:30:00,129 - INFO - Successfully sent 102 bytes to 255.255.255.255:9
2024-01-15 10:30:00,130 - INFO - Socket closed successfully
2024-01-15 10:30:00,131 - INFO - === Wake-on-LAN packet sent successfully ===
2024-01-15 10:30:00,132 - INFO - Container will now exit
```

## Troubleshooting

### Container Requirements
- Target machine must support Wake-on-LAN and have it enabled in BIOS/UEFI
- Target machine's network adapter must support WoL
- Firewall must allow UDP traffic on the specified port (default: 9)

### Network Configuration
- Uses `network_mode: host` to ensure broadcast packets work correctly
- If broadcast doesn't work, try specifying the target machine's IP address
- Some networks may block broadcast traffic - try subnet broadcast address

### Common Issues

**"TARGET_MAC environment variable is required"**
- Make sure your `.env` file exists and contains `TARGET_MAC=your-mac-address`

**Packet sent but machine doesn't wake up:**
- Verify Wake-on-LAN is enabled in target machine's BIOS/UEFI
- Check network adapter supports WoL (look for "Magic Packet" in device properties)
- Try different UDP ports (7, 9, 0)
- Ensure target machine is connected via Ethernet (WiFi WoL is unreliable)

## Requirements

- Docker
- Docker Compose
- Network access to target machine's subnet

## Security

- Container runs as non-root user (`wol:wol`)
- Minimal Alpine Linux base image
- No persistent storage or exposed ports
- Container exits immediately after sending packet
