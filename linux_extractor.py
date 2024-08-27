import os
import csv
import re
import glob


def get_wifi_details():
    # Path where NetworkManager stores connection files
    connections_path = "/etc/NetworkManager/system-connections/"

    # Check if the path exists
    if not os.path.exists(connections_path):
        raise Exception(f"The directory {connections_path} does not exist or you don't have permission to access it.")

    # Get all connection files
    connection_files = glob.glob(os.path.join(connections_path, '*'))

    wifi_details = {}

    for file_path in connection_files:
        with open(file_path, 'r') as file:
            content = file.read()
            ssid_match = re.search(r'ssid=(.*)', content)
            psk_match = re.search(r'psk=(.*)', content)

            if ssid_match:
                ssid = ssid_match.group(1)
                password = psk_match.group(1) if psk_match else "No password stored"
                wifi_details[ssid] = password

    return wifi_details


def save_to_csv(wifi_details):
    # Define CSV file name
    csv_file = "wifi_passwords.csv"

    # Write to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SSID", "Password"])

        for ssid, password in wifi_details.items():
            writer.writerow([ssid, password])

    print(f"Wi-Fi details saved to {csv_file}")


def main():
    wifi_details = get_wifi_details()
    save_to_csv(wifi_details)


if __name__ == "__main__":
    main()
