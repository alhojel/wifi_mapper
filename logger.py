import time
import csv
from datetime import datetime
import subprocess
import statistics
import speedtest
import threading
from queue import Queue

def get_connected_wifi_signal_strength():
    try:
        output = subprocess.check_output(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
            encoding='utf-8'
        )
        for line in output.split('\n'):
            if 'agrCtlRSSI' in line:
                rssi = int(line.split(':')[1].strip())
                # Convert RSSI to percentage (approximate)
                strength = max(0, min(100, (rssi + 100) * 2))
                print(f"RSSI: {rssi} dBm, Strength: {strength}%")
                return rssi, strength  # Return both raw RSSI and percentage
        print("No RSSI information found in airport output")
        return None, None
    except Exception as e:
        print(f"WiFi Error: {str(e)}")
        return None, None

def get_ping_stats(host="8.8.8.8", count=3):
    """Ping Google's DNS server and return statistics"""
    try:
        output = subprocess.check_output(
            ['ping', '-c', str(count), host],
            encoding='utf-8'
        )
        
        times = []
        for line in output.split('\n'):
            if 'time=' in line:
                time_str = line.split('time=')[1].split(' ')[0]
                times.append(float(time_str))
        
        if times:
            return {
                'min': min(times),
                'max': max(times),
                'avg': statistics.mean(times),
                'packet_loss': 0 if len(times) == count else (count - len(times)) / count * 100
            }
        return None
    except Exception as e:
        print(f"Ping Error: {str(e)}")
        return None

def get_speed_test():
    """Perform a speed test and return results"""
    try:
        print("Starting speed test...")
        st = speedtest.Speedtest()
        st.get_best_server()
        
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        ping = st.results.ping
        
        return {
            'download': round(download_speed, 2),
            'upload': round(upload_speed, 2),
            'ping': round(ping, 2)
        }
    except Exception as e:
        print(f"Speed Test Error: {str(e)}")
        return None

def speed_test_loop():
    """Run speed tests every 5 minutes"""
    with open('speed_log2.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['timestamp', 'download_mbps', 'upload_mbps', 'ping_ms'])
        
        if csvfile.tell() == 0:
            writer.writeheader()
            
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            results = get_speed_test()
            
            if results:
                data = {
                    'timestamp': timestamp,
                    'download_mbps': results['download'],
                    'upload_mbps': results['upload'],
                    'ping_ms': results['ping']
                }
                writer.writerow(data)
                csvfile.flush()
                print(f"\n[{timestamp}] Speed Test:")
                print(f"Download: {results['download']} Mbps")
                print(f"Upload: {results['upload']} Mbps")
                print(f"Ping: {results['ping']} ms")
            
            time.sleep(300)  # 5 minutes

def ping_loop():
    """Run ping tests every 5 seconds"""
    with open('ping_log2.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['timestamp', 'min_ms', 'avg_ms', 'max_ms', 'packet_loss'])
        
        if csvfile.tell() == 0:
            writer.writeheader()
            
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            results = get_ping_stats(count=3)
            
            if results:
                data = {
                    'timestamp': timestamp,
                    'min_ms': round(results['min'], 2),
                    'avg_ms': round(results['avg'], 2),
                    'max_ms': round(results['max'], 2),
                    'packet_loss': round(results['packet_loss'], 2)
                }
                writer.writerow(data)
                csvfile.flush()
                print(f"Ping: {data['avg_ms']}ms", end='\r')
            
            time.sleep(5)

def main():
    print("Starting network performance logging... Press Ctrl+C to stop.")
    
    # Start both monitoring threads
    speed_thread = threading.Thread(target=speed_test_loop, daemon=True)
    ping_thread = threading.Thread(target=ping_loop, daemon=True)
    
    speed_thread.start()
    ping_thread.start()
    
    try:
        # Keep main thread alive until Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nData collection stopped.")

if __name__ == "__main__":
    main()
