from scipy import constants
import numpy as np

M_w = 18.01528e-3 # kg/m3 Molecular mass of water
rho_ice = 916.7 # kg/m3, ice volumic mass

def check_float(*argv):
    for arg in argv:
        if type(arg) != float:
            raise TypeError("Argument passed to parametrization module should be float")

def gamma_vw(T):
    '''
    Surface tension of the vapour–water interface, in J/m2
    '''
    Tc = 647.096 # K
    mu = 1.256
    B = 0.2358 # J/m2
    b = -0.625
    tau = 1 - T/Tc

    return B * (tau**mu) * (1 + b * tau)

def gamma_iw(T,P):
    '''
    Surface tension between ice and water, in Jm-2
    '''
    return 0.03 - 0.18e-3 * (273.15 - T) + 4.99e-5 * P - 1.37e-7 * P**2 + 1.53e-10 * P**3 + 1.40e-12 * P**4 - 2.97e-15 * P**5 - 3.05e-17 * P**6

def gamma_vi(T):
    return gamma_vw(T) + gamma_iw(T, P=0.1) # cf Marcolli 2020, P0=0.1 MPa

def kappa(T):
    '''
    Compressibility of liquid water, in MPa-1
    '''
    return 0.487 - 0.04368 * (T - 273.15) + 0.00007235 * (T - 273.15)**2

def dKappa_dP(T):
    '''
    Partial derivative of water compressibility with respect to pressure, in MPa-2
    '''
    return -0.0003805 + 6.639e6 * (T - 273.15) - 9.688e8 * (T - 273.15)**2

def rho_w_P0(T):
    '''
    Liquid water density at P0 = 0.1 MPa, given in kg/m3
    '''
    return 1864.3535 - 72.5821489 * T + 2.5194368 * T**2 - 0.049000203 * T**3 + 5.860253e-4 * T**4 - 4.5055151e-6 * T**5 + 2.2616353e-8 * T**6 - 7.3484974e-11 * T**7 + 1.4862784e-13 * T**8 - 1.6984748e-16 * T**9 + 8.3699379e-20 * T**10

def rho_w(T, P):
    return rho_w_P0(T) + kappa(T) ##### Pas fini

def nu_w_P0(T):
    '''
    Molecular volume of water in m3
    '''
    global M_w
    return M_w / (constants.Avogadro * rho_w_P0(T))

def r_m(T, S_w):
    '''
    Curvature radius of meniscus (Kelvin equation), in m
    T: Temperature in K
    S_w : Relative humidity approx between 0 and 1
    '''
    return 2 * gamma_vw(T) * nu_w_P0(T) / (constants.k * T * np.log(S_w))

def nu_i_P0(T):
    '''
    Molecular volume of ice, in m3
    '''
    T_red = (T - 273.15) / 273.15
    return M_w / (constants.Avogadro * rho_ice) / (1 - 0.05294 * T_red - 0.05637 * T_red**2 - 0.002913 * T_red**3)

def ln_p_i_P0(T):
    return 9.550426 - 5723.265 / T + 3.53068 * np.log(T) - 0.00728332 * T

def ln_p_w_P0(T):
    return 54.842763 - 6763.22 / T - 4.21 * np.log(T) + 0.000367 * T + np.tanh(0.0415 * (T - 218.8)) * (53.878 - 1331.22 / T - 9.44523 * np.log(T) + 0.014025 * T)

def S_w2S_i_P0(T, S_w):
    return np.exp(np.log(S_w) + ln_p_w_P0(T) - ln_p_i_P0(T))

def S_i2S_w_P0(T, S_i):
    return np.exp(np.log(S_i) + ln_p_i_P0(T) - ln_p_w_P0(T))

def S_w_changeTemp(newTemp, oldTemp, S_w):
    return np.exp(np.log(S_w) + ln_p_w_P0(oldTemp) - ln_p_w_P0(newTemp))

def Si2p(T, Si):
    return np.exp(np.log(Si) + ln_p_i_P0(T))# Parametrization already in MPa, no need for * 1e6

def p2Si(T, p):
    return p * 1e-6 / np.exp(ln_p_i_P0(T)) # Parametrization in MPa

def T_F(Psi):
    return 272.55 / 22.452 * np.log(Psi / 611.15) * (1 - np.log(Psi / 611.15)/22.452)

def T_F_MurphyKoop2005(ln_p):
    return (1.514625 * ln_p + 6190.134) / (29.12 - ln_p)

def ln_p_MurphyKoop2005(T_F):
    return (29.120 * T_F - 6190.134) / (1.814625 + T_F)

def dewPoint_S_w(T):
    return 611.21 * np.exp(17.9662 * T/(T + 247.15)) * 1e-6 / np.exp(ln_p_w_P0(T))# Parametrization in MPa

def frostPoint_S_i(T):
    return 611.15 * np.exp(22.452 * T / (T + 272.15)) * 1e-6 / np.exp(ln_p_i_P0(T)) # Parametrization in MPa

def cos_theta_iw(T):
    return (gamma_vw(T) - gamma_iw(T,P=0.1)) / gamma_vi(T)

def criticalOutOfPoresGrowthRadius(T, S_i):
    return 4 * gamma_vi(T) * nu_i_P0(T) * cos_theta_iw(T) / (constants.k * T * np.log(S_i))

def Delta_mu_iw(T,Delta_P):
    return Delta_P * nu_i_P0(T) - Delta_P ######## Pas fini
