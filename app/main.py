import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from ctypes import CDLL, Structure, c_double, c_char, c_char_p, c_int, POINTER
from capacitor_simulator import get_simulator
# Capacitor information dictionary with Persian explanations and image paths
capacitor_info = {
    "Ceramic": {
        "history": "اولین خازن‌های سرامیکی در دهه ۱۹۵۰ ساخته شدند. این خازن‌ها به دلیل هزینه پایین و اندازه کوچک به سرعت در صنعت الکترونیک محبوب شدند و نقش مهمی در توسعه مدارهای مدرن ایفا کردند.",
        "applications": "در مدارهای الکترونیکی به عنوان خازن‌های فیلتر و کوپلینگ استفاده می‌شوند. این خازن‌ها معمولاً در مدارهای RF، صوتی، و دیجیتال به کار می‌روند و برای حذف نویز و اتصال سیگنال‌ها بین مراحل مختلف مدار ضروری هستند.",
        "why_exists": "به دلیل نیاز به خازن‌هایی با ظرفیت بالا در حجم کوچک و قیمت مناسب، خازن‌های سرامیکی طراحی شدند تا جایگزینی مقرون‌به‌صرفه برای خازن‌های سنتی باشند و در تجهیزات الکترونیکی کوچک جای بگیرند.",
        "pros": "ظرفیت بالا نسبت به اندازه، قیمت مناسب، پایداری خوب در دماهای مختلف، و مقاومت بالا در برابر ارتعاشات.",
        "cons": "حساس به دما و ولتاژ، ممکن است در ولتاژهای بالا دچار شکست شوند، و ظرفیت آن‌ها می‌تواند با تغییرات دما تغییر کند.",
        "image": "../assets/ceramic-capacitor.webp"
    },
    "Electrolytic": {
        "history": "خازن‌های الکترولیتی در دهه ۱۹۲۰ معرفی شدند و به سرعت در بازار الکترونیک جا افتادند. این خازن‌ها تحول بزرگی در ذخیره انرژی الکتریکی ایجاد کردند و پایه‌گذار منابع تغذیه مدرن شدند.",
        "applications": "در منابع تغذیه، مدارهای DC، و سیستم‌های ذخیره انرژی استفاده می‌شوند. آن‌ها برای صاف کردن ولتاژ و ذخیره انرژی در مدارهای الکترونیکی بزرگ مانند آمپلی‌فایرها و تجهیزات صنعتی ضروری هستند.",
        "why_exists": "برای تأمین نیاز به ظرفیت بالا در حجم کوچک و قیمت مناسب طراحی شدند، تا بتوانند انرژی زیادی را در فضاهای محدود ذخیره کنند و در تجهیزات الکترونیکی بزرگ استفاده شوند.",
        "pros": "ظرفیت بسیار بالا، قیمت مناسب برای ظرفیت‌های بزرگ، و عملکرد خوب در ولتاژهای پایین.",
        "cons": "حساس به قطبیت (باید با جهت درست نصب شوند)، عمر محدود (معمولاً ۱۰۰۰ تا ۵۰۰۰ ساعت)، و ممکن است در دماهای بالا نشت کنند یا منفجر شوند.",
        "image": "../assets/electrolytic-capacitor.png"
    },
    "Film": {
        "history": "خازن‌های فیلمی در دهه ۱۹۶۰ به بازار آمدند و به دلیل کیفیت بالا به سرعت محبوب شدند. این خازن‌ها از مواد پلاستیکی ساخته شدند و استاندارد جدیدی برای ثبات و دقت ایجاد کردند.",
        "applications": "در مدارهای صوتی، فیلترها، و تجهیزات پزشکی استفاده می‌شوند. آن‌ها برای مدارهای حساس که نیاز به دقت بالا دارند، مانند فیلترهای صوتی و تجهیزات اندازه‌گیری، ایده‌آل هستند.",
        "why_exists": "برای ارائه ثبات و کیفیت بالا در مدارهای حساس طراحی شدند، جایی که تغییرات کوچک در ظرفیت می‌تواند عملکرد سیستم را تحت تأثیر قرار دهد.",
        "pros": "پایداری عالی، عدم حساسیت به دما، عمر طولانی، و عملکرد خوب در فرکانس‌های بالا.",
        "cons": "ظرفیت پایین‌تر نسبت به خازن‌های الکترولیتی، قیمت بالاتر، و اندازه بزرگ‌تر برای ظرفیت‌های مشابه.",
        "image": "../assets/film-capacitor.jpg"
    },
    "Tantalum": {
        "history": "خازن‌های تانتالی در دهه ۱۹۵۰ معرفی شدند و به سرعت در بازار الکترونیک جا افتادند. این خازن‌ها از فلز تانتالم ساخته شدند و برای کاربردهای خاص طراحی شدند.",
        "applications": "در مدارهای RF، فیلترها، و تجهیزات هوافضا استفاده می‌شوند. آن‌ها برای مدارهای حساس و کوچک مانند تلفن‌های همراه و تجهیزات پزشکی ضروری هستند.",
        "why_exists": "برای ارائه ظرفیت بالا در اندازه کوچک طراحی شدند، تا بتوانند در تجهیزات الکترونیکی کوچک و حساس استفاده شوند و عملکرد بالایی ارائه دهند.",
        "pros": "پایداری بالا، اندازه کوچک، و عملکرد خوب در ولتاژهای بالا.",
        "cons": "قیمت بالا، حساس به ولتاژ (ممکن است در صورت اضافه‌ولتاژ بسوزند)، و نیاز به مراقبت در نصب.",
        "image": "../assets/tantalum-capacitor.jpg"
    },
    "Mica": {
        "history": "خازن‌های میکا از اوایل قرن ۲۰ استفاده می‌شدند و به دلیل دقت بالا محبوب شدند. این خازن‌ها از ورقه‌های میکا ساخته شدند و پایه‌گذار خازن‌های دقیق شدند.",
        "applications": "در مدارهای RF، فیلترهای دقیق، و تجهیزات اندازه‌گیری استفاده می‌شوند. آن‌ها برای مدارهایی که نیاز به دقت بالا دارند، مانند رادارها و تجهیزات ارتباطی، ضروری هستند.",
        "why_exists": "برای ارائه دقت بالا و پایداری طراحی شدند، جایی که حتی کوچک‌ترین تغییرات در ظرفیت می‌تواند مشکل‌ساز باشد.",
        "pros": "پایداری فوق‌العاده، دقت بالا، و عملکرد خوب در دماهای مختلف.",
        "cons": "قیمت بالاتر، ظرفیت پایین، و اندازه بزرگ‌تر برای ظرفیت‌های مشابه.",
        "image": "../assets/mica-capacitor.png"
    }
}

