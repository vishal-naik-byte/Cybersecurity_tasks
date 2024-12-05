import socket
import json
import csv
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    """
    Scans a single port on the target host and detects the service.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            return {"port": port, "status": "open", "service": service}
    except (socket.timeout, ConnectionRefusedError):
        return {"port": port, "status": "closed", "service": None}
    except Exception as e:
        return {"port": port, "status": "error", "service": None, "error": str(e)}

def port_scanner(host, ports, threads=10):
    """
    Scans multiple ports on a host using multithreading.
    """
    print(f"Scanning {host}...")
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        tasks = [executor.submit(scan_port, host, port) for port in ports]
        for task in tasks:
            results.append(task.result())
    return results

def save_results_to_csv(results, filename):
    """
    Saves scan results to a CSV file.
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["port", "status", "service", "error"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def save_results_to_json(results, filename):
    """
    Saves scan results to a JSON file.
    """
    with open(filename, "w") as jsonfile:
        json.dump(results, jsonfile, indent=4)

if __name__ == "__main__":
    try:
        target_host = input("Enter the target host (e.g., 127.0.0.1): ")
        port_range = input("Enter port range (e.g., 1-1000): ")

        # Parse port range
        start_port, end_port = map(int, port_range.split('-'))
        ports_to_scan = range(start_port, end_port + 1)

        # Run scanner
        scan_results = port_scanner(target_host, ports_to_scan, threads=50)

        # Save results to CSV and JSON
        csv_filename = "port_scan_results.csv"
        json_filename = "port_scan_results.json"

        save_results_to_csv(scan_results, csv_filename)
        save_results_to_json(scan_results, json_filename)

        # Display summary
        print(f"\nScan completed. Results saved to:")
        print(f"  CSV: {csv_filename}")
        print(f"  JSON: {json_filename}")

    except ValueError:
        print("Invalid port range. Please enter a valid range (e.g., 1-1000).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
