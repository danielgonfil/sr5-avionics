from array import *

class Kalman:
    def __init__(self, dt: float, std_acceletation: float, std_altitude: float) -> None:
         # parameters
        self.dt = dt
        self.std_model = std_acceletation
        self.std_acceleration = 0.1
        self.std_altitude = 0.1
        
        # State transition matrix
        self.F = array([[1, self.dt, self.dt ** 2 / 2], 
                        [0, 1, dt],
                        [0, 0, 1]])
        
       
        
        # State vector
        self.S = array([[0],  # position
                        [0],  # speed
                        [0]]) # acceleration
        
        self.P = new_array(3, 3) # Covariance (uncertainty) matrix

        self.Q = array([[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, self.std_model ** 2]]) # Model covariance (uncertainty) matrix
    
        self.R = array([[self.std_altitude ** 2, 0],
                        [0, self.std_acceleration ** 2]]) # Measurement covariance (uncertainty) matrix
        
        self.H = array([[1, 0, 0],
                        [0, 0, 1]]) # Measurement matrix
        
        self.K = new_array(2, 2) # Kalman gain

    def update(self, altitude: float, acceleration: float) -> None:
        M = array([[altitude],
                   [acceleration]]) # measurement

        # print(self.G)
        self.S = self.F * self.S
        # print(self.S)
        
        # uncertainty of the prediction
        self.P = self.F * self.P * self.F.T + self.Q
        # print(self.P)

        # Kalman gain
        L = self.H * self.P * self.H.T + self.R
        self.K = self.P * self.H.T * inv(L)
        # print("K", self.K)

        # update the prediction
        self.S = self.S + self.K * (M - self.H * self.S)
        # print(self.S)

        # updating the uncertainty
        self.P = (Id(3) - self.K * self.H) * self.P
        # print(self.P)

    @property
    def state(self) -> float:
        return self.S

if __name__ == "__main__":
    filter = Kalman(0.1, 0.1, 0.1)
    for _ in range(10):
        filter.update(10, 30)
        print(filter.state)