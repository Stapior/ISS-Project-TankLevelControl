class PID:

    def __init__(self, p=2.0, i=0.0, d=1.0, integrator_max=500, integrator_min=-500):
        self.Kp = p
        self.Ki = i
        self.Kd = d
        self.Integrator_max = integrator_max
        self.Integrator_min = integrator_min

        self.last_time = 0
        self.last_error = 0
        self.Integrator = 0
        self.set_point = 0.0

    def update(self, current_value, time):

        error = self.set_point - current_value
        duration = time - self.last_time


        self.Integrator = self.Integrator + error * duration
        self.trim_integrator()

        P_value = self.Kp * error
        I_value = self.Integrator * self.Ki
        D_value = self.Kd * (error - self.last_error) / duration

        self.last_error = error

        return P_value + I_value + D_value

    def wskaznikJakosci(self, current_value, time, i):

        self.i = i
        error = self.set_point - current_value
        duration = time - self.last_time

        if i == 1:
            self.Integrator = self.Integrator + error * duration  # normal pid
        elif i == 2:
            self.Integrator = self.Integrator + abs(error) * duration  # IAE
        elif i == 3:
            self.Integrator = self.Integrator + pow(error, 2) * duration  # ISE
        elif i == 4:
            self.Integrator = self.Integrator + time * abs(error) * duration  # ITAE
        elif i == 5:
            self.Integrator = self.Integrator + time * pow(error, 2) * duration  # ITSE
        self.trim_integrator()

        P_value = self.Kp * error
        I_value = self.Integrator * self.Ki
        D_value = self.Kd * (error - self.last_error) / duration

        self.last_error = error

        return P_value + I_value + D_value


    def trim_integrator(self):
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

    def setPoint(self, point):
        self.set_point = point
        self.Integrator = 0
        self.last_error = 0
