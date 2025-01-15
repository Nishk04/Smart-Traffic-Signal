import cv2
import numpy as np
import os

class DetectCars:
    def __init__(self):
        # Start the webcam
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0
        self.save_path = "Images"  # Directory to save frames
        self.detections = 0  # Initialize detection count

        # Create the directory if it doesn't exist
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def detect(self):
        while True:
            # Read the video frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame. Exiting...")
                break

            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to HSV color space
            hsv = cv2.cvtColor(rgbFrame, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for the red color
            lower_red1 = np.array([0, 120, 70])  # First range for red (hue 0-10)
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])  # Second range for red (hue 170-180)
            upper_red2 = np.array([180, 255, 255])

            # Create masks for red color
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 + mask2

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Draw a green rectangle around the red objects
            self.detections = 0  # Reset detection count for each frame
            for contour in contours:
                if cv2.contourArea(contour) > 400:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.detections += 1  # Increment detection count

            # Save the frame with the green rectangles to disk
            frame_filename = os.path.join(self.save_path, f"frame_{self.frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")

            self.frame_count += 1

            # Break the loop after saving a few frames for demonstration
            if self.frame_count >= 1:
                break

        self.cap.release()

    def get_detections(self):
        return self.detections

# Run the detection
detector = DetectCars()
detector.detect()
print(f"Number of detections: {detector.get_detections()}")