# Smart-Traffic-Signal
Smart traffic signals are found on most roads and they help with keeping the flow of traffic going. Smart signal not only track the amount of vehicles in a particular intersection and calculate the green light time for an intersection but also depending on the time of day as well because it tracks traffic flow at different times of day. They many layers of complexity involved in creating a smart traffic signal. Some include the particular traffic phase for a signal, amount of traffic flow at different times of day, number of lanes, and other physical obstacles like lighting and sensor use. 

For my project, I've used a simple traffic intersection as show in the picture below. To make the project less complex as I also don't have the mass data I would need to train my model, I've decided to use a consistent flow of traffic through the "day" for my model as well as a consistent speed of the cars as they cross the intersection. 

{image coming soon}

I broke down the creation of this signal into these steps:
1. Create state machine
2. Detect model cars
3. Use a linear regression on dummy data
4. Create cardboard model intersection
5. Plan Rasp Pi wiring


