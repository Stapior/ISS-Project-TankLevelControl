import numpy as np
import skfuzzy.control as ctrl


class Fuzzy:

    def __init__(self):
        output_universe = np.linspace(0, 1000, 9)
        universe = np.linspace(-10, 10, 7)
        self.error = ctrl.Antecedent(universe, 'error')
        self.delta = ctrl.Antecedent(universe, 'delta')
        self.output = ctrl.Consequent(output_universe, 'output')
        names = ['DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD']
        output_names = ['BDU', 'DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD', 'BDD']
        self.error.automf(names=names)
        self.delta.automf(names=names)
        self.output.automf(names=output_names)
        self.sim = self.getSimWithRules(self.error, self.delta, self.output)
        self.last_error = 0

    def getSimWithRules(self, error, delta, output):
        rules = [ctrl.Rule(antecedent=((error['DU'] & delta['DU'])), consequent=output['BDU']),
                 ctrl.Rule(antecedent=((error['DU'] & delta['SU'])), consequent=output['BDU']),
                 ctrl.Rule(antecedent=((error['DU'] & delta['MU'])), consequent=output['BDU']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['DU'])), consequent=output['BDU']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['SU'])), consequent=output['BDU']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['DU'])), consequent=output['BDU']),
                 ctrl.Rule(antecedent=((error['DU'] & delta['Z'])), consequent=output['DU']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['MU'])), consequent=output['DU']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['SU'])), consequent=output['DU']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['DU'])), consequent=output['DU']),
                 ctrl.Rule(antecedent=((error['DU'] & delta['MD'])), consequent=output['SU']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['Z'])), consequent=output['SU']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['MU'])), consequent=output['SU']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['SU'])), consequent=output['SU']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['DU'])), consequent=output['SU']),
                 ctrl.Rule(antecedent=((error['DU'] & delta['SD'])), consequent=output['MU']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['MD'])), consequent=output['MU']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['Z'])), consequent=output['MU']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['MU'])), consequent=output['MU']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['SU'])), consequent=output['MU']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['DU'])), consequent=output['MU']),
                 ctrl.Rule(antecedent=((error['DU'] & delta['DD'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['SD'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['MD'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['Z'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['MU'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['SU'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['DU'])), consequent=output['Z']),
                 ctrl.Rule(antecedent=((error['SU'] & delta['DD'])), consequent=output['MD']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['SD'])), consequent=output['MD']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['MD'])), consequent=output['MD']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['Z'])), consequent=output['MD']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['MU'])), consequent=output['MD']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['SU'])), consequent=output['MD']),
                 ctrl.Rule(antecedent=((error['MU'] & delta['DD'])), consequent=output['SD']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['SD'])), consequent=output['SD']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['MD'])), consequent=output['SD']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['Z'])), consequent=output['SD']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['MU'])), consequent=output['SD']),
                 ctrl.Rule(antecedent=((error['Z'] & delta['DD'])), consequent=output['DD']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['SD'])), consequent=output['DD']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['MD'])), consequent=output['DD']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['Z'])), consequent=output['DD']),
                 ctrl.Rule(antecedent=((error['MD'] & delta['DD'])), consequent=output['BDD']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['DD'])), consequent=output['BDD']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['DD'])), consequent=output['BDD']),
                 ctrl.Rule(antecedent=((error['SD'] & delta['SD'])), consequent=output['BDD']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['SD'])), consequent=output['BDD']),
                 ctrl.Rule(antecedent=((error['DD'] & delta['MD'])), consequent=output['BDD'])]

        system = ctrl.ControlSystem(rules=rules)
        return ctrl.ControlSystemSimulation(system)

    def update(self, error):
        ce = self.last_error - error
        self.last_error = error
        self.sim.input['error'] = error
        self.sim.input['delta'] = ce
        self.sim.compute()
        return self.sim.output['output']
