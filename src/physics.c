#include "models.h"
#include <math.h>

double calculate_charge_voltage(double V0, double R, double C, double t) {
    // Vc(t) = V0 * (1 - e^(-t/RC))
    double tau = R * C;
    return V0 * (1.0 - exp(-t / tau));
}

double calculate_discharge_voltage(double V0, double R, double C, double t) {
    // Vc(t) = V0 * e^(-t/RC)
    double tau = R * C;
    return V0 * exp(-t / tau);
}

double calculate_energy_stored(double C, double V) {
    // E = 1/2 * C * V^2
    return 0.5 * C * V * V;
}

double calculate_ESR_power_loss(double ESR, double I) {
    // P = I^2 * ESR
    return I * I * ESR;
}

double calculate_temperature_effect(double C0, double temp_coeff, double T, double T0) {
    // C(T) = C0 * (1 + α*(T - T0))
    return C0 * (1.0 + temp_coeff * (T - T0));
}

double simulate_leakage_decay(double V0, double leakage, double t) {
    // Simplified leakage model: V(t) = V0 * e^(-leakage*t)
    // More accurate would be: dV/dt = -leakage * V
    return V0 * exp(-leakage * t);
}
