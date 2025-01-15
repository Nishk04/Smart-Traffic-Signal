from picamera2 import Picamera2
import cv2
import numpy as np

# Initialize the Pi Camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)}))
picam2.start()

class DetectCarsRaspPi:
    def __init__(self):
        self.frame_count = 0
    
    def detect(self):
        # Capture a single frame from the Pi Camera
        frame = picam2.capture_array()
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(rgbFrame, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for the red color
        lower_red1 = np.array([0, 120, 70])  # First range for red (hue 0-10)
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])  # Second range for red (hue 170-180)
        upper_red2 = np.array([180, 255, 255])

        # Create masks for the red color
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Find contours of red areas
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize counter for rectangles
        rectangle_count = 0

        # Draw a green rectangle around the red objects
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filter small contours
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(rgbFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rectangle_count += 1  # Increment rectangle count for each valid contour

        # Display the rectangle count on the frame
        cv2.putText(rgbFrame, f"Rectangles: {rectangle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Show the live feed
        cv2.imshow("Original Frame", rgbFrame)

        # Wait for the 'q' key to be pressed to close the window
        while True:
            key = cv2.waitKey(100)  # Wait for 1 millisecond for key press
            if key == ord('q'):  # Exit when 'q' is pressed
                break  # Exit the loop when 'q' is pressed

        # Stop the camera and close windows after the loop ends
        picam2.stop()
        cv2.destroyAllWindows()
        return rectangle_count


# Initialize the detection class and run the detection
car_detector = DetectCarsRaspPi()
detections = car_detector.detect()

