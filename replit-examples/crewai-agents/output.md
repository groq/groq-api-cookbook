Here is the starter Python code for the project:

```Python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load the data
data = pd.read_csv('nba_data.csv')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.drop('points', axis=1), data['points'], test_size=0.2, random_state=42)

# Define the models
model_linear_regression = LinearRegression()
model_decision_tree = DecisionTreeRegressor()
model_random_forest = RandomForestRegressor()
model_gradient_boosting = GradientBoostingRegressor()

# Train the models
model_linear_regression.fit(X_train, y_train)
model_decision_tree.fit(X_train, y_train)
model_random_forest.fit(X_train, y_train)
model_gradient_boosting.fit(X_train, y_train)

# Evaluate the models
y_pred_linear_regression = model_linear_regression.predict(X_test)
y_pred_decision_tree = model_decision_tree.predict(X_test)
y_pred_random_forest = model_random_forest.predict(X_test)
y_pred_gradient_boosting = model_gradient_boosting.predict(X_test)

# Calculate the metrics
mae_linear_regression = mean_absolute_error(y_test, y_pred_linear_regression)
mse_linear_regression = mean_squared_error(y_test, y_pred_linear_regression)

mae_decision_tree = mean_absolute_error(y_test, y_pred_decision_tree)
mse_decision_tree = mean_squared_error(y_test, y_pred_decision_tree)

mae_random_forest = mean_absolute_error(y_test, y_pred_random_forest)
mse_random_forest = mean_squared_error(y_test, y_pred_random_forest)

mae_gradient_boosting = mean_absolute_error(y_test, y_pred_gradient_boosting)
mse_gradient_boosting = mean_squared_error(y_test, y_pred_gradient_boosting)

print("Linear Regression MAE: ", mae_linear_regression)
print("Linear Regression MSE: ", mse_linear_regression)

print("Decision Tree MAE: ", mae_decision_tree)
print("Decision Tree MSE: ", mse_decision_tree)

print("Random Forest MAE: ", mae_random_forest)
print("Random Forest MSE: ", mse_random_forest)

print("Gradient Boosting MAE: ", mae_gradient_boosting)
print("Gradient Boosting MSE: ", mse_gradient_boosting)
```

This code provides a basic structure for the project, including data loading, model definition, and a basic training loop. The models are trained using the training data and evaluated using the testing data. The metrics used for evaluation are Mean Absolute Error (MAE) and Mean Squared Error (MSE).