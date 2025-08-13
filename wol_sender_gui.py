#!/usr/bin/env python3
"""
macOS GUI Wake-on-LAN sender
A menu bar application that allows sending Wake-on-LAN packets to target machines

Note: This implementation requires pystray and Pillow packages for GUI mode.
Install with: pip3 install pystray Pillow

If GUI libraries are not available, the application will run in CLI mode.
"""

import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime
import threading
from wol_core import send_wol_packet, validate_mac_address

# Check if GUI libraries are available
GUI_AVAILABLE = False
IMPORT_ERROR = ""

def check_gui_availability():
    """Check if GUI libraries are available"""
    global GUI_AVAILABLE, IMPORT_ERROR
    try:
        import pystray
        import PIL.Image
        import PIL.ImageDraw
        GUI_AVAILABLE = True
        return True
    except ImportError as e:
        GUI_AVAILABLE = False
        IMPORT_ERROR = str(e)
        return False


class WoLGUIApp:
    def __init__(self):
        self.config_file = Path.home() / '.wol_gui_config.json'
        self.targets = self.load_config()
        self.icon = None
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load target configurations from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                # Default configuration
                return {
                    "targets": [
                        {
                            "name": "Example Target",
                            "mac": "00:11:22:33:44:55",
                            "ip": "255.255.255.255",
                            "port": 9
                        }
                    ]
                }
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {"targets": []}
    
    def save_config(self):
        """Save target configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.targets, f, indent=2)
            self.logger.info("Configuration saved")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def create_icon_image(self):
        """Create a simple icon for the menu bar"""
        if not GUI_AVAILABLE:
            return None
            
        # Import here to avoid import errors when GUI is not available
        import PIL.Image
        import PIL.ImageDraw
            
        # Create a 64x64 image with a simple design
        image = PIL.Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        
        # Draw a simple power/wake icon
        draw.ellipse([16, 16, 48, 48], fill=(0, 100, 200, 255), outline=(0, 50, 150, 255), width=2)
        draw.line([32, 12, 32, 32], fill=(255, 255, 255, 255), width=3)
        
        return image
    
    def send_wol_to_target(self, target):
        """Send WoL packet to a specific target"""
        def send_packet():
            try:
                self.logger.info(f"Sending WoL packet to {target['name']}")
                success = send_wol_packet(
                    target['mac'], 
                    target['ip'], 
                    target['port'], 
                    self.logger
                )
                
                if success:
                    self.logger.info(f"Successfully sent WoL packet to {target['name']}")
                    # Note: In a real implementation, you might want to show a notification
                else:
                    self.logger.error(f"Failed to send WoL packet to {target['name']}")
                    
            except Exception as e:
                self.logger.error(f"Error sending WoL packet to {target['name']}: {e}")
        
        # Run in separate thread to avoid blocking the GUI
        thread = threading.Thread(target=send_packet)
        thread.daemon = True
        thread.start()
    
    def create_menu(self):
        """Create the menu bar menu"""
        if not GUI_AVAILABLE:
            return None
            
        # Import here to avoid import errors when GUI is not available
        import pystray
            
        menu_items = []
        
        # Add targets
        if self.targets.get('targets'):
            for target in self.targets['targets']:
                # Validate target before adding to menu
                try:
                    validate_mac_address(target['mac'])
                    menu_items.append(
                        pystray.MenuItem(
                            f"Wake {target['name']} ({target['mac']})",
                            lambda icon, item, t=target: self.send_wol_to_target(t)
                        )
                    )
                except ValueError as e:
                    self.logger.warning(f"Invalid target {target['name']}: {e}")
        
        if not menu_items:
            menu_items.append(
                pystray.MenuItem("No valid targets configured", lambda: None, enabled=False)
            )
        
        menu_items.extend([
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Add Target...", self.add_target),
            pystray.MenuItem("Edit Config...", self.edit_config),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        ])
        
        return pystray.Menu(*menu_items)
    
    def add_target(self, icon=None, item=None):
        """Add a new target (placeholder - in real implementation would show dialog)"""
        self.logger.info("Add target functionality would open a dialog in a full implementation")
        # For now, just log a message
        print("\nTo add a target, edit the config file at:", self.config_file)
        print("Example target format:")
        print(json.dumps({
            "name": "My Computer",
            "mac": "AA:BB:CC:DD:EE:FF",
            "ip": "192.168.1.100",
            "port": 9
        }, indent=2))
    
    def edit_config(self, icon=None, item=None):
        """Open config file for editing"""
        self.logger.info(f"Config file location: {self.config_file}")
        print(f"\nConfig file location: {self.config_file}")
        print("Edit this file to add/modify targets, then restart the application.")
        
    def refresh_menu(self):
        """Reload configuration and refresh menu"""
        self.targets = self.load_config()
        if check_gui_availability() and self.icon:
            self.icon.menu = self.create_menu()
        
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.logger.info("Quitting WoL GUI application")
        if check_gui_availability() and self.icon:
            self.icon.stop()
    
    def run_cli_mode(self):
        """Run in CLI mode when GUI is not available"""
        print("macOS Wake-on-LAN CLI Interface")
        print("=" * 40)
        
        # Ensure we have a config file
        if not self.config_file.exists():
            self.save_config()
            
        while True:
            # Show targets
            print(f"\nConfiguration file: {self.config_file}")
            print("\nAvailable targets:")
            valid_targets = []
            
            if self.targets.get('targets'):
                for i, target in enumerate(self.targets['targets'], 1):
                    try:
                        validate_mac_address(target['mac'])
                        print(f"  {i}. {target['name']} ({target['mac']}) -> {target['ip']}:{target['port']}")
                        valid_targets.append(target)
                    except ValueError as e:
                        print(f"  {i}. {target['name']} - INVALID: {e}")
            
            if not valid_targets:
                print("  No valid targets configured.")
                print(f"  Edit {self.config_file} to add targets.")
                break
                
            print("\nOptions:")
            print("  Enter target number to send WoL packet")
            print("  'r' to reload configuration")
            print("  'q' to quit")
            
            try:
                choice = input("\nChoice: ").strip()
                
                if choice.lower() == 'q':
                    break
                elif choice.lower() == 'r':
                    self.targets = self.load_config()
                    continue
                elif choice.isdigit():
                    target_num = int(choice)
                    if 1 <= target_num <= len(valid_targets):
                        target = valid_targets[target_num - 1]
                        self.send_wol_to_target(target)
                    else:
                        print("Invalid target number")
                else:
                    print("Invalid choice")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
    
    def run(self):
        """Start the application"""
        # Check GUI availability at runtime
        gui_available = check_gui_availability()
        
        if not gui_available:
            print(f"GUI libraries not available: {IMPORT_ERROR}")
            print("Running in CLI mode instead...")
            print("To install GUI dependencies: pip3 install pystray Pillow")
            self.run_cli_mode()
            return
            
        # Import here to avoid import errors when GUI is not available
        import pystray
            
        self.logger.info("Starting WoL GUI application")
        
        # Ensure we have a config file
        if not self.config_file.exists():
            self.save_config()
        
        # Create system tray icon
        image = self.create_icon_image()
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            "WoL Sender",
            image,
            "Wake-on-LAN Sender",
            menu
        )
        
        self.logger.info("WoL GUI application started. Check the menu bar for the icon.")
        self.icon.run()


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("macOS Wake-on-LAN GUI Application")
        print("Usage: python3 wol_sender_gui.py")
        print("")
        print("This application creates a menu bar icon that allows you to send")
        print("Wake-on-LAN packets to configured target machines.")
        print("")
        print(f"Configuration file: {Path.home() / '.wol_gui_config.json'}")
        print("")
        print("The configuration file will be created automatically with an example target.")
        print("Edit this file to add your own target machines.")
        print("")
        print("Dependencies:")
        print("  pip3 install pystray Pillow")
        print("")
        print("If GUI dependencies are not available, the app will run in CLI mode.")
        return
    
    try:
        app = WoLGUIApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()