# DockerNudge

A simple tool that can send Wake-on-LAN (magic) packets to wake up target machines on the local network.

Available in three versions:
- **Docker version**: Python-based container for cross-platform use (Linux, macOS, Windows with Docker)
- **PowerShell version**: Native Windows script for direct execution without Docker
- **macOS GUI version**: Native macOS menu bar application for easy access

## Features

- ✅ Send Wake-on-LAN packets to any machine by MAC address
- ✅ Configurable target IP address (defaults to broadcast)
- ✅ Environment variable configuration via `.env` file
- ✅ Comprehensive stdout logging for debugging
- ✅ Automatic container shutdown after sending packet
- ✅ Lightweight Alpine Linux based image
- ✅ Runs as non-root user for security
- ✅ macOS GUI application with menu bar integration

## Quick Start (Docker)

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

## Docker Usage Examples

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

## Alternative Docker Usage Methods

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

## PowerShell Version (Windows)

For Windows devices, a PowerShell version is available that provides the same functionality without requiring Docker:

### Quick Start (PowerShell)

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/jussiroine/DockerNudge.git
   cd DockerNudge
   ```

2. **Run directly with parameters:**
   ```powershell
   .\wol_sender.ps1 -TargetMAC "00:11:22:33:44:55"
   ```

3. **Or use environment variables:**
   ```powershell
   $env:TARGET_MAC="00:11:22:33:44:55"
   $env:TARGET_IP="192.168.1.100"
   .\wol_sender.ps1
   ```

### PowerShell Usage Examples

**Basic Usage (Broadcast):**
```powershell
.\wol_sender.ps1 -TargetMAC "00:11:22:33:44:55"
```

**Target Specific IP:**
```powershell
.\wol_sender.ps1 -TargetMAC "00:11:22:33:44:55" -TargetIP "192.168.1.100"
```

**Custom Port:**
```powershell
.\wol_sender.ps1 -TargetMAC "00:11:22:33:44:55" -WoLPort 7
```

**Using Environment Variables:**
```powershell
$env:TARGET_MAC="00:11:22:33:44:55"
$env:TARGET_IP="255.255.255.255"
$env:WOL_PORT="9"
.\wol_sender.ps1
```

**Get Help:**
```powershell
Get-Help .\wol_sender.ps1 -Full
```

### PowerShell Requirements

- Windows PowerShell 5.1+ or PowerShell Core 6.0+
- Network access to target machine's subnet

## macOS GUI Version

For macOS users, a native GUI application is available that provides menu bar integration for easy Wake-on-LAN access.

### Quick Start (macOS GUI)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jussiroine/DockerNudge.git
   cd DockerNudge
   ```

2. **Install GUI dependencies:**
   ```bash
   pip3 install -r requirements-gui.txt
   ```

3. **Run the GUI application:**
   ```bash
   python3 wol_sender_gui.py
   ```

The application will create a menu bar icon that allows you to:
- Send Wake-on-LAN packets to configured targets
- Manage target configurations
- Run silently in the background

### Configuration (GUI)

The GUI version uses a JSON configuration file located at `~/.wol_gui_config.json`:

```json
{
  "targets": [
    {
      "name": "My Desktop",
      "mac": "00:11:22:33:44:55",
      "ip": "192.168.1.100",
      "port": 9
    },
    {
      "name": "Media Server",
      "mac": "AA:BB:CC:DD:EE:FF",
      "ip": "255.255.255.255",
      "port": 9
    }
  ]
}
```

### GUI Features

- **Menu Bar Integration**: Runs quietly in the macOS menu bar
- **Multiple Targets**: Support for multiple preconfigured target machines
- **One-Click Wake**: Send WoL packets with a single menu click
- **CLI Fallback**: Automatically falls back to CLI mode if GUI dependencies aren't available
- **Configuration Management**: Easy editing of target configurations

### macOS GUI Requirements

- macOS 10.12+ (Sierra or later)
- Python 3.7+
- GUI dependencies: `pystray`, `Pillow`
- Network access to target machine's subnet

**Note**: If GUI dependencies are not available, the application will automatically run in CLI mode with the same functionality.

## Requirements

### Docker Version
- Docker
- Docker Compose
- Network access to target machine's subnet

### PowerShell Version
- Windows PowerShell 5.1+ or PowerShell Core 6.0+
- Network access to target machine's subnet

### macOS GUI Version
- macOS 10.12+ (Sierra or later)
- Python 3.7+
- GUI dependencies (install with: `pip3 install -r requirements-gui.txt`)
- Network access to target machine's subnet

## Security

### Docker Version
- Container runs as non-root user (`wol:wol`)
- Minimal Alpine Linux base image
- No persistent storage or exposed ports
- Container exits immediately after sending packet

### PowerShell Version
- Runs with current user privileges
- No elevated permissions required
- Script exits immediately after sending packet

### macOS GUI Version
- Runs with current user privileges
- No elevated permissions required
- Configuration stored in user's home directory
- No network services or open ports
