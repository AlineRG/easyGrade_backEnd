import os
import pandas as pd
import sqlite3

work_dir = os.getcwd()
conn = sqlite3.connect("instance/easyGrade.db")


def create_table_if_not_exists(table_name: str) -> None:
    query = f"SELECT COUNT(*)FROM sqlite_master WHERE type= 'table' AND name = '{table_name}'"
    result = conn.execute(query)
    result_data = result.fetchall()[0][0]
    print(result_data)
    print(type(result_data))

    if result_data == 0:
        df = pd.read_csv(f"{work_dir}/database/csv_files/{table_name}.csv")
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Se han cargado los datos de {table_name} correctamente")
    elif result_data > 0:
        print(f"La tabla {table_name} ya existe en la base de datos")


create_table_if_not_exists("ALUMNOS")
create_table_if_not_exists("MAESTROS")
create_table_if_not_exists("MATERIAS")
create_table_if_not_exists("CONTACTO")
create_table_if_not_exists("TAREAS")
create_table_if_not_exists("CALIFICACIONES_EJERCICIOS")
create_table_if_not_exists("CALIFICACIONES_EXAMENES")
create_table_if_not_exists("CALIFICACIONES_MATERIA")
create_table_if_not_exists("CALIFICACIONES_TAREAS")
create_table_if_not_exists("REGISTRO_MATERIAS_ALUMNOS")
create_table_if_not_exists("REGISTRO_MATERIAS_MAESTROS")
create_table_if_not_exists("EXAMENES")
create_table_if_not_exists("ALUMNOS_MATERIA")
