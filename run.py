#Importing the libraries
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from HerschelBulkleyCalculator import *
import pandas as pd 
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats.distributions import  t
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import random
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#Define the Herschel Bulkley (Yield Power Law) function.
def YPLfunction(y, tauy, K, m):
    return tauy + K*y**m

def PLfunction(y, K, m):
    return  K*y**m

def NEWTfunction(y, K):
    return  K*y

#Generate the class for signals and slots.
class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #Validate the input is only doubles. Will not accept the entry of text.
        self.ui.lineEditSigma600.setValidator(QDoubleValidator(0.99,99.99,2))
        self.ui.lineEditSigma300.setValidator(QDoubleValidator(0.99,99.99,2))
        self.ui.lineEditSigma200.setValidator(QDoubleValidator(0.99,99.99,2))
        self.ui.lineEditSigma100.setValidator(QDoubleValidator(0.99,99.99,2))
        self.ui.lineEditSigma6.setValidator(QDoubleValidator(0.99,99.99,2))
        self.ui.lineEditSigma3.setValidator(QDoubleValidator(0.99,99.99,2))

        #Calls on_text_changed function when all the texts have changed to enable the push button later on.
        self.ui.lineEditSigma600.textChanged.connect(self.on_text_changed)
        self.ui.lineEditSigma300.textChanged.connect(self.on_text_changed)
        self.ui.lineEditSigma200.textChanged.connect(self.on_text_changed)
        self.ui.lineEditSigma100.textChanged.connect(self.on_text_changed)
        self.ui.lineEditSigma6.textChanged.connect(self.on_text_changed)
        self.ui.lineEditSigma3.textChanged.connect(self.on_text_changed)
        self.ui.pushButtonCalculate.clicked.connect(self.dispParameterResults)
        self.ui.pushButtonGraph.clicked.connect(self.update_graph)
        
        self.show()      
 
    #Function that enables push putton when all the texts are filled.
    @QtCore.pyqtSlot()
    def on_text_changed(self):
        self.ui.pushButtonCalculate.setEnabled(bool(self.ui.lineEditSigma600.text()) and bool(self.ui.lineEditSigma300.text()) and bool(self.ui.lineEditSigma200.text()) and bool(self.ui.lineEditSigma100.text()) and bool(self.ui.lineEditSigma6.text()) and bool(self.ui.lineEditSigma3.text()))
        self.ui.pushButtonGraph.setEnabled(bool(self.ui.lineEditSigma600.text()) and bool(self.ui.lineEditSigma300.text()) and bool(self.ui.lineEditSigma200.text()) and bool(self.ui.lineEditSigma100.text()) and bool(self.ui.lineEditSigma6.text()) and bool(self.ui.lineEditSigma3.text()))

    def dispParameterResults(self):

        #Pulling sigma readings from the GUI.
        sigma600_1=self.ui.lineEditSigma600.text()
        sigma300_1=self.ui.lineEditSigma300.text()
        sigma200_1=self.ui.lineEditSigma200.text()
        sigma100_1=self.ui.lineEditSigma100.text()
        sigma6_1=self.ui.lineEditSigma6.text()
        sigma3_1=self.ui.lineEditSigma3.text()
        
        sigma600=float(sigma600_1)*1.066*0.4788
        sigma300=float(sigma300_1)*1.066*0.4788
        sigma200=float(sigma200_1)*1.066*0.4788
        sigma100=float(sigma100_1)*1.066*0.4788
        sigma6=float(sigma6_1)*1.066*0.4788
        sigma3=float(sigma3_1)*1.066*0.4788

        #Shear stress conversion and rheological property calculations.
        shearstress = [sigma600,sigma300,sigma200,sigma100,sigma6,sigma3]
        y = [1021.98,510.99,341.66,170.33,10.22,5.11]
        
        popt, pcov = curve_fit(YPLfunction,y,shearstress)
        residuals = shearstress- YPLfunction(y, popt[0],popt[1],popt[2])
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((shearstress-np.mean(shearstress))**2)
        r_squared = 1 - (ss_res / ss_tot)
        A = popt[0]
        B = popt[1]
        C = popt[2]

        #Confidence interval calculations
        alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
        n = len(y)    # number of data points
        p = len(popt) # number of parameters
        dof = max(0, n - p) # number of degrees of freedom
        # student-t value for the dof and confidence level
        tval = t.ppf(1.0-alpha/2., dof) 

        #=/- data for constants - interval[0] for tauy, interval[1] for K, interval[2] to m
        interval = []
        for i, p,var in zip(range(n), popt, np.diag(pcov)):
            sigma = var**0.5
            interval.append(sigma*tval)

        #Final rounding on the calculated properties.        
        tauy = round(A,3)
        K = round(B,3)
        m = round(C,3)
        r2 = round(r_squared,3)

        tauyint = round(interval[0],2)
        Kint = round(interval[1],2)
        mint = round(interval[2],2)

        if tauy < 0:
            popt, pcov = curve_fit(PLfunction,y,shearstress)
            residuals = shearstress- PLfunction(y, popt[0],popt[1])
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((shearstress-np.mean(shearstress))**2)
            r_squared = 1 - (ss_res / ss_tot)
            A = 0
            B = popt[0]
            C = popt[1]

            #Confidence interval calculations
            alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
            n = len(y)    # number of data points
            p = len(popt) # number of parameters
            dof = max(0, n - p) # number of degrees of freedom
            # student-t value for the dof and confidence level
            tval = t.ppf(1.0-alpha/2., dof) 

            #=/- data for constants - interval[0] for K, interval[1] for m
            interval = []
            for i, p,var in zip(range(n), popt, np.diag(pcov)):
                sigma = var**0.5
                interval.append(sigma*tval)
  
            tauy = round(A,3)
            K = round(B,3)
            m = round(C,3)
            r2 = round(r_squared,3)

            tauyint = 0
            Kint = round(interval[0],2)
            mint = round(interval[1],2)

        #Pushing the results back to GUI
        self.ui.lineEditTy.setText(str(tauy)+" +/- " + str(tauyint))
        self.ui.lineEditK.setText(str(K)+" +/- " + str(Kint))
        self.ui.lineEditm.setText(str(m)+" +/- " + str(mint))
        self.ui.lineEditR2.setText(str(r2))

    def update_graph(self):
        y = [1021.98,510.99,341.66,170.33,10.22,5.11]
        y2 = [1040,800,700,510.99,341.66,250,170.33,150,130,80,50,30,10.22,5.11,0]
        sigma600_1=self.ui.lineEditSigma600.text()
        sigma300_1=self.ui.lineEditSigma300.text()
        sigma200_1=self.ui.lineEditSigma200.text()
        sigma100_1=self.ui.lineEditSigma100.text()
        sigma6_1=self.ui.lineEditSigma6.text()
        sigma3_1=self.ui.lineEditSigma3.text()
        
        sigma600=float(sigma600_1)*1.066*0.4788
        sigma300=float(sigma300_1)*1.066*0.4788
        sigma200=float(sigma200_1)*1.066*0.4788
        sigma100=float(sigma100_1)*1.066*0.4788
        sigma6=float(sigma6_1)*1.066*0.4788
        sigma3=float(sigma3_1)*1.066*0.4788

        shearstress = [sigma600,sigma300,sigma200,sigma100,sigma6,sigma3]
        popt, pcov = curve_fit(YPLfunction,y,shearstress)
        A = popt[0]
        B = popt[1]
        C = popt[2]

        tauy = round(A,3)
        K = round(B,3)
        m = round(C,3)
      
        shearcalc = tauy + K*y2**m
        #Shear stress conversion and rheological property calculations.
        
        self.ui.MplWidget.canvas.ax.clear()
        self.ui.MplWidget.canvas.ax.scatter(y, shearstress,color='r')
        self.ui.MplWidget.canvas.ax.plot(y2, shearcalc,color='b')
        self.ui.MplWidget.canvas.ax.legend(('Calculated', 'Measured'),loc='upper left')
        self.ui.MplWidget.canvas.ax.set_title('Shear Stress vs Shear Rate')
        self.ui.MplWidget.canvas.ax.set_xlabel('Shear Rate (1/s)')
        self.ui.MplWidget.canvas.ax.set_ylabel('Shear Stress (Pa)')
        self.ui.MplWidget.canvas.ax.set_xlim(0,max(y)+10)
        self.ui.MplWidget.canvas.ax.set_ylim(0,max(shearstress)+2)
        self.ui.MplWidget.canvas.draw()

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
