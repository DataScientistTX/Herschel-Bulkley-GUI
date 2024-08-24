from PyQt5.QtWidgets import QDialog, QDoubleValidator
from PyQt5.QtCore import pyqtSlot
from .ui_main_window import Ui_Dialog
from ..models.herschel_bulkley import calculate_parameters
from ..utils.curve_fitting import fit_curve
import numpy as np

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_validators()
        self.connect_signals()

    def setup_validators(self):
        for line_edit in [self.ui.lineEditSigma600, self.ui.lineEditSigma300, 
                          self.ui.lineEditSigma200, self.ui.lineEditSigma100, 
                          self.ui.lineEditSigma6, self.ui.lineEditSigma3]:
            line_edit.setValidator(QDoubleValidator(0.99, 99.99, 2))

    def connect_signals(self):
        for line_edit in [self.ui.lineEditSigma600, self.ui.lineEditSigma300, 
                          self.ui.lineEditSigma200, self.ui.lineEditSigma100, 
                          self.ui.lineEditSigma6, self.ui.lineEditSigma3]:
            line_edit.textChanged.connect(self.on_text_changed)
        self.ui.pushButtonCalculate.clicked.connect(self.calculate_parameters)
        self.ui.pushButtonGraph.clicked.connect(self.update_graph)

    @pyqtSlot()
    def on_text_changed(self):
        all_filled = all(line_edit.text() for line_edit in 
                         [self.ui.lineEditSigma600, self.ui.lineEditSigma300, 
                          self.ui.lineEditSigma200, self.ui.lineEditSigma100, 
                          self.ui.lineEditSigma6, self.ui.lineEditSigma3])
        self.ui.pushButtonCalculate.setEnabled(all_filled)
        self.ui.pushButtonGraph.setEnabled(all_filled)

    def calculate_parameters(self):
        shear_rates = np.array([1021.98, 510.99, 341.66, 170.33, 10.22, 5.11])
        shear_stresses = np.array([
            float(self.ui.lineEditSigma600.text()),
            float(self.ui.lineEditSigma300.text()),
            float(self.ui.lineEditSigma200.text()),
            float(self.ui.lineEditSigma100.text()),
            float(self.ui.lineEditSigma6.text()),
            float(self.ui.lineEditSigma3.text())
        ]) * 1.066 * 0.4788

        params, intervals = calculate_parameters(shear_stresses, shear_rates)
        
        self.ui.lineEditTy.setText(f"{params['tau_y']:.3f} +/- {intervals['tau_y']:.2f}")
        self.ui.lineEditK.setText(f"{params['K']:.3f} +/- {intervals['K']:.2f}")
        self.ui.lineEditm.setText(f"{params['m']:.3f} +/- {intervals['m']:.2f}")
        self.ui.lineEditR2.setText(f"{params['r_squared']:.3f}")

    def update_graph(self):
        # Implementation for updating the graph
        pass