# import the required libraries
from kalman import Kalman
import time, csv

a0, p0, std_a, std_z = 1.074307, 96538.98, 0.004518452, 0.04360311
f = 100
filter = Kalman(dt = 1 / f, std_pred = 0.004518452, std_measure = 0.04360311)

import csv
# altitude, acceleration
file = open("/Users/daniel/Documents/sr5-avionics/kalman/data.csv", newline = '')
result = open("/Users/daniel/Documents/sr5-avionics/kalman/results.csv", "w+")
data = csv.reader(file, delimiter = ',')
results = csv.writer(result, delimiter = ',')

for row in data:
    altitude, acceleration = float(row[0]), float(row[1])
    filter.update(measurement = altitude, input = acceleration)
    results.writerow([filter.state[0][0], altitude, filter.state[1][0], acceleration])
    # print(filter.state[0][0], altitude, filter.state[1][0], filter.state[2][0], acceleration)
    time.sleep(filter.dt)

file.close()
result.close()