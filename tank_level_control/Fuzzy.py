import numpy as np
import skfuzzy.control as ctrl

class Fuzzy:

    def __init__(self, error, delta, output):
        self.error = error
        self.delta = delta
        self.output = output

    def rule(self, error, delta, output):

        universe = np.linspace(-4, 4, 9)
        self.error = ctrl.Antecedent(universe, 'error')
        self.delta = ctrl.Antecedent(universe, 'delta')
        self.output = ctrl.Consequent(universe, 'output')


        rule0 = ctrl.Rule(antecedent=((error['DU'] & delta['DU'])), consequent=output['BDU'])
        rule1 = ctrl.Rule(antecedent=((error['DU'] & delta['SU'])), consequent=output['BDU'])
        rule2 = ctrl.Rule(antecedent=((error['DU'] & delta['MU'])), consequent=output['BDU'])
        rule3 = ctrl.Rule(antecedent=((error['SU'] & delta['DU'])), consequent=output['BDU'])
        rule4 = ctrl.Rule(antecedent=((error['SU'] & delta['SU'])), consequent=output['BDU'])
        rule5 = ctrl.Rule(antecedent=((error['MU'] & delta['SU'])), consequent=output['BDU'])

        rule6 = ctrl.Rule(antecedent=((error['DU'] & delta['Z'])), consequent=output['DU'])
        rule7 = ctrl.Rule(antecedent=((error['SU'] & delta['MU'])), consequent=output['DU'])
        rule8 = ctrl.Rule(antecedent=((error['MU'] & delta['SU'])), consequent=output['DU'])
        rule9 = ctrl.Rule(antecedent=((error['Z'] & delta['SU'])), consequent=output['DU'])

        rule10 = ctrl.Rule(antecedent=((error['DU'] & delta['MD'])), consequent=output['SU'])
        rule11 = ctrl.Rule(antecedent=((error['SU'] & delta['Z'])), consequent=output['SU'])
        rule12 = ctrl.Rule(antecedent=((error['MU'] & delta['MU'])), consequent=output['SU'])
        rule13 = ctrl.Rule(antecedent=((error['Z'] & delta['SU'])), consequent=output['SU'])
        rule14 = ctrl.Rule(antecedent=((error['MD'] & delta['DU'])), consequent=output['SU'])

        rule15 = ctrl.Rule(antecedent=((error['DU'] & delta['SD'])), consequent=output['MU'])
        rule16 = ctrl.Rule(antecedent=((error['SU'] & delta['MD'])), consequent=output['MU'])
        rule17 = ctrl.Rule(antecedent=((error['MU'] & delta['Z'])), consequent=output['MU'])
        rule18 = ctrl.Rule(antecedent=((error['Z'] & delta['MU'])), consequent=output['MU'])
        rule19 = ctrl.Rule(antecedent=((error['MD'] & delta['SU'])), consequent=output['MU'])
        rule20 = ctrl.Rule(antecedent=((error['SD'] & delta['DU'])), consequent=output['MU'])

        rule21 = ctrl.Rule(antecedent=((error['DU'] & delta['DD'])), consequent=output['Z'])
        rule22 = ctrl.Rule(antecedent=((error['SU'] & delta['SD'])), consequent=output['Z'])
        rule23 = ctrl.Rule(antecedent=((error['MU'] & delta['MD'])), consequent=output['Z'])
        rule24 = ctrl.Rule(antecedent=((error['Z'] & delta['Z'])), consequent=output['Z'])
        rule25 = ctrl.Rule(antecedent=((error['MD'] & delta['MU'])), consequent=output['Z'])
        rule26 = ctrl.Rule(antecedent=((error['SD'] & delta['SU'])), consequent=output['Z'])
        rule27 = ctrl.Rule(antecedent=((error['DD'] & delta['DU'])), consequent=output['Z'])

        rule28 = ctrl.Rule(antecedent=((error['SU'] & delta['DD'])), consequent=output['MD'])
        rule29 = ctrl.Rule(antecedent=((error['MU'] & delta['SD'])), consequent=output['MD'])
        rule30 = ctrl.Rule(antecedent=((error['Z'] & delta['MD'])), consequent=output['MD'])
        rule31 = ctrl.Rule(antecedent=((error['MD'] & delta['Z'])), consequent=output['MD'])
        rule32 = ctrl.Rule(antecedent=((error['SD'] & delta['MU'])), consequent=output['MD'])
        rule33 = ctrl.Rule(antecedent=((error['DD'] & delta['SU'])), consequent=output['MD'])

        rule34 = ctrl.Rule(antecedent=((error['MU'] & delta['DD'])), consequent=output['SD'])
        rule35 = ctrl.Rule(antecedent=((error['Z'] & delta['SD'])), consequent=output['SD'])
        rule36 = ctrl.Rule(antecedent=((error['MD'] & delta['MD'])), consequent=output['SD'])
        rule37 = ctrl.Rule(antecedent=((error['SD'] & delta['Z'])), consequent=output['SD'])
        rule38 = ctrl.Rule(antecedent=((error['DD'] & delta['MU'])), consequent=output['SD'])

        rule39 = ctrl.Rule(antecedent=((error['Z'] & delta['DD'])), consequent=output['DD'])
        rule40 = ctrl.Rule(antecedent=((error['MD'] & delta['SD'])), consequent=output['DD'])
        rule41 = ctrl.Rule(antecedent=((error['SD'] & delta['MD'])), consequent=output['DD'])
        rule42 = ctrl.Rule(antecedent=((error['DD'] & delta['Z'])), consequent=output['DD'])

        rule43 = ctrl.Rule(antecedent=((error['MD'] & delta['DD'])), consequent=output['BDD'])
        rule44 = ctrl.Rule(antecedent=((error['SD'] & delta['DD'])), consequent=output['BDD'])
        rule45 = ctrl.Rule(antecedent=((error['DD'] & delta['DD'])), consequent=output['BDD'])
        rule46 = ctrl.Rule(antecedent=((error['SD'] & delta['SD'])), consequent=output['BDD'])
        rule47 = ctrl.Rule(antecedent=((error['DD'] & delta['SD'])), consequent=output['BDD'])
        rule48 = ctrl.Rule(antecedent=((error['DD'] & delta['MD'])), consequent=output['BDD'])


        system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
                                           rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19,
                                           rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29,
                                           rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39,
                                           rule40, rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48])

        sim = ctrl.ControlSystemSimulation(system)
        return


