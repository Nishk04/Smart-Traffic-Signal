import time
from enum import Enum
import DetectCars as dc

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

detections = dc.get_detections()

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
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()
    
    def end_timer(self):
        self.end_time = time.time()
    
    def calculate_time(self):
        return self.end_time - self.start_time

    def activate_pedestrian_request(self):
        self.pedestrian_request = True

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
        self.current_phase_signal = self.get_next_signal(self.current_phase_signal) # Go to next signal 
    
    def get_next_signal(self, cur_signal):
        if cur_signal == PHASE_1:
            return PHASE_2
        else:
            return PHASE_1
    
    def calculate_green_time(self):
        return (1.47 * detections) + 8.43

    def run(self, cycles=5):
        for _ in range(cycles):
            self.start_timer()
            print(f"Current State: {self.state}")
            
            if self.state == TrafficState.GREEN:
                print("GREEN")
                time.sleep(self.green_time)
                self.end_timer()
                elapsed_time = self.calculate_time()
                print(f"Time: {elapsed_time:.2f} seconds (Expected: {self.green_time} seconds)")

            elif self.state == TrafficState.YELLOW:
                print("YELLOW")
                time.sleep(5)  # Fixed duration for yellow light
                self.end_timer()
                elapsed_time = self.calculate_time()
                print(f"Time: {elapsed_time:.2f} seconds (Expected: 5 seconds)")

            elif self.state == TrafficState.PEDESTRIAN:
                print("PEDESTRIAN")
                time.sleep(20)  # Fixed duration for pedestrian signal
                self.end_timer()
                elapsed_time = self.calculate_time()
                print(f"Time: {elapsed_time:.2f} seconds (Expected: 20 seconds)")

            else:  # Red light
                print("RED")
                time.sleep(5)  # Fixed duration for red light
                self.end_timer()
                elapsed_time = self.calculate_time()
                print(f"Time: {elapsed_time:.2f} seconds (Expected: 5 seconds)")
            
            self.transition()

# Run the program here
signal = TrafficSignal()
signal.activate_pedestrian_request()
signal.run()