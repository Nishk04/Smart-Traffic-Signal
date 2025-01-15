from enum import Enum
import time
import RPi.GPIO as GPIO
import atexit
import CarDetection as dc

# Setup GPIO Pins
SIGNAL_1 = {'RED': 2, 'YELLOW': 3, 'GREEN': 4}
SIGNAL_2 = {'RED': 14, 'YELLOW': 15, 'GREEN': 18}
SIGNAL_3 = {'RED': 17, 'YELLOW': 22, 'GREEN': 22}
SIGNAL_4 = {'RED': 10, 'YELLOW': 9, 'GREEN': 11}
PEDESTRIAN_BUZZER = 10
PEDESTRIAN_BUTTON = 11

ALL_SIGNALS = [SIGNAL_1, SIGNAL_2, SIGNAL_3, SIGNAL_4]
PHASE_1 = [SIGNAL_1, SIGNAL_3]
PHASE_2 = [SIGNAL_2, SIGNAL_4]

GPIO.setmode(GPIO.BCM)

# Setup pins for lights and buzzer
for signal in PHASE_1 and PHASE_2:
    GPIO.setup(list(signal.values()), GPIO.OUT) # Setup all pins in the signal group
GPIO.setup(PEDESTRIAN_BUZZER, GPIO.OUT)
GPIO.setup(PEDESTRIAN_BUTTON, GPIO.IN)

#########################################################################################################

class TrafficState(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    PEDESTRIAN = 4

class TrafficSignal:
    def __init__(self):
        self.state = TrafficState.RED
        self.green_time = 10  # Default green light duration
        self.pedestrian_request = False
        self.current_phase_signal = PHASE_1  # Active signal group
        #self.detections = dc.detector.detect()
        self.detections = dc.detections
    def activate_pedestrian_request(self):
        if(GPIO.input(PEDESTRIAN_BUTTON)):
            self.pedestrian_request = True

    #TO-DO: Implement a method to detect the number of cars waiting at the intersection
    # Controls which state to go to next
    def transition(self, cars=0):
        if self.state == TrafficState.RED:
            if self.pedestrian_request:
                self.state = TrafficState.PEDESTRIAN
            else:
                self.state = TrafficState.GREEN
                self.green_time = self.calculate_green_time(cars)
        elif self.state == TrafficState.GREEN:
            self.state = TrafficState.YELLOW
        elif self.state == TrafficState.YELLOW:
            self.state = TrafficState.RED
        elif self.state == TrafficState.PEDESTRIAN:
            self.state = TrafficState.RED
            self.pedestrian_request = False  # Reset pedestrian request
        #To-Do: Method to go to next signal in the list + figure out which phase to use for the intersection
        self.current_phase_signal = self.get_next_signal(self.current_phase_signal) # Go to next signal 
    
    def get_next_signal(self, cur_signal):
        if cur_signal == PHASE_1:
            return PHASE_2
        else:
            return PHASE_1
    
    def calculate_green_time(self):
        # Linear Regression: y = 1.47x + 8.43
        return (1.47 * detections) + 8.43

    def run(self, cycles=5):
        for _ in range(cycles):
            print(f"Current State: {self.state}")
            
            if self.state == TrafficState.GREEN:
                self.control_lights("GREEN")
                time.sleep(self.green_time)
            elif self.state == TrafficState.YELLOW:
                self.control_lights("YELLOW")
                time.sleep(5)  # Fixed duration for yellow light
            elif self.state == TrafficState.PEDESTRIAN:
                self.control_lights("PEDESTRIAN")
                time.sleep(20)  # Fixed duration for pedestrian signal
            else:  # Red light
                self.control_lights("RED")
                time.sleep(5)  # Fixed duration for red light
            
            self.transition()

    def control_lights(self, current_light):
        # Turn off all lights in the current signal first
        GPIO.output(list(self.current_phase_signal[0].values()), GPIO.LOW)
        GPIO.output(list(self.current_phase_signal[1].values()), GPIO.LOW)
        GPIO.output(PEDESTRIAN_BUZZER, GPIO.LOW)  # Turn off buzzer

        # Turn on appropriate light by getting specific pin from the current signal
        if current_light == "RED":
            GPIO.output(self.current_phase_signal[0]['RED'], GPIO.HIGH)
            GPIO.output(self.current_phase_signal[1]['RED'], GPIO.HIGH)
        elif current_light == "YELLOW":
            GPIO.output(self.current_phase_signal[0]['YELLOW'], GPIO.HIGH)
            GPIO.output(self.current_phase_signal[1]['YELLOW'], GPIO.HIGH)
        elif current_light == "GREEN":
            GPIO.output(self.current_phase_signal[0]['GREEN'], GPIO.HIGH)
            GPIO.output(self.current_phase_signal[1]['GREEN'], GPIO.HIGH)
        elif current_light == "PEDESTRIAN":
            GPIO.output(PEDESTRIAN_BUZZER, GPIO.HIGH)  # Activate buzzer

#########################################################################################################

# GPIO Cleanup Logic when the program exits
@atexit.register
def cleanup_gpio():
    #Turn off all lights and buzzer
    GPIO.output([pin for signal in PHASE_1 and PHASE_2 for pin in signal.values()], GPIO.LOW)
    GPIO.output(PEDESTRIAN_BUZZER, GPIO.LOW)
    GPIO.cleanup()

# Run the program here
signal = TrafficSignal()
signal.run()