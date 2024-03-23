from array import *

class KalmanFilter:
    def __init__(self, dt, process_noise, measurement_noise, initial_position_estimate=0, initial_velocity_estimate=0):
        self.dt = dt  # Time step
        self.process_noise = process_noise  # Process noise covariance
        self.measurement_noise = measurement_noise  # Measurement noise covariance

        # State transition matrix
        self.A = array([[1, dt],
                        [0, 1]])

        # Control matrix
        self.B = array([[0.5 * dt ** 2],
                        [dt]])

        # Measurement matrix
        self.H = array([[1, 0]])

        # Covariance of the estimated state
        self.P = Id(2)

        # Initial state estimate
        self.x = array([[initial_position_estimate],
                           [initial_velocity_estimate]])

    def predict(self, u = 0):
        # Predict the next state
        self.x = self.A * self.x + self.B * u
        self.P = self.A * self.P * self.A.T() + self.process_noise

    def update(self, z):
        # Update the state estimate based on measurement z
        y = z - self.H * self.x  # Residual
        S = self.H * self.P * self.H.T() + self.measurement_noise  # Innovation covariance
        K = self.P * self.H.T() * inv(S)  # Kalman gain

        # Update state estimate and covariance
        self.x = self.x + K * y
        self.P = (Id(2) - K * self.H) * self.P

    def get_position(self):
        return self.x[0][0]

# Example usage
if __name__ == "__main__":
    # Constants
    dt = 0.01  # Time step in seconds
    process_noise = diag([0.1, 0.1])  # Process noise covariance
    measurement_noise = 0.1  # Measurement noise covariance

    # Create Kalman Filter
    kf = KalmanFilter(dt, process_noise, measurement_noise)

    # Simulated acceleration data (replace this with real data from MPU6050)
    accelerations = random_matrix(1, 1000) * 2 

    # Simulate double integration to get position
    positions = []
    for acc in accelerations:
        kf.predict(u=acc)
        positions.append(kf.get_position())

    # Plotting
    import matplotlib.pyplot as plt
    plt.plot(positions, label='Kalman Filtered Position')
    plt.xlabel('Time steps')
    plt.ylabel('Position')
    plt.title('Position Estimation using Kalman Filter')
    plt.legend()
    plt.show()