# Load capacitor specifications
@st.cache_data
def load_capacitor_data():
    return pd.read_csv('data/capacitor_specs.csv')

# C structure definition for ctypes
class CapacitorStruct(Structure):
    _fields_ = [
        ("name", c_char * 30),
        ("capacitance", c_double),
        ("ESR", c_double),
        ("leakage", c_double),
        ("temp_coeff", c_double)
    ]

def display_capacitor_info(capacitor_type):
    """Display Persian information and image for the selected capacitor type"""
    if capacitor_type in capacitor_info:
        info = capacitor_info[capacitor_type]
        
        # Display image
        image_path = info["image"]
        if os.path.exists(image_path):
            st.image(image_path, caption=f"تصویر خازن {capacitor_type}", use_column_width=True)
        else:
            st.warning(f"تصویر برای خازن {capacitor_type} یافت نشد.")
        
        # Display information in an organized layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### تاریخچه")
            st.write(info["history"])
            
            st.markdown(f"### کاربردها")
            st.write(info["applications"])
        
        with col2:
            st.markdown(f"### چرا وجود دارند")
            st.write(info["why_exists"])
            
            st.markdown(f"### مزایا")
            st.write(info["pros"])
            
            st.markdown(f"### معایب")
            st.write(info["cons"])
    else:
        st.error(f"اطلاعات برای خازن {capacitor_type} موجود نیست.")

