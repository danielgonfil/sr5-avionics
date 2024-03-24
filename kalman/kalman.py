from array import *

class Kalman:
    def __init__(self, dt: float, std_pred: float, std_measure: float) -> None:
        self.F = array([[1, dt], [0, 1]]) # State transition matrix
        self.G = array([[0.5 * dt ** 2], [dt]]) # Control input matrix
        
        self.dt = dt
        self.std_pred = std_pred
        self.std_measure = std_measure
        
        self.M = new_array(1, 1) # Measurement vector

        self.S = new_array(2, 1) # State vector
        self.P = new_array(2, 2) # Covariance (uncertainty) matrix
        self.Q = self.G * self.G.T * self.std_pred ** 2 # Process covariance (uncertainty) matrix
        self.H = array([[1, 0]]) # Measurement matrix
        self.K = new_array(2, 2) # Kalman gain

    def update(self, input: float, measurement: float) -> None:
        U = array([[input]]) # input variable
        M = array([[measurement]]) # measurement

        # print(self.G)
        self.S = self.F * self.S + self.G * U
        # print(self.S)
        
        # uncertainty of the prediction
        self.P = self.F * self.P * self.F.T + self.Q
        # print(self.P)

        # Kalman gain
        L = self.H * self.P * self.H.T + array([[self.std_measure ** 2]])
        self.K = self.P * self.H.T * inv(L)
        # print("K", self.K)

        # update the prediction
        self.S = self.S + self.K * (M - self.H * self.S)
        # print(self.S)

        # updating the uncertainty
        self.P = (Id(2) - self.K * self.H) * self.P
        # print(self.P)

    @property
    def state(self) -> float:
        return self.S

if __name__ == "__main__":
    a = array([[1, 2, 3], 
               [4, 10, 6],
               [7, 8, 9]])

    # filter = Kalman(0.1, 0.1, 0.1)
    # print(filter.S)
    # filter.update(10, 30)
    # print(filter.S)