# Architecture Documentation

## System Overview

The Capacitor Behavior Simulator is a hybrid C/Python application designed to provide accurate physics-based simulation of capacitor behavior. The system combines high-performance C code for computational accuracy with Python's Streamlit framework for interactive visualization.

## Architecture Components

### 1. C Physics Engine (`src/`)

#### Core Components
- **`models.h`**: Header file defining the `Capacitor` struct and function prototypes
- **`physics.c`**: Implementation of fundamental physics calculations
- **`simulator.c`**: High-level simulation functions and capacitor management
- **`Makefile`**: Build system for creating shared library

#### Capacitor Structure
```c
typedef struct {
    char name[30];       // Capacitor type name
    double capacitance;  // Capacitance in Farads
    double ESR;          // Equivalent Series Resistance in Ohms
    double leakage;      // Leakage current in A/V
    double temp_coeff;   // Temperature coefficient in %/°C
} Capacitor;
```

#### Key Functions
- `calculate_charge_voltage(V0, R, C, t)`: RC charging equation
- `calculate_discharge_voltage(V0, R, C, t)`: RC discharging equation
- `calculate_energy_stored(C, V)`: Energy storage calculation
- `calculate_temperature_effect(C0, temp_coeff, T, T0)`: Temperature compensation
- `simulate_capacitor_behavior(...)`: Complete charge/discharge cycle simulation

### 2. Python Frontend (`app/`)

#### Core Files
- **`main.py`**: Main Streamlit application with UI and simulation orchestration
- **`capacitor_simulator.py`**: Python wrapper for C library integration
- **`requirements.txt`**: Python dependencies
- **`data/capacitor_specs.csv`**: Capacitor specification database

#### Streamlit Interface Features
- **Interactive Controls**: Sliders for resistance, voltage, temperature, simulation time
- **Capacitor Selection**: Dropdown for different capacitor types
- **Tabbed Interface**: Organized visualization across three analysis modes
- **Real-time Updates**: Dynamic recalculation based on parameter changes

#### Visualization Components
1. **Charge/Discharge Curves**: Matplotlib plots of voltage vs time
2. **Energy Analysis**: Pie charts showing energy distribution
3. **Temperature Effects**: Line plots of capacitance vs temperature

### 3. Data Flow Architecture

```
User Input (Streamlit UI)
        ↓
Parameter Processing (Python)
        ↓
C Library Integration (ctypes)
        ↓
Physics Calculations (C Engine)
        ↓
Result Processing (Python)
        ↓
Visualization (Matplotlib)
        ↓
Display (Streamlit)
```

### 4. Integration Layer

#### ctypes Integration
The C library is compiled as a shared object and loaded via Python's ctypes module:

```python
class CapacitorSimulator:
    def __init__(self):
        # Load shared library
        self.lib = CDLL('libcapacitor_simulator.so')
        # Set up function signatures
        self._setup_function_signatures()

    def simulate_behavior(self, capacitor, R, V0, T, time_steps):
        # Call C function via ctypes
        return self.lib.simulate_capacitor_behavior(...)
```

#### Error Handling
- **Graceful Degradation**: Falls back to Python simulation if C library unavailable
- **Build Automation**: Automatic compilation of C library if missing
- **Cross-platform Support**: Handles Windows DLL vs Unix shared object differences

### 5. Physics Model Details

#### RC Circuit Modeling
The system models capacitor behavior using standard electrical engineering equations:

**Charging Phase:**
```
Vc(t) = V₀ × (1 - e^(-t/RC))
I(t) = (V₀/R) × e^(-t/RC)
```

**Discharging Phase:**
```
Vc(t) = V₀ × e^(-t/RC)
I(t) = -(V₀/R) × e^(-t/RC)
```

#### Energy Calculations
- **Stored Energy**: E = ½CV²
- **ESR Losses**: P_ESR = I² × ESR
- **Leakage Losses**: P_leakage = V × I_leakage

#### Temperature Effects
Temperature compensation using linear coefficient:
```
C(T) = C₀ × (1 + α × (T - T₀))
```

### 6. Performance Considerations

#### C Optimization
- Compiled C code for numerical computation speed
- Minimal function call overhead via ctypes
- Efficient array operations for time-series data

#### Memory Management
- Proper ctypes memory handling for array parameters
- Automatic cleanup of temporary objects
- Efficient data structures for simulation results

### 7. Extensibility

#### Future Enhancement Points
1. **AC Analysis**: Add frequency domain analysis
2. **Multi-Capacitor Networks**: Support series/parallel configurations
3. **Advanced Materials**: Include dielectric absorption modeling
4. **Machine Learning**: Add capacitor type prediction from behavior curves

#### Modular Design
- Clear separation between physics engine and UI
- Independent function implementations for easy testing
- Configurable simulation parameters

## Deployment Architecture

### Local Development
```
A_CapacitorSimulator/
├── src/           # C source code
├── app/           # Python application
└── docs/          # Documentation
```

### Runtime Dependencies
- **Python**: Streamlit, NumPy, Matplotlib, Pandas
- **C Compiler**: For building physics engine
- **ctypes**: For C-Python interoperability

### Cross-platform Compatibility
- **Windows**: Builds as DLL with Visual Studio or MinGW
- **Linux/macOS**: Builds as shared object with GCC
- **Python**: Compatible with 3.8+ across all platforms

## Testing Strategy

### Unit Tests
- Individual physics function validation
- C library function testing
- Python wrapper functionality verification

### Integration Tests
- End-to-end simulation workflow
- UI component interaction testing
- Cross-platform compatibility validation

### Performance Tests
- Large dataset simulation benchmarking
- Memory usage profiling
- Real-time interaction responsiveness

## Security Considerations

- **No External Dependencies**: Self-contained simulation engine
- **Input Validation**: Parameter range checking in UI
- **Safe C Integration**: Proper ctypes usage prevents buffer overflows
- **No Network Operations**: Pure computational tool with no external API calls