def main():
    st.title("⚡ Capacitor Behavior Simulator")
    st.markdown("Simulate and visualize how different capacitors behave in various conditions.")

    # Load capacitor data
    df = load_capacitor_data()

    # Initialize C library
    try:
        simulator = get_simulator()
        c_library_available = True
    except RuntimeError as e:
        st.warning(f"C library not available: {e}. Using simplified Python simulation.")
        c_library_available = False
        simulator = None

    # Sidebar controls
    st.sidebar.header("Simulation Parameters")

    # Capacitor selection
    capacitor_type = st.sidebar.selectbox(
        "Select Capacitor Type",
        df['Type'].tolist(),
        help="Choose the type of capacitor to simulate"
    )

    # Get selected capacitor specs
    cap_data = df[df['Type'] == capacitor_type].iloc[0]

    # Simulation parameters
    resistance = st.sidebar.slider(
        "Resistance (Ω)",
        min_value=1.0,
        max_value=1000.0,
        value=100.0,
        step=10.0,
        help="Resistance in the RC circuit"
    )

    voltage = st.sidebar.slider(
        "Input Voltage (V)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=1.0,
        help="Initial voltage for charging"
    )

    temperature = st.sidebar.slider(
        "Temperature (°C)",
        min_value=-40.0,
        max_value=125.0,
        value=25.0,
        step=5.0,
        help="Operating temperature"
    )

    # Time range for simulation
    time_range = st.sidebar.slider(
        "Simulation Time (s)",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="Total time for charge/discharge cycle"
    )

    # Create time array
    num_points = 200
    time_steps = np.linspace(0, time_range, num_points)

    # Display capacitor information
    st.header(f"Capacitor: {capacitor_type}")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Capacitance", f"{cap_data['Capacitance (µF)']} µF")
        st.metric("ESR", f"{cap_data['ESR (Ω)']} Ω")

    with col2:
        st.metric("Leakage", f"{cap_data['Leakage (µA/V)']} µA/V")
        st.metric("Temp. Coefficient", f"{cap_data['TempCoeff (%/°C)']} %/°C")

    # Placeholder for simulation results
    st.header("Simulation Results")

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Charge/Discharge Curve", "Energy Analysis", "Temperature Effects", "3D Analysis", "اطلاعات/Info"])

    with tab1:
        st.subheader("Charge and Discharge Behavior")
        simulate_charge_discharge(cap_data, resistance, voltage, temperature, time_steps, simulator, c_library_available)

    with tab2:
        st.subheader("Energy Storage Efficiency")
        simulate_energy_analysis(cap_data, resistance, voltage, temperature, simulator, c_library_available)

    with tab3:
        st.subheader("Temperature Effects")
        simulate_temperature_effects(cap_data, resistance, voltage, time_steps, temperature, simulator, c_library_available)

    with tab4:
        st.subheader("Advanced 3D Analysis")
        simulate_3d_analysis(cap_data, resistance, voltage, temperature, time_steps, simulator, c_library_available)

    with tab5:
        st.subheader("اطلاعات خازن / Capacitor Information")
        display_capacitor_info(capacitor_type)

