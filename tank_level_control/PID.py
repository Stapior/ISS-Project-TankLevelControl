class PID:
    """
    Discrete PID control
    """

    def __init__(self, P=2.0, I=0.0, D=1.0, ):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.Derivator = 0
        self.Integrator = 0
        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):

        self.error = self.set_point - current_value

        P_value = self.Kp * self.error
        D_value = self.Kd * (self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        I_value = self.Integrator * self.Ki

        return P_value + I_value + D_value

    def setPoint(self, set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.Integrator = 0
        self.Derivator = 0


