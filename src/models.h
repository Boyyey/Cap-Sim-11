#ifndef MODELS_H
#define MODELS_H

typedef struct {
    char name[30];
    double capacitance;  // Farads
    double ESR;          // Ohms
    double leakage;      // A/V
    double temp_coeff;   // %/°C
} Capacitor;

// Function declarations
double calculate_charge_voltage(double V0, double R, double C, double t);
double calculate_discharge_voltage(double V0, double R, double C, double t);
double calculate_energy_stored(double C, double V);
double calculate_ESR_power_loss(double ESR, double I);
double calculate_temperature_effect(double C0, double temp_coeff, double T, double T0);
double simulate_leakage_decay(double V0, double leakage, double t);

#endif
