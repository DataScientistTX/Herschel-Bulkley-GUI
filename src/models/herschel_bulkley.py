import numpy as np
from ..utils.curve_fitting import fit_curve

def ypl_function(y, tau_y, k, m):
    return tau_y + k * y**m

def pl_function(y, k, m):
    return k * y**m

def calculate_parameters(shear_stresses, shear_rates):
    popt, pcov, r_squared = fit_curve(shear_rates, shear_stresses, ypl_function)
    tau_y, k, m = popt

    if tau_y < 0:
        popt, pcov, r_squared = fit_curve(shear_rates, shear_stresses, pl_function)
        tau_y, k, m = 0, popt[0], popt[1]

    intervals = np.sqrt(np.diag(pcov))

    return {
        'tau_y': tau_y,
        'K': k,
        'm': m,
        'r_squared': r_squared
    }, {
        'tau_y': intervals[0] if tau_y > 0 else 0,
        'K': intervals[1] if tau_y > 0 else intervals[0],
        'm': intervals[2] if tau_y > 0 else intervals[1]
    }