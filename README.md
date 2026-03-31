# Ad campaign performance tracker

proyecto en python para automatizar el análisis de campañas de meta y google. limpia los datos, saca los kpis y te genera un excel con gráficos para no tener que hacerlo a mano.

## ¿Qué hace?
* Calcula CTR, CPC, CPL, CVR y ROAS por campaña y canal
* Detecta días con gasto anómalo (> 2σ sobre la media de la campaña)
* Genera 4 gráficos de rendimiento automáticos
* Exporta un Excel con 5 pestañas a la carpeta /outputs

## Estructura

ad-campaign-tracker/
├── generate_data.py   # genera el csv de prueba para practicar
├── pipeline.py        # lógica del etl y exportación
├── run.py             # punto de entrada principal
└── requirements.txt

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python run.py
```
Al ejecutar, si no existe data/campaigns.csv se genera automáticamente. Los resultados se guardan en outputs/.

## KPIs principales

Para no calcular todo a mano, el script saca esto:

* **CTR:** clicks / impresiones
* **CPC:** gasto / clicks
* **CPL:** gasto / conversiones
* **CVR:** conversiones / clicks
* **ROAS:** ingresos / gasto

## Stack

Python · Pandas · NumPy · Matplotlib · OpenPyXL