def simulate_charge_discharge(cap_data, resistance, voltage, temperature, time_steps, simulator, c_library_available):
    C = cap_data['Capacitance (µF)'] * 1e-6  # Convert to Farads
    R = resistance
    V0 = voltage

    if c_library_available and simulator:
        # Use C library for accurate simulation
        capacitor = simulator.create_capacitor(
            cap_data['Type'],
            C,
            cap_data['ESR (Ω)'],
            cap_data['Leakage (µA/V)'] * 1e-6,  # Convert to A/V
            cap_data['TempCoeff (%/°C)'] / 100.0  # Convert to decimal
        )

        voltages = simulator.simulate_behavior(capacitor, R, V0, temperature, time_steps)
        voltages = np.array(voltages)
    else:
        # Fallback to Python simulation
        voltages = []
        for t in time_steps:
            if t <= time_steps[-1] / 2:
                # Charging
                V = V0 * (1 - np.exp(-t / (R * C)))
            else:
                # Discharging
                discharge_time = t - time_steps[-1] / 2
                V = V0 * np.exp(-discharge_time / (R * C))
            voltages.append(V)
        voltages = np.array(voltages)

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time_steps, voltages, linewidth=2, color='#1f77b4')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('Capacitor Charge/Discharge Curve')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=time_steps[len(time_steps)//2], color='red', linestyle='--', alpha=0.7, label='Switch to Discharge')

    # Add capacitor specs to legend (better positioning to avoid overlap)
    specs_text = f"C={C*1e6:.1f}µF, R={R}Ω, V₀={V0}V, T={temperature}°C"
    ax.text(0.98, 0.02, specs_text, transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9),
            verticalalignment='bottom', horizontalalignment='right', fontsize=9)

    st.pyplot(fig)

    return voltages

