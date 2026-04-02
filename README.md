📝 IT Monitor Dashboard: Sistema de Gestión de Disponibilidad
Este proyecto implementa una solución de Monitoreo de Infraestructura IT de extremo a extremo. Combina una base de datos relacional en MySQL, un proceso ETL (Extracción, Transformación y Carga) en Python, y un tablero de control interactivo en Power BI.
🚀 1. Configuración de la Base de Datos (MySQL)
El primer paso es crear la estructura de datos. Utilizamos un modelo de "Estrella" donde relacionamos los activos de red con sus incidentes.
Comandos SQL:
SQL
CREATE DATABASE IF NOT EXISTS IT_MONITOR_DB;
USE IT_MONITOR_DB;

-- 1. Catálogo de Nodos (Dispositivos)
CREATE TABLE nodos (
    id_nodo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_nodo VARCHAR(50) NOT NULL,
    tipo_dispositivo ENUM('Servidor', 'Router', 'Switch', 'Firewall'),
    ubicacion VARCHAR(50),
    ip_address VARCHAR(15)
);

-- 2. Logs de Eventos (Hechos)
CREATE TABLE logs_eventos (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_nodo INT,
    fecha_evento DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_evento ENUM('Falla de Red', 'Sobrecarga CPU', 'Disco Lleno', 'Reinicio'),
    gravedad ENUM('Baja', 'Media', 'Alta', 'Critica'),
    duracion_minutos INT,
    FOREIGN KEY (id_nodo) REFERENCES nodos(id_nodo)
);

-- 3. Vista Optimizada para el Reporte
-- Esta vista une las tablas para que Python no tenga que procesar JOINS pesados.
CREATE OR REPLACE VIEW vista_monitoreo_it AS
SELECT 
    n.nombre_nodo, 
    n.tipo_dispositivo, 
    l.tipo_evento, 
    l.gravedad, 
    l.duracion_minutos, 
    l.fecha_evento
FROM nodos n
JOIN logs_eventos l ON n.id_nodo = l.id_nodo;

-- Datos de prueba iniciales
INSERT INTO nodos (nombre_nodo, tipo_dispositivo, ubicacion, ip_address) VALUES 
('SRV-Main-01', 'Servidor', 'DataCenter-Quito', '192.168.1.10'),
('RT-Edge-02', 'Router', 'Sucursal-Guayaquil', '10.0.0.1'),
('SW-Core-01', 'Switch', 'DataCenter-Quito', '192.168.1.5'),
('FW-Core-01', 'Firewall', 'DataCenter-Quito', '192.168.1.1');
________________________________________
🐍 2. Procesamiento de Datos (Python)
El script de Python extrae los datos de la Vista SQL, calcula el Índice de Salud y genera un archivo CSV limpio para Power BI.
Requisitos:
Ejecuta este comando en tu terminal para instalar las librerías necesarias:
Bash
pip install pandas sqlalchemy mysql-connector-python
Código procesamientos_it.py:
Python
import pandas as pd
from sqlalchemy import create_engine

# 1. Conexión a la Base de Datos (Ajusta root:tu_password)
engine = create_engine('mysql+mysqlconnector://root:Sofiap1419*@localhost/IT_MONITOR_DB')

# 2. Extracción de datos desde la Vista SQL
query = "SELECT * FROM vista_monitoreo_it"
df = pd.read_sql(query, engine)

# 3. Lógica de Negocio: Calcular "Índice de Salud"
# Restamos del 100% el tiempo de falla basado en 1440 min (un día).
df['salud_diaria_porcentaje'] = 100 - (df['duracion_minutos'] / 1440 * 100)

# 4. Limpieza: Asegurar que las fechas sean datetime y el rango sea 0-100
df['fecha_evento'] = pd.to_datetime(df['fecha_evento'])
df['salud_diaria_porcentaje'] = df['salud_diaria_porcentaje'].clip(0, 100).round(2)

# 5. Exportar a CSV para Power BI
df.to_csv('reporte_it_procesado.csv', index=False)
print("✅ Procesamiento completado. Archivo 'reporte_it_procesado.csv' generado.")
________________________________________
📊 3. Visualización (Power BI)
El Dashboard final permite una lectura rápida del estado de la infraestructura.
KPIs y Visuales clave:
1.	Estado de Salud (Velocímetro): Muestra el Promedio de la columna salud_diaria_porcentaje.
o	Configuración: Rojo (0-50), Amarillo (50-85), Verde (85-100).
2.	Suma de Minutos por Nodos (Barras): Identifica rápidamente qué equipo tuvo más tiempo fuera de servicio.
3.	Fallas por Dispositivo (Treemap): Muestra qué tipo de equipo (Servidor, Router, etc.) está generando más incidentes.
________________________________________
🛠️ 4. Glosario de Dispositivos (Nodos)
•	SRV (Servidor): Aloja aplicaciones y bases de datos críticas.
•	RT (Router): Gestiona la salida a Internet y conexión entre sucursales.
•	SW (Switch): Conecta los dispositivos dentro de la misma oficina.
•	FW (Firewall): Protege la red contra accesos no autorizados.
________________________________________
🔄 5. Procedimiento de Ejecución Mensual/Semanal
1.	Asegurarse de que los nuevos logs estén cargados en MySQL.
2.	Ejecutar el script Python para actualizar el cálculo de salud.
3.	Abrir Power BI y hacer clic en "Actualizar" para refrescar los gráficos con el nuevo CSV.
________________________________________
Desarrollado por: AngTI / DBA Fecha: Abril 2026
