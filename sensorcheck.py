import OPi.GPIO as GPIO
import time
import sys
import select
import termios
import tty

class GPIOReader:
    def __init__(self):
        self.gpio_pin = None
        self.running = False
        self.old_settings = termios.tcgetattr(sys.stdin)
        
        # Setup GPIO mode
        GPIO.setmode(GPIO.BOARD)  # or GPIO.BCM
        
    def setup_gpio_pin(self, gpio_pin):
        """Setup a specific GPIO pin for reading"""
        self.gpio_pin = gpio_pin
        GPIO.setup(self.gpio_pin, GPIO.IN)  # Set as INPUT
        
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
                gpio_value = GPIO.input(self.gpio_pin)
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
            
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()

# Install with: pip install OrangePi.GPIO