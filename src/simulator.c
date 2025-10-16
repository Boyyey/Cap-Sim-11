#include "models.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to create a capacitor from specifications
Capacitor create_capacitor(const char* name, double capacitance, double ESR, double leakage, double temp_coeff) {
    Capacitor cap;
    strncpy(cap.name, name, sizeof(cap.name) - 1);
    cap.name[sizeof(cap.name) - 1] = '\0';
    cap.capacitance = capacitance;
    cap.ESR = ESR;
    cap.leakage = leakage;
    cap.temp_coeff = temp_coeff;
    return cap;
}

// Function to simulate charge/discharge cycle and return results
void simulate_capacitor_behavior(Capacitor cap, double R, double V0, double temperature,
                                double time_steps[], double voltages[], int num_steps) {
    // Apply temperature effect to capacitance
    double C_effective = calculate_temperature_effect(cap.capacitance, cap.temp_coeff, temperature, 25.0);

    for (int i = 0; i < num_steps; i++) {
        double t = time_steps[i];

        // Charging phase (first half of time)
        if (t <= time_steps[num_steps-1] / 2.0) {
            voltages[i] = calculate_charge_voltage(V0, R, C_effective, t);
        } else {
            // Discharging phase (second half of time)
            double discharge_time = t - time_steps[num_steps-1] / 2.0;
            voltages[i] = calculate_discharge_voltage(V0, R, C_effective, discharge_time);
        }
    }
}

// Function to calculate energy efficiency
double calculate_energy_efficiency(Capacitor cap, double R, double V0, double temperature) {
    double C_effective = calculate_temperature_effect(cap.capacitance, cap.temp_coeff, temperature, 25.0);

    // Energy stored in capacitor
    double energy_stored = calculate_energy_stored(C_effective, V0);

    // More realistic ESR loss calculation
    // For exponential charging, average current is V0/(2R)
    double tau = R * C_effective;
    double avg_current = V0 / (2.0 * R);  // Average current during charging
    double energy_lost_ESR = calculate_ESR_power_loss(cap.ESR, avg_current) * tau;

    // Leakage losses (very small for most capacitors)
    // Leakage current is roughly constant at average voltage
    double avg_voltage = V0 / 2.0;  // Average voltage during charging
    double leakage_current = cap.leakage * avg_voltage;
    double energy_lost_leakage = leakage_current * V0 * tau;  // Conservative estimate

    // Additional realistic losses for real-world capacitors
    double dielectric_losses = energy_stored * 0.03;  // 3% dielectric losses
    double plate_losses = energy_stored * 0.05;       // 5% plate/terminal losses
    double self_discharge_losses = energy_stored * 0.02;  // 2% self-discharge

    double total_energy_lost = energy_lost_ESR + energy_lost_leakage + dielectric_losses + plate_losses + self_discharge_losses;

    if (energy_stored + total_energy_lost > 0) {
        return (energy_stored / (energy_stored + total_energy_lost)) * 100.0;
    }

    return 0.0;
}

// Function to print capacitor information
void print_capacitor_info(Capacitor cap) {
    printf("Capacitor: %s\n", cap.name);
    printf("Capacitance: %.2e F\n", cap.capacitance);
    printf("ESR: %.3f Ω\n", cap.ESR);
    printf("Leakage: %.2e A/V\n", cap.leakage);
    printf("Temperature Coefficient: %.3f %%/°C\n", cap.temp_coeff);
}
