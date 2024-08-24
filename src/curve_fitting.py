from scipy.optimize import curve_fit
from scipy.stats import t
import numpy as np

def fit_curve(x, y, function, p0=None):
    popt, pcov = curve_fit(function, x, y, p0=p0)
    
    residuals = y - function(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)

    return popt, pcov, r_squared