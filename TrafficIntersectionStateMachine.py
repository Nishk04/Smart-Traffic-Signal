from enum import Enum
import time

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

    def activate_pedestrian_request(self):
        self.pedestrian_request = True

    #TO-DO: Implement a method to detect the number of cars waiting at the intersection
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

    def calculate_green_time(self, cars):
        # Linear Regression: 
        return 2 * cars + 5

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
        # Raspberry Pi GPIO integration goes here
        print(f"Turning on {current_light} light.")

# Example usage
signal = TrafficSignal()

# Simulate pedestrian request during the cycle
signal.activate_pedestrian_request()
signal.run()
