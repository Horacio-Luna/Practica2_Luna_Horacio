"""
Práctica Individual N° 2 - Unidad II
Caso: Demanda diaria de Paracetamol 500 mg en una farmacia.
Objetivo: Caracterizar la demanda para alimentar el módulo de
inventario de un sistema de ventas (punto de reorden y stock de seguridad).
Autor: Horacio Rodrigo Luna Loza
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

# ---------- Rutas ----------
BASE    = Path(__file__).resolve().parent.parent
CSV     = BASE / "datos" / "datos.csv"
REPORTE = BASE / "reporte" / "informe.txt"
REPORTE.parent.mkdir(parents=True, exist_ok=True)

# ---------- 1. Carga de datos ----------
df = pd.read_csv(CSV)
x  = df["demanda_unidades"].astype(float)
n  = len(x)

# ---------- 2. Estadísticos descriptivos ----------
media     = x.mean()
mediana   = x.median()
moda      = x.mode().iloc[0]
var_m     = x.var(ddof=1)
std_m     = x.std(ddof=1)
cv        = std_m / media * 100
minimo    = x.min()
maximo    = x.max()
q1        = x.quantile(0.25)
q3        = x.quantile(0.75)
iqr       = q3 - q1
asimetria = x.skew()
curtosis  = x.kurt()

# ---------- 3. Outliers con Z-Score ----------
z       = (x - media) / std_m
mask    = np.abs(z) > 3
outliers = df[mask].copy()
outliers["z_score"] = z[mask].values

# ---------- 4. Prueba de bondad de ajuste (K-S Normal) ----------
D, p_valor = stats.kstest(x, stats.norm(loc=media, scale=std_m).cdf)
alpha = 0.05
if p_valor >= alpha:
    decision = "No se rechaza H0: la demanda diaria puede modelarse como Normal."
else:
    decision = "Se rechaza H0: la demanda diaria no se ajusta a una Normal."

# ---------- 5. Aplicación al sistema de inventario ----------
# Parámetros de gestión (se asumen para el ejemplo)
lead_time_dias = 3       # tiempo de reposición del proveedor
nivel_servicio = 0.95    # 95% de nivel de servicio
z_servicio     = stats.norm.ppf(nivel_servicio)   # ≈ 1.645

# Punto de reorden: ROP = mu*L + z*sigma*sqrt(L)
ROP = media * lead_time_dias + z_servicio * std_m * np.sqrt(lead_time_dias)
SS  = z_servicio * std_m * np.sqrt(lead_time_dias)   # stock de seguridad

# ---------- 6. Reporte ----------
L = []
L.append("INFORME TÉCNICO - PRÁCTICA 2 (UNIDAD II)")
L.append("=" * 60)
L.append("1. Nombre del estudiante : <Tu Nombre>")
L.append("2. Título del caso       : Demanda diaria de Paracetamol 500 mg")
L.append("                           en una farmacia (base para sistema")
L.append("                           de ventas e inventario).")
L.append("")
L.append("3. Formulación del problema")
L.append("   La farmacia no cuenta con un criterio cuantitativo para")
L.append("   decidir cuándo reponer el Paracetamol 500 mg ni cuánto")
L.append("   stock de seguridad mantener. Esto provoca quiebres de")
L.append("   stock en días de alta demanda y sobre-stock en días")
L.append("   normales. Se necesita caracterizar la demanda diaria")
L.append("   para alimentar el módulo de inventario de un futuro")
L.append("   sistema de ventas.")
L.append("")
L.append("4. Variable principal")
L.append("   demanda_unidades: unidades vendidas por día.")
L.append("   Tipo: cuantitativa discreta (unidades).")
L.append("   Unidad: unidades/día.")
L.append("")
L.append("5. Supuestos")
L.append("   - La farmacia opera los 40 días en condiciones similares.")
L.append("   - Un solo punto de venta, sin promociones durante la")
L.append("     mayor parte del periodo observado.")
L.append("   - Las ventas diarias son independientes entre sí.")
L.append("   - El proveedor tiene un lead time estable de 3 días.")
L.append("   - Los registros del sistema de ventas son confiables.")
L.append("")
L.append("6. Estadísticos descriptivos")
L.append(f"   n                      = {n}")
L.append(f"   Media                  = {media:.4f} unidades/día")
L.append(f"   Mediana                = {mediana:.4f}")
L.append(f"   Moda                   = {moda:.4f}")
L.append(f"   Varianza muestral      = {var_m:.4f}")
L.append(f"   Desviación estándar    = {std_m:.4f}")
L.append(f"   Coeficiente de variación = {cv:.2f} %")
L.append(f"   Mínimo                 = {minimo:.2f}")
L.append(f"   Q1                     = {q1:.2f}")
L.append(f"   Q3                     = {q3:.2f}")
L.append(f"   IQR                    = {iqr:.2f}")
L.append(f"   Máximo                 = {maximo:.2f}")
L.append(f"   Asimetría              = {asimetria:.4f}")
L.append(f"   Curtosis               = {curtosis:.4f}")
L.append("")
L.append("7. Valores atípicos (Z-Score, |Z| > 3)")
if outliers.empty:
    L.append("   No se detectaron outliers con el criterio |Z| > 3.")
else:
    for _, r in outliers.iterrows():
        L.append(f"   id_dia={int(r['id_dia']):>2}  "
                 f"demanda={r['demanda_unidades']:>5.0f} u  "
                 f"Z={r['z_score']:+.3f}")
L.append("")
L.append("8. Análisis descriptivo")
L.append(f"   La demanda media es de {media:.2f} unidades/día con una")
L.append(f"   desviación estándar de {std_m:.2f} unidades. El coeficiente")
L.append(f"   de variación ({cv:.2f}%) indica una dispersión moderada.")
L.append(f"   La asimetría ({asimetria:+.2f}) y la curtosis ({curtosis:+.2f})")
L.append("   reflejan la presencia de días con comportamiento anómalo.")
L.append("")
L.append("9. Interpretación técnica")
L.append("   Prueba de Kolmogorov-Smirnov (bondad de ajuste Normal)")
L.append(f"   Estadístico D = {D:.4f}")
L.append(f"   p-valor       = {p_valor:.4f}   (alpha = {alpha})")
L.append(f"   Decisión      : {decision}")
L.append("")
L.append("   Aplicación al sistema de inventario")
L.append(f"   Lead time del proveedor     L  = {lead_time_dias} días")
L.append(f"   Nivel de servicio deseado      = {nivel_servicio*100:.0f} %")
L.append(f"   z de servicio                  = {z_servicio:.4f}")
L.append(f"   Punto de reorden (ROP)         = {ROP:.2f} unidades")
L.append(f"   Stock de seguridad (SS)        = {SS:.2f} unidades")
L.append("")
L.append("10. Conclusión")
L.append("   La demanda diaria de Paracetamol 500 mg puede caracterizarse")
L.append("   con una media cercana a 45 unidades/día y una desviación")
L.append("   estándar de ~7 unidades. Los días 8 (brote/demanda alta) y")
L.append("   22 (feriado/demanda baja) son outliers que el sistema debe")
L.append("   tratar como eventos especiales y no como parte del patrón")
L.append("   normal. Con un lead time de 3 días y un nivel de servicio")
L.append(f"   del 95%, se recomienda configurar en el sistema un punto")
L.append(f"   de reorden de {ROP:.0f} unidades y un stock de seguridad")
L.append(f"   de {SS:.0f} unidades. Este resultado es directamente")
L.append("   utilizable como parámetro de configuración del módulo de")
L.append("   inventario del sistema de ventas.")

with open(REPORTE, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("Análisis completado.")
print(f"Reporte generado en: {REPORTE}")
print(f"Media={media:.2f}  Desv={std_m:.2f}  CV={cv:.2f}%")
print(f"Outliers |Z|>3: {len(outliers)}")
print(f"K-S Normal: D={D:.4f}  p={p_valor:.4f}")
print(f"ROP={ROP:.2f} u  SS={SS:.2f} u")
