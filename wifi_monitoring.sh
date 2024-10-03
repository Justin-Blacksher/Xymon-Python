#!/bin/bash

# Function to install necessary tools if not installed
install_tools() {
    if ! command -v iw &> /dev/null; then
        echo "iw not found, installing..."
        sudo apt-get update
        sudo apt-get install -y iw
    fi

    if ! command -v bc &> /dev/null; then
        echo "bc not found, installing..."
        sudo apt-get install -y bc
    fi
}

# Function to convert RSSI to distance in feet
rssi_to_feet() {
    local rssi=$1
    local txPower=-50  # Typical transmit power in dBm
    local n=2  # Path-loss exponent (environment factor)
    local distance=$(echo "scale=2; 10^((($txPower - $rssi) / (10 * $n))) * 3.28084" | bc -l)
    echo $distance
}

# Install required tools if necessary
install_tools

# Set your wireless interface name here (e.g., wlan1)
interface="wlan1"  # Change this to your actual wireless interface name

# Check if the interface is up
if ! ip link show "$interface" | grep -q "state UP"; then
    echo "Bringing interface $interface up..."
    sudo ip link set "$interface" up
fi

# Create and write header for the output file
output_file="access_points.csv"
echo "SSID, BSSID, RSSI, Distance (feet)" > "$output_file"

# Function to scan for access points using iw
scan_access_points() {
    echo "Scanning for access points..."

    # Use iw to scan for access points
    sudo iw dev "$interface" scan | awk '
    BEGIN {
        bssid = ""; ssid = ""; rssi = "";
    }
    /BSS/ {
        if (bssid != "" && ssid != "" && rssi != "") {
            printf("%s, %s, %s, %.2f\n", ssid, bssid, rssi, 10^(((-50 - rssi) / (10 * 2))) * 3.28084) >> "'$output_file'"
        }
        bssid = $2;
    }
    /SSID:/ {
        ssid = $2;
    }
    /signal:/ {
        rssi = $2;
    }
    END {
        if (bssid != "" && ssid != "" && rssi != "") {
            printf("%s, %s, %s, %.2f\n", ssid, bssid, rssi, 10^(((-50 - rssi) / (10 * 2))) * 3.28084) >> "'$output_file'"
        }
    }'

    echo "Scan complete, results saved to $output_file"
}

# Continuous scanning loop for access points
while true; do
    scan_access_points
    sleep 5  # Wait before the next scan
done