def simulate_energy_analysis(cap_data, resistance, voltage, temperature, simulator, c_library_available):
    C = cap_data['Capacitance (µF)'] * 1e-6  # Convert to Farads
    R = resistance
    V0 = voltage

    # Initialize variables (will be calculated in both branches)
    energy_stored = 0.0
    energy_lost_ESR = 0.0
    energy_lost_leakage = 0.0
    dielectric_losses = 0.0
    plate_losses = 0.0
    self_discharge_losses = 0.0
    efficiency = 0.0

    if c_library_available and simulator:
        # Use C library for accurate calculation
        capacitor = simulator.create_capacitor(
            cap_data['Type'],
            C,
            cap_data['ESR (Ω)'],
            cap_data['Leakage (µA/V)'] * 1e-6,  # Convert to A/V
            cap_data['TempCoeff (%/°C)'] / 100.0  # Convert to decimal
        )

        efficiency = simulator.calculate_efficiency(capacitor, R, V0, temperature)

        # Calculate energy components for visualization - more realistic approach
        energy_stored = 0.5 * C * V0**2

        # ESR losses during charging (more realistic calculation)
        # For RC circuit, average power loss in ESR is (V0²/(4R)) during charging
        tau = R * C
        charging_time = min(5 * tau, tau * 3)  # Use 5τ or 3τ, whichever is smaller
        avg_ESR_loss_rate = (V0**2) / (4 * R)  # Average power loss during charging
        energy_lost_ESR = avg_ESR_loss_rate * charging_time

        # Leakage losses (very small for most capacitors)
        leakage = cap_data['Leakage (µA/V)'] * 1e-6  # Convert to A/V
        # Leakage is roughly constant current, but very small
        avg_leakage_current = leakage * V0 * 0.5  # Average voltage during charging
        energy_lost_leakage = avg_leakage_current * V0 * charging_time  # V*I*t approximation

        # Additional realistic losses for real-world capacitors
        # Dielectric losses (typically 1-5% of stored energy)
        dielectric_losses = energy_stored * 0.03  # 3% dielectric losses

        # Plate and terminal losses (typically 2-8% depending on capacitor type)
        plate_losses = energy_stored * 0.05  # 5% plate/terminal losses

        # Self-discharge losses (typically 1-3% over charging period)
        self_discharge_losses = energy_stored * 0.02  # 2% self-discharge

    else:
        # Simplified but more realistic calculation
        energy_stored = 0.5 * C * V0**2

        # More realistic ESR loss calculation
        tau = R * C
        charging_time = min(5 * tau, tau * 3)
        # Average current during charging is V0/(2R) for exponential charging
        avg_current = V0 / (2 * R)
        ESR = cap_data['ESR (Ω)']
        energy_lost_ESR = ESR * avg_current**2 * charging_time

        # Leakage losses (very small)
        leakage = cap_data['Leakage (µA/V)'] * 1e-6
        avg_leakage_current = leakage * V0 * 0.5
        energy_lost_leakage = avg_leakage_current * V0 * charging_time

        # Additional realistic losses for real-world capacitors
        # Dielectric losses (typically 1-5% of stored energy)
        dielectric_losses = energy_stored * 0.03  # 3% dielectric losses

        # Plate and terminal losses (typically 2-8% depending on capacitor type)
        plate_losses = energy_stored * 0.05  # 5% plate/terminal losses

        # Self-discharge losses (typically 1-3% over charging period)
        self_discharge_losses = energy_stored * 0.02  # 2% self-discharge

        total_energy_lost = energy_lost_ESR + energy_lost_leakage + dielectric_losses + plate_losses + self_discharge_losses
        efficiency = (energy_stored / (energy_stored + total_energy_lost)) * 100 if total_energy_lost > 0 else 0

    # Display results
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Energy Stored", f"{energy_stored*1e6:.2f} µJ")

    with col2:
        st.metric("Energy Lost (ESR)", f"{energy_lost_ESR*1e6:.2f} µJ")

    with col3:
        st.metric("Total Losses", f"{(dielectric_losses + plate_losses + self_discharge_losses)*1e6:.2f} µJ")

    with col4:
        st.metric("Efficiency", f"{efficiency:.1f}%")

    # Beautiful horizontal bar chart for energy distribution (no overlapping issues)
    fig, ax = plt.subplots(figsize=(12, 6))

    # Prepare data for horizontal bar chart
    categories = ['Stored Energy', 'ESR Losses', 'Dielectric Losses', 'Plate Losses', 'Self-Discharge', 'Leakage Losses']
    values = [energy_stored, energy_lost_ESR, dielectric_losses, plate_losses, self_discharge_losses, energy_lost_leakage]
    colors = ['#2ecc71', '#e74c3c', '#9b59b6', '#e67e22', '#34495e', '#f39c12']

    # Sort by value for better visual hierarchy
    sorted_indices = np.argsort(values)[::-1]
    categories = [categories[i] for i in sorted_indices]
    values = [values[i] for i in sorted_indices]
    colors = [colors[i] for i in sorted_indices]

    # Create horizontal bars
    bars = ax.barh(categories, values, color=colors, alpha=0.8)

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, values)):
        width = bar.get_width()
        percentage = (value / sum([energy_stored, energy_lost_ESR, energy_lost_leakage, dielectric_losses, plate_losses, self_discharge_losses])) * 100
        ax.text(width + max(values) * 0.02, bar.get_y() + bar.get_height()/2,
                f'{value*1e6:.1f} µJ ({percentage:.1f}%)',
                ha='left', va='center', fontsize=9, fontweight='bold')

    ax.set_xlabel('Energy (µJ)', fontsize=11)
    ax.set_title('Energy Distribution Breakdown', fontsize=14, pad=20)
    ax.grid(True, alpha=0.3, axis='x')

    # Remove spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adjust layout to prevent text cutoff
    plt.tight_layout()

    st.pyplot(fig)

    return efficiency

