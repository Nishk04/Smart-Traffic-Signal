# Smart-Traffic-Signal

Smart traffic signals are designed to optimize the flow of vehicles and pedestrians at intersections. These systems adjust signal timings dynamically based on real-time traffic data, ensuring efficient and safe movement through intersections.

This project focuses on implementing a simplified smart traffic signal system. It integrates features like car detection, adaptive green light timing based on traffic flow, and a pedestrian signal.

For simplicity, the model simulates a single intersection with consistent traffic flow and car speeds. The images and videos below showcase the final model in action.

![Final Model](#) <!-- Add your GIF or video link here -->

---

## Key Features

1. **Dynamic Green Light Timing**  
   Adaptive signal timings based on the number of cars detected in each lane.

2. **Car Detection Using OpenCV**  
   The system detects cars (represented by red paper rectangles) using color-based image processing.

3. **Pedestrian Signal Integration**  
   Pedestrian signals operate with a buzzer and a button for user activation.

4. **Linear Regression Optimization**  
   Dummy traffic data is analyzed to determine optimal green light duration, minimizing congestion.

![Feature Showcase](#) <!-- Add your images or GIFs here -->

---

## Project Breakdown

### Step 1: State Machine Design

A state machine was created to handle the following states:
- **Red Light**
- **Green Light**
- **Yellow Light**
- **Pedestrian Signal**

Transitions occur in the sequence `Red → Green → Yellow → Red`, with interruptions for pedestrian signals as needed.

**Timings:**
- Red and Yellow: Fixed (5 seconds each)
- Green: Dynamic, based on car count
- Pedestrian Signal: Fixed (20 seconds)

![State Machine Diagram](#) <!-- Add your flowchart or diagram here -->

---

### Step 2: Car Detection

Using OpenCV, the system detects red rectangles (representing cars) on a cardboard intersection model. The process includes:
- Converting the image from BGR to HSV color space
- Applying masks to detect red objects
- Counting the detected "cars" to adjust green light timing

![Car Detection Process](#) <!-- Add screenshots or visual outputs here -->

---

### Step 3: Data Analysis and Timing Optimization

A dummy dataset was created to simulate traffic flow. Using linear regression, the optimal green light duration (`y = 1.47x + 8.43`) was calculated based on car count (`x`) and the time (`t`) it took for them to get across. In the real world, engineers would have to make these datasets using observations for the intersection they are analyzing. 

![Dummy Data Graph](#) <!-- Add your graph here -->

---

### Step 4: Model Intersection Creation

A 12x12-inch cardboard model was built to simulate the intersection, featuring lanes, signals, and cars. The camera was mounted 7 inches above the center for optimal detection coverage as it sees only the lanes and nothing else to reduce any distractions.

![Model Intersection](#) <!-- Add a photo of your model here -->

---

### Step 5: Raspberry Pi Integration

The Raspberry Pi handles signal control, including:
- LEDs for traffic lights
- A camera for detection of cars and pedestrians
- A button and buzzer for pedestrian signal activation

**Key commands for setup:**
```bash
sudo apt update
sudo apt install python3-libraryName
```

---

### Challenges
1. **Car Detection Accuracy**  
   - The initial detection algorithm struggled to differentiate cars from the background.  
   - Adding a smaller, controlled intersection model with a consistent background (brown cardboard) improved detection.  

2. **Time Constraints**  
   - Limited project time meant focusing on core features, such as car detection and state machine logic, while deferring more advanced functionality like detecting multiple car colors. This also meant that I couldn't finish troubleshooting with the wiring to the raspberry pi. 

3. **GPIO Power Issue**  
   - During initial testing, GPIO pins provided power without the expected code execution. Debugging this required reconfiguration and additional testing.  

4. **Dataset Limitations**  
   - The YOLO model was unsuitable due to the lack of sufficient labeled data and training time.  
   - Opted for OpenCV to detect red cars instead of training a custom neural network which caused there to be less model pieces like pedestrians as paper clips
to be used for the project.

### Future Improvements
1. **Detection Algorithm**  
   - Detect pedestrians as paper clips and other colored rectangles as different cars. 

2. **Linear Regression Model for Pedestrians**  
   - Based on pedestrian detection, I could have made the time for the pedestrian signal longer if my model detects someone with a disability that may need more time to walk. I could have done the same for different types of cars by labeling them with a certain color of paper to add more complexity to the project.

3. **Pedestrian Signal Integration**  
   - Added a pedestrian signal with a button and buzzer for user interaction, despite time constraints.

---
