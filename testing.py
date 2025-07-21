import wiringpi
import time
import logging
import sys

class LoggerWriter:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message != '\n':
            self.level(message)

    def flush(self):
        pass

# Configure logging
logging.basicConfig(
    filename='sensor_log.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    filemode='a'
)

# Redirect print statements to logging
sys.stdout = LoggerWriter(logging.info)

# Pin definitions from your table
m1a = 17
m1b = 19
m2a = 18
m2b = 16
left_color = 25
right_color = 26
right_ir = 24
front_right_ir = 23
button = 14
left_ir = 13
front_left_ir = 12

# Pin mappings for easy reference
input_pins = {
    'left_color': left_color,
    'right_color': right_color,
    'right_ir': right_ir,
    'front_right_ir': front_right_ir,
    'button': button,
    'left_ir': left_ir,
    'front_left_ir': front_left_ir
}

output_pins = {
    'm1a': m1a,
    'm1b': m1b,
    'm2a': m2a,
    'm2b': m2b
}

# Store previous sensor states
previous_states = {}

def setup_gpio():
    """Initialize GPIO pins"""
    wiringpi.wiringPiSetup()
    
    # Setup input pins
    for pin in input_pins.values():
        wiringpi.pinMode(pin, wiringpi.INPUT)  # INPUT
    
    # Setup output pins
    for pin in output_pins.values():
        wiringpi.pinMode(pin, wiringpi.OUTPUT)  # OUTPUT
    
    # Initialize previous states
    for name, pin in input_pins.items():
        previous_states[name] = wiringpi.digitalRead(pin)

def scan_input(pin_name):
    """Read and display input pin state"""
    if pin_name in input_pins:
        pin = input_pins[pin_name]
        state = wiringpi.digitalRead(pin)
        status = "HIGH" if state else "LOW"
        print(f"Pin {pin_name} (GPIO {pin}): {status}")
    else:
        print(f"Unknown input pin: {pin_name}")
        print(f"Available inputs: {list(input_pins.keys())}")

def write_output(pin_name, value):
    """Write to output pin"""
    if pin_name in output_pins:
        pin = output_pins[pin_name]
        wiringpi.digitalWrite(pin, value)
        status = "HIGH" if value else "LOW"
        print(f"Set {pin_name} (GPIO {pin}) to {status}")
    else:
        print(f"Unknown output pin: {pin_name}")
        print(f"Available outputs: {list(output_pins.keys())}")

def scan_all_inputs():
    """Scan and display all input pins"""
    print("All Input Pin States:")
    print("-" * 30)
    for name, pin in input_pins.items():
        state = wiringpi.digitalRead(pin)
        status = "HIGH" if state else "LOW"
        print(f"{name:15} (GPIO {pin:2}): {status}")

def monitor_changes(duration=None):
    """Monitor sensor changes and print when they occur"""
    print(f"Monitoring sensor changes{'...' if duration is None else f' for {duration} seconds...'}")
    print("Press Ctrl+C to stop monitoring")
    
    start_time = time.time()
    
    try:
        while True:
            if duration and (time.time() - start_time) > duration:
                break
                
            for name, pin in input_pins.items():
                current_state = wiringpi.digitalRead(pin)
                
                if current_state != previous_states[name]:
                    old_status = "HIGH" if previous_states[name] else "LOW"
                    new_status = "HIGH" if current_state else "LOW"
                    print(f"CHANGE: {name} (GPIO {pin}) changed from {old_status} to {new_status}")
                    previous_states[name] = current_state
            
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage
            
    except KeyboardInterrupt:
        print("\nStopped monitoring")

def show_help():
    """Display available commands"""
    print("\nAvailable Commands:")
    print("scan <pin_name>     - Read input pin state")
    print("write <pin_name> <value> - Write to output pin (0 or 1)")
    print("scan_all           - Read all input pins")
    print("monitor [duration] - Monitor sensor changes (optional duration in seconds)")
    print("list_pins          - Show all available pins")
    print("help               - Show this help message")
    print("exit               - Exit program")

def list_pins():
    """List all available pins"""
    print("\nInput Pins:")
    for name, pin in input_pins.items():
        print(f"  {name:15} - Sensor {name} GPIO {pin}")

    print("\nOutput Pins:")
    for name, pin in output_pins.items():
        print(f"  {name:15} - Motor {name} GPIO {pin}")

def main():
    """Main program loop"""
    setup_gpio()
    
    print("GPIO Pin Scanner/Controller")
    print("=" * 30)
    print("Type 'help' for available commands")
    
    while True:
        # try:
            command = input("\n> ").strip().lower().split()
            
            if not command:
                continue
            
            if command[0] == "exit":
                break
            
            elif command[0] == "help":
                show_help()
            
            elif command[0] == "scan":
                if len(command) != 2:
                    print("Usage: scan <pin_name>")
                else:
                    scan_input(command[1])
            
            elif command[0] == "write":
                if len(command) != 3:
                    print("Usage: write <pin_name> <value>")
                else:
                    try:
                        value = int(command[2])
                        if value not in [0, 1]:
                            print("Value must be 0 or 1")
                        else:
                            write_output(command[1], value)
                    except ValueError:
                        print("Value must be 0 or 1")
            
            elif command[0] == "scan_all":
                scan_all_inputs()
            
            elif command[0] == "monitor":
                if len(command) == 1:
                    monitor_changes()
                elif len(command) == 2:
                    try:
                        duration = float(command[1])
                        monitor_changes(duration)
                    except ValueError:
                        print("Duration must be a number")
                else:
                    print("Usage: monitor [duration]")
            
            elif command[0] == "list_pins":
                list_pins()
            
            else:
                print(f"Unknown command: {command[0]}")
                print("Type 'help' for available commands")
        
        # except KeyboardInterrupt:
        #     print("\nExiting...")
        #     break
        # except Exception as e:
        #     print(f"Error: {e}")
    
    # Cleanup - turn off all outputs
    for pin in output_pins.values():
        wiringpi.digitalWrite(pin, 0)
    
    print("GPIO cleanup completed.")

if __name__ == "__main__":
    main()