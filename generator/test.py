import time
print(time.time())
# # Initialize variables to hold the sum of values and the count of lines
# sum_value1 = 0
# sum_value2 = 0
# count = 0
#
# # Open the file and process each line
# with open('results.txt', 'r') as file:
#     for line in file:
#         # Split the line by comma to extract value1 and value2
#         value1, value2 = line.split(',')
#
#         # Convert the extracted values to floats or ints
#         value1 = float(value1.strip())
#         value2 = float(value2.strip())
#
#         # Add the values to the running total
#         sum_value1 += value1
#         sum_value2 += value2
#
#         # Increment the line count
#         count += 1
#
# # Calculate the average of each value
# average_value1 = sum_value1 / count
# average_value2 = sum_value2 / count
#
# # Output the results
# print(f"Average of value1: {average_value1}")
# print(f"Average of value2: {average_value2}")

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
#
# def convert_to_float(value):
#     try:
#         # Try to convert the value directly to a float
#         return float(value)
#     except ValueError:
#         # If it fails, assume it's a fraction like '2/3' and convert it to a float
#         numerator, denominator = value.split('/')
#         return float(numerator) / float(denominator)
#
# # Initialize lists to hold the data
# confidence_levels = []
# distance_thresholds = []
# average_miss_location_amounts = []
# average_step_amounts = []
#
# # Read data from file
# file_name = 'final_results.txt'  # Replace with your file path
# with open(file_name, 'r') as file:
#     for line in file:
#         # Split the line into four values
#         values = line.strip().split(',')
#         # Convert each value to float, handling fractions if necessary
#         confidence_levels.append(convert_to_float(values[0]))
#         distance_thresholds.append(convert_to_float(values[1]))
#         average_miss_location_amounts.append(convert_to_float(values[2]))
#         average_step_amounts.append(convert_to_float(values[3]))
#
# # Convert lists to numpy arrays for plotting
# confidence_levels = np.array(confidence_levels)
# distance_thresholds = np.array(distance_thresholds)
# average_miss_location_amounts = np.array(average_miss_location_amounts)
# average_step_amounts = np.array(average_step_amounts)
#
# # Create the first 3D plot for average miss location amount (value3)
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111, projection='3d')
# ax1.scatter(confidence_levels, distance_thresholds, average_miss_location_amounts, color='b')
# ax1.set_xlabel('Confidence Level')
# ax1.set_ylabel('Distance Threshold')
# ax1.set_zlabel('Average Miss Location Amount')
# ax1.set_title('Movement Test - Average Miss Location Amount')
#
# # Create the second 3D plot for average step amount (value4)
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111, projection='3d')
# ax2.scatter(confidence_levels, distance_thresholds, average_step_amounts, color='r')
# ax2.set_xlabel('Confidence Level')
# ax2.set_ylabel('Distance Threshold')
# ax2.set_zlabel('Average Step Amount')
# ax2.set_title('Movement Test - Average Step Amount')
#
# # Show both plots
# plt.show()