def simulate_temperature_effects(cap_data, resistance, voltage, time_steps, temperature, simulator, c_library_available):
    # Temperature range for comparison
    temp_range = np.linspace(-40, 125, 20)
    capacitance_values = []

    C_base = cap_data['Capacitance (µF)'] * 1e-6  # Convert to Farads
    temp_coeff = cap_data['TempCoeff (%/°C)'] / 100.0  # Convert to decimal

    for T in temp_range:
        # Apply temperature coefficient using the formula from C library
        if c_library_available and simulator:
            # Create a temporary capacitor for temperature calculation
            capacitor = simulator.create_capacitor(
                cap_data['Type'],
                C_base,
                cap_data['ESR (Ω)'],
                cap_data['Leakage (µA/V)'] * 1e-6,
                temp_coeff
            )
            # For temperature effects, we simulate at different temperatures
            # but for capacitance vs temperature, we'll use the formula directly
            C_T = C_base * (1 + temp_coeff * (T - 25))
        else:
            # Use the formula directly
            C_T = C_base * (1 + temp_coeff * (T - 25))

        capacitance_values.append(C_T * 1e6)  # Convert back to µF

    # Plot capacitance vs temperature
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(temp_range, capacitance_values, linewidth=2, color='#9b59b6', marker='o', markersize=4)
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Capacitance (µF)')
    ax.set_title('Capacitance vs Temperature')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=25, color='red', linestyle='--', alpha=0.7, label='Reference (25°C)')

    st.pyplot(fig)

    # Show capacitance change at selected temperature
    C_selected = C_base * (1 + temp_coeff * (temperature - 25))
    capacitance_change = (C_selected / C_base - 1) * 100
    st.metric("Capacitance at Selected Temperature",
              f"{C_selected*1e6:.2f} µF ({capacitance_change:+.1f}% change)")

def simulate_3d_analysis(cap_data, resistance, voltage, temperature, time_steps, simulator, c_library_available):
    """Create advanced 3D visualizations for capacitor analysis"""

    st.markdown("### 🎲 Multi-Dimensional Analysis")

    # Create sub-tabs for different 3D visualizations
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["3D Surface Plot", "Capacitor Comparison", "Energy Landscape"])

    with sub_tab1:
        st.markdown("#### 🌊 3D Voltage Surface (Time vs Resistance)")
        simulate_3d_surface_plot(cap_data, resistance, voltage, temperature, time_steps, simulator, c_library_available)

    with sub_tab2:
        st.markdown("#### ⚡ 3D Capacitor Comparison")
        simulate_3d_capacitor_comparison(resistance, voltage, temperature, simulator, c_library_available)

    with sub_tab3:
        st.markdown("#### 🏔️ 3D Energy Efficiency Landscape")
        simulate_3d_energy_landscape(cap_data, resistance, temperature, simulator, c_library_available)

def simulate_3d_surface_plot(cap_data, resistance, voltage, temperature, time_steps, simulator, c_library_available):
    """Create a 3D surface plot of voltage vs time and resistance"""

    # Parameters for 3D surface
    resistance_range = np.linspace(resistance * 0.5, resistance * 2, 20)
    time_range = np.linspace(0, time_steps[-1], 50)

    R_grid, T_grid = np.meshgrid(resistance_range, time_range)

    # Calculate voltage for each resistance value
    voltage_surface = np.zeros_like(R_grid)
    C = cap_data['Capacitance (µF)'] * 1e-6

    for i in range(len(resistance_range)):
        for j in range(len(time_range)):
            t = time_range[j]
            r = resistance_range[i]

            if t <= time_steps[-1] / 2:
                # Charging phase
                voltage_surface[j, i] = voltage * (1 - np.exp(-t / (r * C)))
            else:
                # Discharging phase
                discharge_time = t - time_steps[-1] / 2
                voltage_surface[j, i] = voltage * np.exp(-discharge_time / (r * C))

    # Create 3D surface plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(R_grid, T_grid, voltage_surface, cmap='viridis', alpha=0.8)

    ax.set_xlabel('Resistance (Ω)')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Voltage (V)')
    ax.set_title('3D Voltage Surface: Time vs Resistance')

    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.6)

    st.pyplot(fig)

