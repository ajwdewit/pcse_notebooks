import numpy as np

class PedotransferFunctionsWosten():

    def calculate_van_genuchten_parameters(self, C, D, S, OM, theta_r, topSoil):
        if(OM == 0):
            OM = 0.01
        dict_vg = {}
        dict_vg["alpha"] = self.calculate_alpha(C, D, S, OM, topSoil)
        dict_vg["n"] = self.calculate_n(C, D, S, OM, topSoil)
        dict_vg["lambda"] = self.calculate_lambda(C, D, S, OM, topSoil)
        dict_vg["k_sat"] = self.calculate_k_sat(C, D, S, OM, topSoil)
        dict_vg["theta_r"] = theta_r
        dict_vg["theta_s"] = self.calculate_theta_s(C, D, S, OM, topSoil)
        return dict_vg

    def calculate_alpha(self, C, D, S, OM, topSoil):
        t_alpha = self.calculate_transformed_alpha(C, D, S, OM, topSoil)
        alpha = np.exp(t_alpha)
        return alpha

    def calculate_n(self, C, D, S, OM, topSoil):
        t_n = self.calculate_transformed_n(C, D, S, OM, topSoil)
        n = np.exp(t_n) + 1
        return n

    def calculate_lambda(self, C, D, S, OM, topSoil):
        t_labda = self.calculate_transformed_lambda(C, D, S, OM, topSoil)
        labda = (10 * np.exp(t_labda) - 10) / (1 + np.exp(t_labda))
        return labda

    def calculate_k_sat(self,  C, D, S, OM, topSoil):
        t_k_sat = self.calculate_transformed_ksat( C, D, S, OM, topSoil)
        k_sat = np.exp(t_k_sat)
        return k_sat

    def calculate_theta_s(self, C, D, S, OM, topSoil):
        if(topSoil):
            TS = 1.
        else:
            TS = 0.
        theta_s = 0.7919 + 0.001691 * C - 0.29619 * D - 0.000001491 * S * S + 0.0000821 * OM * OM + 0.02427 * (1 / C) + 0.01113 * (1 / S) + \
                0.01472 * np.log(S) - 0.0000733 * OM * C - 0.000619 * D * C - 0.001183 * D * OM - 0.0001664 * topSoil * S
        return theta_s

    def calculate_transformed_alpha(self, C, D, S, OM, topSoil):
        if(topSoil):
            TS = 1.
        else:
            TS = 0.
        t_alpha = -14.96 + 0.03135 * C + 0.0351 * S + 0.646 * OM + 15.29 * D - 0.192 * topSoil - 4.671 * D * D - 0.000781 * C * C - \
                0.00687 * OM * OM + 0.0449 * (1 / OM) + 0.0663 * np.log(S) + 0.1482 * np.log(OM) - 0.04546 * D * S - 0.4852 * D * OM + 0.00673 * topSoil * C
        return t_alpha

    def calculate_transformed_n(self, C, D, S, OM, topSoil):
        if(topSoil):
            TS = 1.
        else:
            TS = 0.
        t_n = -25.23 - 0.02195 * C + 0.0074 * S - 0.1940 * OM + 45.5 * D - 7.24 * D * D + 0.0003658 * C * C + 0.002885 * OM * OM - 12.81 * (1 / D) - \
                0.1524 * (1 / S) - 0.01958 * (1 / OM) - 0.2876 * np.log(S) - 0.0709 * np.log(OM) - 44.6 * np.log(D) - 0.02264 * D * C + 0.0896 * D * OM + 0.00718 * topSoil * C
        return t_n

    def calculate_transformed_lambda(self, C, D, S, OM, topSoil):
        if(topSoil):
            TS = 1.
        else:
            TS = 0.
        t_lambda = 0.0202 + 0.0006193 * C * C - 0.001136 * OM * OM - 0.2316 * np.log(OM) - 0.03544 * D * C + 0.00283 * D * S + 0.0488 * D * OM;  
        return t_lambda

    def calculate_transformed_ksat(self, C, D, S, OM, topSoil):
        if(topSoil):
            TS = 1.
        else:
            TS = 0.
        t_k_sat = 7.755 + 0.0352 * S + 0.93 * topSoil - 0.967 * D * D - 0.000484 * C * C - 0.000322 * S * S + \
                0.001 * (1 / S) - 0.0748 * (1 / OM) - 0.643 * np.log(S) - 0.01398 * D * C - 0.1673 * D * OM + \
                0.02986 * topSoil * C - 0.03305 * topSoil * S
        return t_k_sat