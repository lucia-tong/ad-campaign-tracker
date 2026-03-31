# Ad Campaign Performance Tracker

Pipeline ETL en Python que procesa datos de campañas publicitarias multicanal, calcula KPIs de rendimiento, detecta anomalías de gasto y exporta un informe en Excel con gráficos.

## ¿Qué hace?

- Calcula CTR, CPC, CPL, CVR y ROAS por campaña y canal
- Detecta días con gasto anómalo (> 2σ sobre la media de la campaña)
- Genera 4 gráficos de rendimiento
- Exporta un Excel con 5 pestañas a `outputs/`

## Estructura

```
ad-campaign-tracker/
├── generate_data.py   # genera el CSV de prueba
├── pipeline.py        # ETL: cálculo de KPIs, anomalías y exportación
├── run.py             # punto de entrada
└── requirements.txt
```

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python run.py
```

Al ejecutar, si no existe `data/campaigns.csv` se genera automáticamente. Los resultados se guardan en `outputs/`.

## KPIs calculados

| Métrica | Fórmula |
|---------|---------|
| CTR | Clicks / Impresiones |
| CPC | Gasto / Clicks |
| CPL | Gasto / Conversiones |
| CVR | Conversiones / Clicks |
| ROAS | Ingresos estimados / Gasto |

## Stack

Python · Pandas · NumPy · Matplotlib · OpenPyXL

---
Lucia Kai Li Tong Medina · [LinkedIn](https://linkedin.com/in/lucia-tong-)
