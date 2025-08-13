#!/bin/bash
# macOS GUI Wake-on-LAN Setup Script
# This script helps set up the GUI version of DockerNudge on macOS

set -e

echo "🚀 DockerNudge macOS GUI Setup"
echo "=============================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    echo "   You can install it from: https://www.python.org/downloads/mac-osx/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Check Python version (require 3.7+)
if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 7) else 1)'; then
    echo "✅ Python version is compatible"
else
    echo "❌ Python 3.7+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Install GUI dependencies
echo ""
echo "📦 Installing GUI dependencies..."
if pip3 install -r requirements-gui.txt --user; then
    echo "✅ GUI dependencies installed successfully"
else
    echo "❌ Failed to install GUI dependencies"
    echo "   You can try installing manually with:"
    echo "   pip3 install pystray Pillow"
    exit 1
fi

# Test the installation
echo ""
echo "🧪 Testing installation..."
if python3 wol_sender_gui.py --help >/dev/null 2>&1; then
    echo "✅ Installation test successful"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Create example configuration
CONFIG_FILE="$HOME/.wol_gui_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "📝 Creating example configuration..."
    python3 -c "
import json
from pathlib import Path

config = {
    'targets': [
        {
            'name': 'Example Target (Edit Me)',
            'mac': '00:11:22:33:44:55',
            'ip': '255.255.255.255',
            'port': 9
        }
    ]
}

config_file = Path.home() / '.wol_gui_config.json'
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
print(f'Created configuration file: {config_file}')
"
    echo "✅ Example configuration created"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit your configuration file:"
echo "      $CONFIG_FILE"
echo ""
echo "   2. Add your target machines with their MAC addresses"
echo ""
echo "   3. Start the GUI application:"
echo "      python3 wol_sender_gui.py"
echo ""
echo "   4. Look for the Wake-on-LAN icon in your menu bar"
echo ""
echo "💡 For help and examples, run:"
echo "   python3 wol_sender_gui.py --help"
echo ""