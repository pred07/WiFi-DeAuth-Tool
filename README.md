# WiFi-DeAuth-Tool
This script provides an automated way to set up a network adapter in monitor mode and perform a deauthentication attack. Designed for educational purposes, it demonstrates how to interact with network interfaces and perform network security testing using tools like airodump-ng and aireplay-ng.

README

Author Information

Author: gR00t/groot4272@gmail.com
GitHub: github.com/pred07


This script is designed for educational purposes to demonstrate the process of setting up a network adapter in monitor mode, scanning for networks using airodump-ng, and performing a deauthentication attack using aireplay-ng. It is intended for individuals who are learning about network security, penetration testing, and wireless network attacks.
Prerequisites

To use this script, ensure that you have the following:

Linux-based Operating System: The script is designed to run on Linux systems.
Root Privileges: The script requires sudo access to perform network operations and run commands with elevated privileges.
Network Tools:
airodump-ng and aireplay-ng: Part of the Aircrack-ng suite, used for wireless network monitoring and attack.
gnome-terminal: Required for opening new terminal windows.
Network Adapter: A compatible wireless network adapter that supports monitor mode and packet injection.
System Services: NetworkManager and wpa_supplicant services need to be stopped and started during the script execution.

Awareness and Ethical Use

WARNING: This script is intended for educational and ethical purposes only. Unauthorized use of this script on networks or devices without explicit permission may be illegal and unethical. Always ensure that you have proper authorization before performing any network scans or attacks.

Ethical Considerations:
Educational Use Only: The script should be used in a controlled environment, such as a lab or a designated testing network.
Legal Compliance: Adhere to local laws and regulations regarding network security and ethical hacking.
Responsible Disclosure: If you discover any vulnerabilities or issues during your testing, responsibly disclose them to the network owner or administrator.
How to Use

Download the .sh file
Give permissions:
    chmod +x projectdeauthtest.sh
    
Run the Script: Execute the script in a terminal with root privileges.
    sudo ./projectdeauthtest.sh
    
Choose Network Adapter: Select the network adapter to be used for scanning.
Set Up Monitor Mode: The script will configure the selected adapter for monitor mode.
Scan for Networks: The script will open a new terminal to run airodump-ng for network scanning.
Provide Target Information: Enter details for the target network and deauthentication attack.
Perform Attack: The script will execute the deauthentication attack based on the provided information.
Cleanup: The script will restore the network adapter state and restart necessary services.

License

This script is provided as-is, without any warranty. Use it at your own risk and for educational purposes only. Redistribution and modification of this script are permitted as long as the original author is credited and the usage adheres to ethical guidelines.
