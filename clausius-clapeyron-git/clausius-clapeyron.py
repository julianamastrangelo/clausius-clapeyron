import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path


# ============================================================
# 1. CONSTANTES Y DATOS EXPERIMENTALES
# ============================================================

R = 8.314  # Constante universal de los gases [J/(mol K)]

BASE_DIR = Path(__file__).resolve().parent

# Carga de datos experimentales
datos = np.genfromtxt(
    BASE_DIR / "data" / "datos_experimentales.csv",
    delimiter=",",
    skip_header=1
)

temperaturas_c= datos[:, 0]
voltajes = datos[:, 1]

# ============================================================
# 2. CALIBRACIÓN DEL BARÓMETRO
# ============================================================

# Relación lineal entre voltaje y presión:
# P = m_cal * V + b_cal

m_cal = 0.2041  # [atm/V]
b_cal = -0.0203 # [atm]

presiones = m_cal * voltajes + b_cal


# ============================================================
# 3. PROCESAMIENTO DE LOS DATOS
# ============================================================

# Conversión de temperatura a Kelvin
temperaturas_k = temperaturas_c + 273.15

# Linealización de Clausius-Clapeyron
inv_T = 1 / temperaturas_k
ln_p = np.log(presiones)

# Regresión lineal por mínimos cuadrados
pendiente, ordenada = np.polyfit(inv_T, ln_p, 1)

# Incerteza de la pendiente calculada analíticamente
incerteza_pendiente = 140

# Calor latente de vaporización
lv_estimado = -pendiente * R /1000

incerteza_lv = R * incerteza_pendiente /1000

# ============================================================
# 4. PRESENTACIÓN DE RESULTADOS
# ============================================================

print("\n--- RESULTADOS EXPERIMENTALES ---")

print(f"Pendiente: {pendiente:.2f} ± {incerteza_pendiente:.2f} K")

print(
    f"Calor latente de vaporización: "
    f"{lv_estimado / 1000:.2f} ± "
    f"{incerteza_lv / 1000:.2f} kJ/mol"
)


# ============================================================
# 5. GRÁFICO DE CLAUSIUS-CLAPEYRON
# ============================================================

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(7, 5))

# Datos experimentales
ax.plot(
    inv_T, ln_p,
    'o',
    color="#7fd9e7",
    label="Datos experimentales"
)

# Recta de ajuste
x_ajuste = np.linspace(inv_T.min(), inv_T.max(), 100)
y_ajuste = pendiente * x_ajuste + ordenada

ax.plot(
    x_ajuste, y_ajuste,
    '--',
    color="#081738",
    linewidth=2,
    label=(
    f"Ajuste lineal\n"
    f"$\\mathrm{{Pendiente}} = {pendiente:.0f} \\pm "
    f"{incerteza_pendiente:.0f}\\ \\mathrm{{K}}$\n"
    f"$\\mathrm{{Calor\\ Latente}} = {lv_estimado:.1f} \\pm "
    f"{incerteza_lv:.1f}\\ \\mathrm{{kJ/mol}}$"
)
)

# Etiquetas y título
ax.set_xlabel(r"$1/T$ [$K^{-1}$]", fontsize=20)
ax.set_ylabel(r"$\ln(P/P_0)$", fontsize=20)
ax.set_title("Ecuación lineal de Clausius-Clapeyron", fontsize=22)

# Formato de los ejes
ax.tick_params(axis='both', labelsize=15)

ax.xaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"{x:.1e}".replace(".", ","))
)

ax.yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"{x:.2f}".replace(".", ","))
)

# Estética
ax.grid(True, alpha=0.3)
ax.legend(prop={'family': 'Times New Roman', 'size': 14})

# Guardar resultados
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

plt.savefig(
    RESULTS_DIR / "grafico_clausius_clapeyron.png",
    dpi=300,
    bbox_inches="tight"
)

plt.tight_layout()
plt.show()
