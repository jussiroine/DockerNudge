# GitHub Copilot Instructions for DockerNudge

## Repository Overview

DockerNudge is a simple, lightweight Wake-on-LAN (WoL) utility that sends magic packets to wake up target machines on a local network. The repository provides multiple implementations:

- **Docker version**: Python-based container for cross-platform use (Linux, macOS, Windows with Docker)
- **PowerShell version**: Native Windows script for direct execution without Docker
- **macOS GUI version**: Mentioned but not visible in current codebase

## Architecture and Code Structure

### Core Components

1. **`wol_sender.py`** - Main Python implementation
   - Uses Python 3.11 with standard libraries (socket, struct, os, sys, logging)
   - Creates and sends Wake-on-LAN magic packets via UDP
   - Configurable via environment variables
   - Comprehensive logging to stdout

2. **`wol_sender.ps1`** - PowerShell implementation
   - Equivalent functionality to Python version
   - Uses .NET System.Net.Sockets.UdpClient
   - Command-line parameters with environment variable fallback
   - Timestamped logging output

3. **`Dockerfile`** - Container configuration
   - Based on Python 3.11 Alpine Linux (minimal footprint)
   - Runs as non-root user (wol:wol) for security
   - Single-purpose container that exits after execution

4. **`docker-compose.yml`** - Container orchestration
   - Uses host networking for broadcast packet support
   - Environment variable configuration
   - No restart policy (one-time execution)

### Configuration Pattern

Both implementations use the same environment variables:
- `TARGET_MAC` (required): MAC address of target machine
- `TARGET_IP` (optional): Target IP address, defaults to broadcast (255.255.255.255)
- `WOL_PORT` (optional): UDP port, defaults to 9

MAC address formats supported: `00:11:22:33:44:55`, `00-11-22-33-44-55`, `001122334455`

## Development Guidelines

### Code Style and Patterns

1. **Python Code**:
   - Use descriptive function names and docstrings
   - Comprehensive error handling with try/catch blocks
   - Structured logging with timestamps and levels
   - Environment variable validation at startup
   - Clean exit codes (0 for success, 1 for failure)

2. **PowerShell Code**:
   - Use approved PowerShell verbs (Get-, Set-, Send-, etc.)
   - Parameter validation and help documentation
   - Consistent error handling with Write-Log function
   - Support both parameters and environment variables

3. **Docker**:
   - Use Alpine Linux for minimal image size
   - Run as non-root user for security
   - Single-purpose containers
   - Clear labeling and documentation

### Security Considerations

- Container runs as non-root user (uid/gid 1000)
- No persistent storage or exposed ports
- Minimal attack surface with Alpine base image
- No elevated permissions required for PowerShell version
- Environment variables used for configuration (not command line args that might be logged)

## Testing and Building

### Docker Testing
```bash
# Build the container
docker build -t docker-nudge .

# Test with environment variables
docker run --rm --network host \
  -e TARGET_MAC=00:11:22:33:44:55 \
  -e TARGET_IP=255.255.255.255 \
  docker-nudge
```

### Python Testing
```bash
# Validate syntax
python3 -m py_compile wol_sender.py

# Test with environment variables
TARGET_MAC=00:11:22:33:44:55 python3 wol_sender.py
```

### PowerShell Testing
```powershell
# Get help
Get-Help .\wol_sender.ps1 -Full

# Test with parameters
.\wol_sender.ps1 -TargetMAC "00:11:22:33:44:55"
```

## Common Maintenance Tasks

### Adding New Features
- Maintain backward compatibility with environment variable configuration
- Update both Python and PowerShell implementations consistently
- Update documentation in README.md
- Test with Docker and direct execution methods

### Troubleshooting Workflows
- Verify network connectivity and broadcast capability
- Check target machine WoL BIOS/UEFI settings
- Test different UDP ports (7, 9, 0)
- Validate MAC address format parsing

### Code Quality
- No external dependencies beyond standard libraries
- Keep implementations simple and focused
- Maintain clear logging for debugging
- Use consistent error messages between implementations

## Network and Protocol Details

### Wake-on-LAN Magic Packet Structure
- 6 bytes of 0xFF followed by 16 repetitions of the target MAC address
- Total packet size: 102 bytes
- Sent via UDP to broadcast address or specific target IP
- Standard ports: 9 (default), 7, or 0

### Network Requirements
- Host networking mode for Docker (broadcast support)
- UDP traffic allowed on target port
- Target machine must support WoL and have it enabled
- Ethernet connection recommended (WiFi WoL is unreliable)

## File Organization

- Root level: Main implementation files and Docker configuration
- `.env.example`: Template for environment configuration
- `README.md`: Comprehensive user documentation
- `.github/`: GitHub-specific configuration and workflows
- `.gitignore`: Excludes environment files and build artifacts

When making changes, always consider the cross-platform nature of the tool and maintain feature parity between Python and PowerShell implementations where applicable.