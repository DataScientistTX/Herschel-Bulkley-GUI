# Herschel-Bulkley Calculator

## Overview

The Herschel-Bulkley Calculator is a Python application with a graphical user interface (GUI) designed for calculating Herschel-Bulkley parameters of non-Newtonian drilling or well completion fluids. It provides an easy-to-use interface for inputting shear stress data and visualizing the results.

## Features

- User-friendly GUI for data input
- Calculation of Herschel-Bulkley parameters (τy, K, m)
- Visualization of shear stress vs. shear rate curves
- Error handling and input validation
- Exportable results and graphs

## Installation

1. Ensure you have Python 3.7 or newer installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/herschel-bulkley-calculator.git
   cd herschel-bulkley-calculator
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Activate your virtual environment if it's not already activated.
2. Run the application:
   ```
   python -m src.main
   ```
3. Input the dial readings for different shear rates in the GUI.
4. Click the "Calculate" button to compute the Herschel-Bulkley parameters.
5. Click the "Plot" button to visualize the shear stress vs. shear rate curve.

## Project Structure

```
herschel_bulkley_calculator/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── mpl_widget.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── herschel_bulkley.py
│   └── utils/
│       ├── __init__.py
│       └── curve_fitting.py
├── tests/
│   ├── __init__.py
│   ├── test_herschel_bulkley.py
│   └── test_curve_fitting.py
├── resources/
│   └── codalogo.png
├── requirements.txt
└── README.md
```

## Development

To set up the development environment:

1. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```
2. Run tests:
   ```
   pytest tests/
   ```
3. Check code style:
   ```
   flake8 src/
   ```
4. Format code:
   ```
   black src/
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PyQt5 for the GUI framework
- Matplotlib for plotting capabilities
- NumPy and SciPy for numerical computations

## Contact

For any queries or suggestions, please open an issue on the GitHub repository.