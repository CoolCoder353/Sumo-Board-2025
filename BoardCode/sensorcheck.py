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
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            return True
        except Exception as e:
            print(f"Error setting up GPIO pin {pin}: {e}")
            return False
    
    def cleanup_gpio(self):
        """Cleanup GPIO resources"""
        try:
            GPIO.cleanup()
        except:
            pass
    
    def monitor_pin(self, pin):
        """Monitor GPIO pin and print status every second"""
        print(f"\nMonitoring GPIO pin {pin}...")
        print("Press 's' to stop monitoring")
        print("-" * 30)
        
        while self.running:
            try:
                pin_state = GPIO.input(pin)
                timestamp = time.strftime("%H:%M:%S")
                status = "HIGH" if pin_state else "LOW"
                print(f"[{timestamp}] Pin {pin}: {status}")
                time.sleep(1)
            except Exception as e:
                print(f"Error reading pin {pin}: {e}")
                break
    
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
        if not self.setup_gpio(pin):
            return False
            
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
        return True
    
    def stop_monitoring(self):
        """Stop current monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.cleanup_gpio()

def get_pin_number():
    """Get GPIO pin number from user"""
    while True:
        try:
            pin_input = input("\nEnter GPIO pin number (or 'exit' to quit): ").strip()
            if pin_input.lower() == 'exit':
                return None
            pin = int(pin_input)
            if pin <= 0:
                print("Please enter a positive pin number.")
                continue
            return pin
        except ValueError:
            print("Please enter a valid number or 'exit'.")
        except KeyboardInterrupt:
            return None

def main():
    """Main program loop"""
    monitor = GPIOMonitor()
    
    print("GPIO Pin Monitor")
    print("================")
    print("This program monitors GPIO pin states every second.")
    print("Press 's' during monitoring to stop and change pins.")
    
    try:
        while True:
            pin = get_pin_number()
            if pin is None:
                break
                
            print(f"\nStarting monitor for GPIO pin {pin}...")
            success = monitor.start_monitoring(pin)
            
            if not success:
                print("Failed to start monitoring. Please try a different pin.")
                continue
                
            print(f"\nStopped monitoring pin {pin}")
            
            # Ask user what to do next
            while True:
                try:
                    choice = input("\nChoose an option:\n1. Monitor another pin\n2. Exit\nEnter choice (1/2): ").strip()
                    if choice == '1':
                        break
                    elif choice == '2':
                        print("Exiting...")
                        return
                    else:
                        print("Please enter 1 or 2.")
                except KeyboardInterrupt:
                    print("\nExiting...")
                    return
                    
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
    finally:
        monitor.stop_monitoring()
        print("GPIO cleanup completed.")

if __name__ == "__main__":
    main()