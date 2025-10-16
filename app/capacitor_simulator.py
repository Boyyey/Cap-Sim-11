import os
import ctypes
from ctypes import CDLL, Structure, c_double, c_char, c_char_p, c_int, POINTER, c_void_p
import numpy as np

class CapacitorStruct(Structure):
    _fields_ = [
        ("name", c_char * 30),
        ("capacitance", c_double),
        ("ESR", c_double),
        ("leakage", c_double),
        ("temp_coeff", c_double)
    ]

class CapacitorSimulator:
    def __init__(self):
        # Get the directory of this file and build path to shared library
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)  # Go up one level to A_CapacitorSimulator

        # Determine library extension based on platform
        if os.name == 'nt':  # Windows
            lib_name = 'libcapacitor_simulator.dll'
        else:  # Unix-like systems
            lib_name = 'libcapacitor_simulator.so'

        lib_path = os.path.join(parent_dir, 'src', lib_name)

        # Check if library exists, if not try to build it
        if not os.path.exists(lib_path):
            self._build_library()

        try:
            self.lib = CDLL(lib_path)
            self._setup_function_signatures()
        except OSError as e:
            raise RuntimeError(f"Failed to load C library: {e}")

    def _build_library(self):
        """Build the C library if it doesn't exist"""
        # Get the root directory of the project
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Check if we're on Windows and adjust accordingly
        if os.name == 'nt':
            # On Windows, use the build script
            build_script = os.path.join(root_dir, 'build.bat')
            os.chdir(root_dir)
            result = os.system(f'"{build_script}"')
            if result != 0:
                raise RuntimeError("Failed to build C library using build.bat")
        else:
            # On Unix-like systems, build as shared object
            src_dir = os.path.join(root_dir, 'src')
            os.chdir(src_dir)
            result = os.system('make')
            if result != 0:
                raise RuntimeError("Failed to build C library using make")

    def _setup_function_signatures(self):
        """Set up ctypes function signatures"""

        # Function: create_capacitor
        self.lib.create_capacitor.argtypes = [c_char_p, c_double, c_double, c_double, c_double]
        self.lib.create_capacitor.restype = CapacitorStruct

        # Function: simulate_capacitor_behavior
        self.lib.simulate_capacitor_behavior.argtypes = [
            CapacitorStruct, c_double, c_double, c_double,
            POINTER(c_double), POINTER(c_double), c_int
        ]
        self.lib.simulate_capacitor_behavior.restype = None

        # Function: calculate_energy_efficiency
        self.lib.calculate_energy_efficiency.argtypes = [CapacitorStruct, c_double, c_double, c_double]
        self.lib.calculate_energy_efficiency.restype = c_double

        # Function: print_capacitor_info
        self.lib.print_capacitor_info.argtypes = [CapacitorStruct]
        self.lib.print_capacitor_info.restype = None

    def create_capacitor(self, name, capacitance, ESR, leakage, temp_coeff):
        """Create a capacitor structure"""
        return self.lib.create_capacitor(
            name.encode('utf-8'), capacitance, ESR, leakage, temp_coeff
        )

    def simulate_behavior(self, capacitor, resistance, voltage, temperature, time_steps):
        """Simulate capacitor charge/discharge behavior"""
        num_steps = len(time_steps)
        time_array = (c_double * num_steps)(*time_steps)
        voltage_array = (c_double * num_steps)()

        self.lib.simulate_capacitor_behavior(
            capacitor, resistance, voltage, temperature,
            time_array, voltage_array, num_steps
        )

        return np.array(voltage_array)

    def calculate_efficiency(self, capacitor, resistance, voltage, temperature):
        """Calculate energy efficiency"""
        return self.lib.calculate_energy_efficiency(
            capacitor, resistance, voltage, temperature
        )

    def print_capacitor_info(self, capacitor):
        """Print capacitor information"""
        self.lib.print_capacitor_info(capacitor)

# Global simulator instance
_simulator = None

def get_simulator():
    """Get or create the global simulator instance"""
    global _simulator
    if _simulator is None:
        _simulator = CapacitorSimulator()
    return _simulator
