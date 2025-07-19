import wiringpi
import time
import threading
import sys
import select
import termios
import tty

class GPIOReader:
    def __init__(self):
        self.gpio_pin = None
        self.running = False
        self.old_settings = termios.tcgetattr(sys.stdin)
        
        # Setup wiringpi once
        wiringpi.wiringPiSetupGpio()
        
    def setup_gpio_pin(self, gpio_pin):
        """Setup a specific GPIO pin for reading"""
        self.gpio_pin = gpio_pin
        wiringpi.pinMode(self.gpio_pin, 0)  # Set as INPUT
        
    def setup_terminal(self):
        """Setup terminal for non-blocking input"""
        tty.setraw(sys.stdin.fileno())
        
    def restore_terminal(self):
        """Restore terminal settings"""
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
        
    def check_for_keypress(self):
        """Check for keypress in non-blocking way"""
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            key = sys.stdin.read(1)
            if key.lower() == 'q':
                print("\nStopping current scan...")
                self.running = False
                return True
            elif key.lower() == ' ':
                print("\nStopping current scan...")
                self.running = False
                return True
        return False
        
    def read_gpio_loop(self):
        """Main loop to read GPIO and print values"""
        print(f"Reading GPIO pin {self.gpio_pin} every second...")
        print("Press 'q' or SPACE to stop and choose new pin")
        print("-" * 40)
        
        try:
            self.setup_terminal()
            
            while self.running:
                # Read GPIO pin
                gpio_value = wiringpi.digitalRead(self.gpio_pin)
                timestamp = time.strftime("%H:%M:%S")
                
                print(f"[{timestamp}] GPIO Pin {self.gpio_pin}: {gpio_value}")
                
                # Check for keypress every 0.1 seconds for 1 second total
                for _ in range(10):
                    if self.check_for_keypress():
                        break
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            self.running = False
        finally:
            self.restore_terminal()
            
    def get_user_choice(self):
        """Get user input for new GPIO pin or exit"""
        while True:
            try:
                choice = input("\nOptions:\n1. Enter new GPIO pin number\n2. Exit program\nChoice (1/2): ").strip()
                
                if choice == '1':
                    gpio_input = input("Enter GPIO pin number: ").strip()
                    try:
                        gpio_pin = int(gpio_input)
                        if gpio_pin < 0:
                            print("GPIO pin must be a positive number.")
                            continue
                        return gpio_pin
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                        
                elif choice == '2':
                    return None  # Signal to exit
                    
                else:
                    print("Please enter 1 or 2.")
                    continue
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                return None

def main():
    reader = GPIOReader()
    
    print("GPIO Pin Monitor")
    print("================")
    
    # Get initial GPIO pin
    try:
        initial_pin = input("Enter initial GPIO pin number to monitor: ").strip()
        gpio_pin = int(initial_pin)
        if gpio_pin < 0:
            print("GPIO pin must be a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    except KeyboardInterrupt:
        print("\nExiting...")
        return
    
    try:
        while True:
            # Setup the GPIO pin
            reader.setup_gpio_pin(gpio_pin)
            reader.running = True
            
            # Start monitoring
            reader.read_gpio_loop()
            
            # When monitoring stops, get user choice
            choice = reader.get_user_choice()
            
            if choice is None:  # User wants to exit
                print("Goodbye!")
                break
            else:  # User wants to monitor new pin
                gpio_pin = choice
                print(f"\nSwitching to GPIO pin {gpio_pin}...")
                
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you're running with appropriate permissions (sudo)")

if __name__ == "__main__":
    main()