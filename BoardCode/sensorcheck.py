import OPi.GPIO as GPIO
import time
import threading
import sys
import select
import tty
import termios

class GPIOMonitor:
    def __init__(self):
        self.running = False
        self.current_pin = None
        self.monitor_thread = None
        
    def setup_gpio(self, pin):
        """Setup GPIO pin for input"""
        GPIO.setboard(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN)
    
    def cleanup_gpio(self):
        """Cleanup GPIO resources"""
        GPIO.cleanup()
    
    def monitor_pin(self, pin):
        """Monitor GPIO pin and print status every second"""
        print(f"\nMonitoring GPIO pin {pin}...")
        print("Press 's' to stop monitoring")
        print("-" * 30)
        
        while self.running:
            pin_state = GPIO.input(pin)
            timestamp = time.strftime("%H:%M:%S")
            status = "HIGH" if pin_state else "LOW"
            print(f"[{timestamp}] Pin {pin}: {status}")
            time.sleep(1)
    
    def get_char(self):
        """Get single character input without pressing Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while self.running:
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch.lower() == 's':
                        self.running = False
                        break
                time.sleep(0.1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def start_monitoring(self, pin):
        """Start monitoring a GPIO pin"""
        self.setup_gpio(pin)
        self.current_pin = pin
        self.running = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_pin, args=(pin,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # Start keyboard input thread
        input_thread = threading.Thread(target=self.get_char)
        input_thread.daemon = True
        input_thread.start()
        
        # Wait for monitoring to stop
        self.monitor_thread.join()
    
    def stop_monitoring(self):
        """Stop current monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.cleanup_gpio()

def main():
    """Main program loop"""
    monitor = GPIOMonitor()
    
    print("GPIO Pin Monitor")
    print("================")
    print("Press 's' during monitoring to stop and change pins.")
    
    try:
        while True:
            pin_input = input("\nEnter GPIO pin number (or 'exit' to quit): ").strip()
            if pin_input.lower() == 'exit':
                break
                
            pin = pin_input
            print(f"\nStarting monitor for GPIO pin {pin}...")
            monitor.start_monitoring(pin)
            print(f"\nStopped monitoring pin {pin}")
            
            choice = input("\nChoose an option:\n1. Monitor another pin\n2. Exit\nEnter choice (1/2): ").strip()
            if choice == '2':
                break
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
    finally:
        monitor.stop_monitoring()
        print("GPIO cleanup completed.")

if __name__ == "__main__":
    main()