def simulate_3d_capacitor_comparison(resistance, voltage, temperature, simulator, c_library_available):
    """Create a 3D scatter plot comparing different capacitor types"""

    # Load all capacitor data
    df = load_capacitor_data()

    # Create parameter ranges for 3D visualization
    resistance_range = np.linspace(50, 500, 15)
    voltage_range = np.linspace(5, 25, 10)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['red', 'blue', 'green', 'orange', 'purple']

    for idx, (_, cap_data) in enumerate(df.iterrows()):
        C = cap_data['Capacitance (µF)'] * 1e-6
        ESR = cap_data['ESR (Ω)']
        temp_coeff = cap_data['TempCoeff (%/°C)'] / 100.0

        # Calculate efficiency for different resistance/voltage combinations
        efficiencies = []

        for r in resistance_range:
            for v in voltage_range:
                if c_library_available and simulator:
                    capacitor = simulator.create_capacitor(
                        cap_data['Type'], C, ESR,
                        cap_data['Leakage (µA/V)'] * 1e-6, temp_coeff
                    )
                    eff = simulator.calculate_efficiency(capacitor, r, v, temperature)
                else:
                    # Simplified calculation
                    tau = r * C
                    avg_current = v / (2 * r)
                    energy_lost_ESR = ESR * avg_current**2 * tau
                    energy_stored = 0.5 * C * v**2
                    eff = (energy_stored / (energy_stored + energy_lost_ESR)) * 100

                efficiencies.append(eff)

        # Create 3D scatter plot
        R_grid, V_grid = np.meshgrid(resistance_range, voltage_range)
        E_grid = np.array(efficiencies).reshape(len(voltage_range), len(resistance_range))

        ax.scatter(R_grid, V_grid, E_grid, c=colors[idx], label=cap_data['Type'], alpha=0.6, s=20)

    ax.set_xlabel('Resistance (Ω)')
    ax.set_ylabel('Voltage (V)')
    ax.set_zlabel('Efficiency (%)')
    ax.set_title('3D Capacitor Comparison: Efficiency vs Parameters')

    # Position legend outside the plot to avoid overlap
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)

def simulate_3d_energy_landscape(cap_data, resistance, temperature, simulator, c_library_available):
    """Create a 3D energy landscape showing efficiency across parameter ranges"""

    # Parameter ranges
    resistance_range = np.linspace(50, 500, 20)
    voltage_range = np.linspace(5, 25, 15)

    R_grid, V_grid = np.meshgrid(resistance_range, voltage_range)

    # Calculate efficiency surface
    efficiency_surface = np.zeros_like(R_grid)
    C = cap_data['Capacitance (µF)'] * 1e-6
    ESR = cap_data['ESR (Ω)']
    temp_coeff = cap_data['TempCoeff (%/°C)'] / 100.0

    for i in range(len(resistance_range)):
        for j in range(len(voltage_range)):
            r = resistance_range[i]
            v = voltage_range[j]

            if c_library_available and simulator:
                capacitor = simulator.create_capacitor(
                    cap_data['Type'], C, ESR,
                    cap_data['Leakage (µA/V)'] * 1e-6, temp_coeff
                )
                efficiency_surface[j, i] = simulator.calculate_efficiency(capacitor, r, v, temperature)
            else:
                # Simplified calculation
                tau = r * C
                avg_current = v / (2 * r)
                energy_lost_ESR = ESR * avg_current**2 * tau
                energy_stored = 0.5 * C * v**2
                efficiency_surface[j, i] = (energy_stored / (energy_stored + energy_lost_ESR)) * 100

    # Create 3D surface plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(R_grid, V_grid, efficiency_surface, cmap='plasma', alpha=0.8)

    ax.set_xlabel('Resistance (Ω)')
    ax.set_ylabel('Voltage (V)')
    ax.set_zlabel('Efficiency (%)')
    ax.set_title(f'3D Energy Landscape: {cap_data["Type"]} Capacitor')

    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.6)

    # Add contour plot projection on the bottom
    ax.contour(R_grid, V_grid, efficiency_surface, zdir='z', offset=0, levels=10, alpha=0.3)

    st.pyplot(fig)

if __name__ == "__main__":
    main()
