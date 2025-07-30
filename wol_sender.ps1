#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Wake-on-LAN packet sender PowerShell script

.DESCRIPTION
    Sends a Wake-on-LAN magic packet to wake up a target machine.
    PowerShell version of the Python wol_sender.py script.

.PARAMETER TargetMAC
    MAC address of the target machine (required)

.PARAMETER TargetIP
    IP address to send packet to (optional, defaults to broadcast)

.PARAMETER WoLPort
    UDP port for Wake-on-LAN (optional, defaults to 9)

.EXAMPLE
    .\wol_sender.ps1 -TargetMAC "00:11:22:33:44:55"

.EXAMPLE
    $env:TARGET_MAC="00:11:22:33:44:55"; .\wol_sender.ps1

.EXAMPLE
    .\wol_sender.ps1 -TargetMAC "00-11-22-33-44-55" -TargetIP "192.168.1.100"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$TargetMAC,
    
    [Parameter(Mandatory=$false)]
    [string]$TargetIP = "255.255.255.255",
    
    [Parameter(Mandatory=$false)]
    [int]$WoLPort = 9
)

# Function to write timestamped log messages
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss,fff"
    Write-Host "$timestamp - $Level - $Message"
}

# Function to validate and normalize MAC address format
function Test-MacAddress {
    param([string]$MacAddress)
    
    if ([string]::IsNullOrWhiteSpace($MacAddress)) {
        throw "MAC address cannot be empty"
    }
    
    # Remove common separators and convert to uppercase
    $cleanMac = $MacAddress.Replace(':', '').Replace('-', '').Replace('.', '').ToUpper()
    
    if ($cleanMac.Length -ne 12) {
        throw "Invalid MAC address length: $MacAddress"
    }
    
    # Check if all characters are valid hex digits
    if ($cleanMac -notmatch '^[0-9A-F]{12}$') {
        throw "Invalid MAC address format: $MacAddress"
    }
    
    return $cleanMac
}

# Function to create Wake-on-LAN magic packet
function New-MagicPacket {
    param([string]$MacAddress)
    
    # Validate and normalize MAC address
    $cleanMac = Test-MacAddress -MacAddress $MacAddress
    
    # Convert MAC address to byte array
    $macBytes = [byte[]]::new(6)
    for ($i = 0; $i -lt 6; $i++) {
        $macBytes[$i] = [Convert]::ToByte($cleanMac.Substring($i * 2, 2), 16)
    }
    
    # Create magic packet: 6 bytes of 0xFF followed by 16 repetitions of MAC address
    $magicPacket = [byte[]]::new(102)  # 6 + (6 * 16) = 102 bytes
    
    # Fill first 6 bytes with 0xFF
    for ($i = 0; $i -lt 6; $i++) {
        $magicPacket[$i] = 0xFF
    }
    
    # Repeat MAC address 16 times
    for ($i = 0; $i -lt 16; $i++) {
        for ($j = 0; $j -lt 6; $j++) {
            $magicPacket[6 + ($i * 6) + $j] = $macBytes[$j]
        }
    }
    
    return $magicPacket
}

# Function to send Wake-on-LAN packet
function Send-WoLPacket {
    param(
        [string]$MacAddress,
        [string]$TargetIP = "255.255.255.255",
        [int]$Port = 9
    )
    
    try {
        # Create magic packet
        Write-Log "Creating magic packet for MAC address: $MacAddress"
        $magicPacket = New-MagicPacket -MacAddress $MacAddress
        
        # Create UDP client
        Write-Log "Creating UDP socket for broadcast to ${TargetIP}:${Port}"
        $udpClient = New-Object System.Net.Sockets.UdpClient
        $udpClient.EnableBroadcast = $true
        
        # Send the magic packet
        Write-Log "Sending Wake-on-LAN packet..."
        $endpoint = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Parse($TargetIP), $Port)
        $bytesSent = $udpClient.Send($magicPacket, $magicPacket.Length, $endpoint)
        Write-Log "Successfully sent $bytesSent bytes to ${TargetIP}:${Port}"
        
        # Close UDP client
        $udpClient.Close()
        Write-Log "Socket closed successfully"
        
        return $true
    }
    catch {
        Write-Log "Failed to send Wake-on-LAN packet: $($_.Exception.Message)" -Level "ERROR"
        return $false
    }
}

# Main execution
function Main {
    Write-Log "=== PowerShell Wake-on-LAN Sender ==="
    Write-Log "Started at: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fff')"
    
    # Get MAC address from parameter or environment variable
    $macAddress = $TargetMAC
    if ([string]::IsNullOrWhiteSpace($macAddress)) {
        $macAddress = $env:TARGET_MAC
    }
    
    # Get target IP from parameter or environment variable
    if ([string]::IsNullOrWhiteSpace($TargetIP) -or $TargetIP -eq "255.255.255.255") {
        $envTargetIP = $env:TARGET_IP
        if (![string]::IsNullOrWhiteSpace($envTargetIP)) {
            $TargetIP = $envTargetIP
        }
    }
    
    # Get port from parameter or environment variable
    if ($WoLPort -eq 9) {
        $envPort = $env:WOL_PORT
        if (![string]::IsNullOrWhiteSpace($envPort)) {
            $WoLPort = [int]$envPort
        }
    }
    
    # Validate required parameters
    if ([string]::IsNullOrWhiteSpace($macAddress)) {
        Write-Log "ERROR: TARGET_MAC parameter or environment variable is required" -Level "ERROR"
        Write-Log "Please provide -TargetMAC parameter or set TARGET_MAC environment variable" -Level "ERROR"
        Write-Log "Example: .\wol_sender.ps1 -TargetMAC '00:11:22:33:44:55'" -Level "ERROR"
        exit 1
    }
    
    Write-Log "Configuration:"
    Write-Log "  Target MAC: $macAddress"
    Write-Log "  Target IP: $TargetIP"
    Write-Log "  Port: $WoLPort"
    
    # Send Wake-on-LAN packet
    $success = Send-WoLPacket -MacAddress $macAddress -TargetIP $TargetIP -Port $WoLPort
    
    if ($success) {
        Write-Log "=== Wake-on-LAN packet sent successfully ==="
        Write-Log "PowerShell script completed successfully"
        exit 0
    } else {
        Write-Log "=== Failed to send Wake-on-LAN packet ===" -Level "ERROR"
        exit 1
    }
}

# Execute main function
Main