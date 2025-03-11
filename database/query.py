import sqlite3
import pandas as pd

conn = sqlite3.connect("instance/easyGrade.db")


def get_maestros_data_by_apellido(conn, apellido) -> pd.DataFrame:
    """
    This function queries the database and retrieves all the data from the table
    MAESTROS where APELLIDO == apellido.

    Args:
    * apellido : str. The apellido to query

    Returns:
    * df: pd.DataFrame. A table with all the data from the MAESTROS table
    where APELLIDO is equal to the variable apellido
    """
    query = f"SELECT * FROM MAESTROS WHERE APELLIDO = '{apellido}'"
    result = conn.execute(query)

    result_data = result.fetchall()
    columns = [description[0] for description in result.description]
    df = pd.DataFrame(result_data, columns=columns)
    return df


def get_alumnos_data_by_materia_id(conn, materia_id) -> pd.DataFrame:
    """
    This function queries the database and retrieves all the data from the ALUMNOS table
    related to the specified MATERIA_ID in the ALUMNOS_MATERIA table.

    Args:
    * materia_id : int. The MATERIA_ID to query.

    Returns:
    * df: pd.DataFrame. A DataFrame containing MATERIA_ID, ALUMNO_ID, and NOMBRE
    from the ALUMNOS table related to the specified MATERIA_ID.
    """
    query = """
    SELECT AM.materia_id, AM.alumno_id, A.nombre
    FROM alumnos_materia AS AM
    JOIN ALUMNOS AS A ON AM.alumno_id = A.ALUMNO_ID
    WHERE AM.materia_id = ?;  
    """

    result = conn.execute(query, (materia_id,))
    result_data = result.fetchall()
    columns = [description[0] for description in result.description]
    df = pd.DataFrame(result_data, columns=columns)
    return df


def get_maestros_by_materia_id(conn, materia_id) -> pd.DataFrame:
    """
    This function queries the database and retrieves the NOMBRE and APELLIDO
    from the MAESTROS table for a specific MATERIA_ID.

    Args:
    * materia_id : int. The MATERIA_ID to query.

    Returns:
    * df: pd.DataFrame. A table with NOMBRE and APELLIDO of MAESTROS
    who teach the specified MATERIA_ID.
    """

    query = f"""
    SELECT MAESTROS.NOMBRE, MAESTROS.APELLIDO 
    FROM MAESTROS
    JOIN REGISTRO_MATERIAS_MAESTROS ON MAESTROS.MAESTRO_ID = REGISTRO_MATERIAS_MAESTROS.MAESTRO_ID
    WHERE REGISTRO_MATERIAS_MAESTROS.MATERIA_ID = {materia_id};
    """

    result = conn.execute(query)
    result_data = result.fetchall()
    df = pd.DataFrame(result_data, columns=["NOMBRE", "APELLIDO"])
    return df


def get_average_calificacion_by_alumno_id(conn, alumno_id) -> float:
    """
    This function queries the database to calculate the average CALIFICACION
    from the EXAMENES table for a specific ALUMNO_ID.

    Args:
    * alumno_id : int. The ALUMNO_ID to query

    Returns:
    * promedio: float. The average CALIFICACION for the given ALUMNO_ID
    """
    query = f"""
    SELECT AVG(CALIFICACION) AS Promedio 
    FROM EXAMENES 
    WHERE ALUMNO_ID = {alumno_id};
    """
    result = conn.execute(query)
    result_data = result.fetchall()
    promedio = result_data[0][0] if result_data else None

    return promedio


def get_materias_by_maestro_id(conn, maestro_id) -> pd.DataFrame:
    """
    This function queries the database and retrieves the NOMBRE of all
    subjects (MATERIAS) from the REGISTRO_MATERIAS_MAESTROS table where
    MAESTRO_ID == maestro_id.

    Args:
    * maestro_id : int. The MAESTRO_ID to query.

    Returns:
    * df: pd.DataFrame. A table with the NOMBRE of the subjects taught by the specified MAESTRO_ID.
    """
    query = f"""
    SELECT MATERIAS.NOMBRE
    FROM MATERIAS
    JOIN REGISTRO_MATERIAS_MAESTROS ON MATERIAS.MATERIA_ID = REGISTRO_MATERIAS_MAESTROS.MATERIA_ID
    WHERE REGISTRO_MATERIAS_MAESTROS.MAESTRO_ID = {maestro_id};
    """
    result = conn.execute(query)
    result_data = result.fetchall()
    df = pd.DataFrame(result_data, columns=["NOMBRE"])
    return df


def count_alumnos_by_maestro_id(conn, maestro_id) -> int:
    """
    This function queries the database to count the number of ALUMNOS
    enrolled in subjects taught by a specific MAESTRO_ID.

    Args:
    * maestro_id : int. The MAESTRO_ID to query.

    Returns:
    * count: int. The count of ALUMNOS for the given MAESTRO_ID.
    """
    query = f"""
    SELECT COUNT(DISTINCT ALUMNOS.ALUMNO_ID) AS count
    FROM ALUMNOS
    JOIN ALUMNOS_MATERIA ON ALUMNOS.ALUMNO_ID = ALUMNOS_MATERIA.ALUMNO_ID
    JOIN REGISTRO_MATERIAS_ALUMNOS ON ALUMNOS_MATERIA.MATERIA_ID = REGISTRO_MATERIAS_ALUMNOS.MATERIA_ID
    WHERE REGISTRO_MATERIAS_ALUMNOS.MAESTRO_ID = {maestro_id};
    """
    result = conn.execute(query)
    result_data = result.fetchone()  # fetchone() returns a single row
    count = result_data[0] if result_data else 0
    return count


def get_tareas_by_alumno_id(conn, alumno_id) -> pd.DataFrame:
    """
    This function queries the database and retrieves all the data from the TAREAS
    table where ALUMNO_ID == alumno_id.

    Args:
    * alumno_id : int. The ALUMNO_ID to query

    Returns:
    * df: pd.DataFrame. A table with all the data from the TAREAS table
    where ALUMNO_ID is equal to the variable alumno_id
    """
    query = f"""
    SELECT * 
    FROM TAREAS 
    WHERE ALUMNO_ID = {alumno_id};
    """
    result = conn.execute(query)
    result_data = result.fetchall()
    columns = [description[0] for description in result.description]
    df = pd.DataFrame(result_data, columns=columns)
    return df


def get_alumnos_by_materia_ordered_by_apellido_nombre(conn, materia_id) -> pd.DataFrame:
    """
    This function queries the database to retrieve all data from the ALUMNOS
    table for a specific MATERIA_ID and orders the results by APELLIDO and then NOMBRE.

    Args:
    * materia_id : int. The MATERIA_ID to query.

    Returns:
    * df: pd.DataFrame. A table with all the data from the ALUMNOS table
    ordered by APELLIDO and NOMBRE.
    """
    query = f"""
    SELECT ALUMNOS.NOMBRE, ALUMNOS.APELLIDO 
    FROM ALUMNOS 
    JOIN ALUMNOS_MATERIA ON ALUMNOS.ALUMNO_ID = ALUMNOS_MATERIA.ALUMNO_ID 
    WHERE ALUMNOS_MATERIA.MATERIA_ID = {materia_id}
    ORDER BY ALUMNOS.APELLIDO, ALUMNOS.NOMBRE;
    """
    result = conn.execute(query)

    result_data = result.fetchall()
    columns = [description[0] for description in result.description]
    df = pd.DataFrame(result_data, columns=columns)
    return df


# Close the connection after all operations
conn.close()
