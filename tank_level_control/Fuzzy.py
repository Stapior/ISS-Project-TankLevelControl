import numpy as np
import skfuzzy.control as ctrl


def getSimWithRules(error, integrator, output):
    rules = [ctrl.Rule(antecedent=((error['DU'] & integrator['DU']) |
                                   (error['DU'] & integrator['SU']) |
                                   (error['DU'] & integrator['MU']) |
                                   (error['SU'] & integrator['DU']) |
                                   (error['SU'] & integrator['SU']) |
                                   (error['MU'] & integrator['DU'])),
                       consequent=output['BDU']),

             ctrl.Rule(antecedent=((error['DU'] & integrator['Z']) |
                                   (error['SU'] & integrator['MU']) |
                                   (error['MU'] & integrator['SU']) |
                                   (error['Z'] & integrator['DU'])),
                       consequent=output['DU']),

             ctrl.Rule(antecedent=((error['DU'] & integrator['MD']) |
                                   (error['SU'] & integrator['Z']) |
                                   (error['MU'] & integrator['MU']) |
                                   (error['Z'] & integrator['SU']) |
                                   (error['MD'] & integrator['DU'])),
                       consequent=output['SU']),

             ctrl.Rule(antecedent=((error['DU'] & integrator['SD'])|
                                   (error['SU'] & integrator['MD']) |
                                   (error['MU'] & integrator['Z']) |
                                   (error['Z'] & integrator['MU']) |
                                   (error['MD'] & integrator['SU']) |
                                   (error['SD'] & integrator['DU'])),
                       consequent=output['MU']),

             ctrl.Rule(antecedent=((error['DU'] & integrator['DD']) |
                                   (error['SU'] & integrator['SD']) |
                                   (error['MU'] & integrator['MD']) |
                                   (error['Z'] & integrator['Z']) |
                                   (error['MD'] & integrator['MU']) |
                                   (error['SD'] & integrator['SU']) |
                                   (error['DD'] & integrator['DU'])),
                       consequent=output['Z']),

             ctrl.Rule(antecedent=((error['SU'] & integrator['DD']) |
                                   (error['MU'] & integrator['SD']) |
                                   (error['Z'] & integrator['MD']) |
                                   (error['MD'] & integrator['Z']) |
                                   (error['SD'] & integrator['MU']) |
                                   (error['DD'] & integrator['SU'])),
                       consequent=output['MD']),

             ctrl.Rule(antecedent=((error['MU'] & integrator['DD']) |
                                   (error['Z'] & integrator['SD']) |
                                   (error['MD'] & integrator['MD']) |
                                   (error['SD'] & integrator['Z']) |
                                   (error['DD'] & integrator['MU'])),
                       consequent=output['SD']),

             ctrl.Rule(antecedent=((error['Z'] & integrator['DD']) |
                                   (error['MD'] & integrator['SD']) |
                                   (error['SD'] & integrator['MD']) |
                                   (error['DD'] & integrator['Z'])),
                       consequent=output['DD']),

             ctrl.Rule(antecedent=((error['MD'] & integrator['DD']) |
                                   (error['SD'] & integrator['DD']) |
                                   (error['DD'] & integrator['DD']) |
                                   (error['SD'] & integrator['SD']) |
                                   (error['DD'] & integrator['SD']) |
                                   (error['DD'] & integrator['MD'])),
                       consequent=output['BDD'])]
    system = ctrl.ControlSystem(rules=rules)
    return ctrl.ControlSystemSimulation(system, flush_after_run=10)


class Fuzzy:

    def __init__(self):
        output_universe = np.linspace(0, 100, 9)
        error_universe = np.array([-10., -7., -4, 0, 4, 7., 10.]) * 2
        integrator_universe = np.array([-10., -7., -4, 0, 4, 7., 10.]) * 10
        self.error = ctrl.Antecedent(error_universe, 'error')
        self.integrator = ctrl.Antecedent(integrator_universe, 'integrator')
        self.output = ctrl.Consequent(output_universe, 'output')
        names = ['DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD']
        output_names = ['BDU', 'DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD', 'BDD']
        self.error.automf(names=names)
        self.integrator.automf(names=names)
        self.output.automf(names=output_names)
        self.sim = getSimWithRules(self.error, self.integrator, self.output)
        self.error_sum = 0

    def update(self, error, duration):
        # ce = (self.last_error - error) / duration
        self.error_sum += error * duration
        self.sim.input['error'] = error
        self.sim.input['integrator'] = self.error_sum
        self.sim.compute()
        return self.sim.output['output']
