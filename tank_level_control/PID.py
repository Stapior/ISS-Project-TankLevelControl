import math
class PID:
    """
    Discrete PID control
    """

    def __init__(self, P=2.0, I=0.0, D=1.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.Derivator = 0
        self.Integrator = 0
        self.Integrator_max = 500
        self.Integrator_min = -500
        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):

        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * (self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        self.Integrator = abs(self.Integrator)
       # self.Integrator = math.pow(self.Integrator,2)

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki

        return self.P_value + self.I_value + self.D_value

    def setPoint(self, set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.Integrator = 0
        self.Derivator = 0


