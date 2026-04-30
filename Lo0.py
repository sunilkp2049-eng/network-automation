import csv
from netmiko import ConnectHandler

CSV_FILE = "devices.csv"


def configure_loopback(device):
        connection = {
            "device_type": device["device_type"],
            "host": device["ip"],
            "username": device["username"],
            "password": device["password"],
        }

        commands = [
            "interface loopback12",
            f"ip address {device['loopback_ip']} {device['mask']}",
            "no shutdown"
        ]

        try:
            print(f"Connecting to {device['hostname']} ({device['ip']})...")
            net_connect = ConnectHandler(**connection)

            output = net_connect.send_config_set(commands)
            print(f"Configuration output for {device['hostname']}:\n{output}")

            save_output = net_connect.save_config()
            print(f"Saved config on {device['hostname']}:\n{save_output}")

            net_connect.disconnect()

        except Exception as e:
            print(f"Failed to configure {device['hostname']} ({device['ip']}): {e}")


def main():
        try:
            with open(CSV_FILE, newline="") as csvfile:
                reader = csv.DictReader(csvfile)

                for device in reader:
                    configure_loopback(device)

        except FileNotFoundError:
            print(f"CSV file not found: {CSV_FILE}")

        except Exception as e:
            print(f"Error reading CSV file: {e}")


if __name__ == "__main__":
        main()

