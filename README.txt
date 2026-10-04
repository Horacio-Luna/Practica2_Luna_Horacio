# Práctica 2 — Demanda diaria de Paracetamol 500 mg en una farmacia

**Autor:** Horacio Rodrigo Luna Loza
**Curso:** Simulación — Unidad II (03/10/2026)

## ¿Por qué este caso?
La variable **demanda_unidades/día** es el insumo básico del módulo
de **inventario** de cualquier sistema de ventas: define el punto de
reorden (ROP) y el stock de seguridad (SS).

## Estructura
- `datos/datos.csv`        → 40 días de demanda observada.
- `scripts/analisis.py`    → estadísticos, Z-Score, K-S y ROP.
- `reporte/informe.txt`    → informe técnico final.
- `README.md`              → este archivo.

## Ejecución
```bash
pip install pandas numpy scipy
python scripts/analisis.py