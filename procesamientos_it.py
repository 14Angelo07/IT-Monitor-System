
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# 1. Configurar la conexión (Ajusta con tu contraseña de root)
engine = create_engine('mysql+mysqlconnector://root:Sofiap1419*@localhost/IT_MONITOR_DB')

# 2. Extraer datos con SQL
query = """
SELECT n.nombre_nodo, n.tipo_dispositivo, l.tipo_evento, l.gravedad, l.duracion_minutos, l.fecha_evento
FROM nodos n
JOIN logs_eventos l ON n.id_nodo = l.id_nodo
"""
df = pd.read_sql(query, engine)

# 3. Transformación: Calcular "Indice de Salud"
# Supongamos que un nodo debería estar activo 1440 min al día (24h).
df['salud_diaria_porcentaje'] = 100 - (df['duracion_minutos'] / 1440 * 100)

# 4. Limpieza: Asegurar que las fechas sean tipo datetime
df['fecha_evento'] = pd.to_datetime(df['fecha_evento'])

# TRUCO DE LIMPIEZA: Redondear a 2 decimales y asegurar que no pase de 100
df['salud_diaria_porcentaje'] = df['salud_diaria_porcentaje'].clip(0, 100).round(2)

# Exportar de nuevo
df.to_csv('reporte_it_procesado.csv', index=False)
print("Dato de ejemplo:", df['salud_diaria_porcentaje'].iloc[0]) 
# Si aquí te imprime un número normal (ej: 95.5), el problema era el archivo anterior.

print("Datos procesados con éxito:")
print(df.head())

# Guardar a CSV para que Power BI lo lea fácil o dejarlo en SQL
df.to_csv('reporte_it_procesado.csv', index=False)

