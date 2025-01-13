import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "Traffic Signal Dummy Data.xlsx"  # Replace with the path to your Excel file
data = pd.read_excel(file_path)

# Extract the columns
x = data['Number of Cars'].values.reshape(-1, 1)  # Independent variable (Number of cars)
y = data['Green Light Duration (seconds)'].values  # Dependent variable (Green light duration)

# Create and train the linear regression model
model = LinearRegression()
model.fit(x, y)

# Get the regression equation
slope = model.coef_[0]
intercept = model.intercept_
print(f"Linear Regression Equation: y = {slope:.2f}x + {intercept:.2f}")

# Predict y values for plotting the regression line
y_pred = model.predict(x)

# Plot the data and the regression line
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color="blue", label="Data Points")
plt.plot(x, y_pred, color="red", linestyle="--", label="Regression Line")
plt.title("Linear Regression: Number of Cars vs Green Light Duration")
plt.xlabel("Number of Cars")
plt.ylabel("Green Light Duration (seconds)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
