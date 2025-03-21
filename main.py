import db
from sqlalchemy import create_engine, text
import traceback
import inspect
import util

import pandas as pd
import os
import logging
import smtp
from dotenv import load_dotenv
load_dotenv()


def main():
    try:
        

        start_time = util.show_time("Inicio")
        print(db.engine)

        TABLA = 'vkm_articulos'
        CSV_PATH = os.getenv('IMPORT_PATH','./')+ 'articulos.csv'
    
        # === LEER CSV ===
        df = pd.read_csv(CSV_PATH, sep=',', engine='python', encoding='utf-8')

        # Renombrar columnas si hiciera falta
        df.columns = [col.strip() for col in df.columns]

        df_final = pd.DataFrame({
            'IdArticulo': df['IdArticulo'],
            'cliente_id': df['cliente_id'],
            'IdCategoria': df['CATID'],  # viene como vacío en algunos casos
            'articulo_codigo': df['articulo_codigo'],
            'articulo_descripcion': df['nombre'],
            'articulo_master': 1,  # valor por defecto según tu tabla
        })    

        with db.engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {TABLA}"))

        # === INSERTAR DATOS (bulk insert) ===
        df_final.to_sql(TABLA, con=db.engine, if_exists='append', index=False)
        
        cantidad = len(df_final)
        print(f"✅ Se insertaron {cantidad} registros en la tabla `{TABLA}`.")


        end_time = util.show_time("Fin")
        
        print(f"Tiempo de ejecución: {end_time - start_time}")

    except Exception as e:
        description = traceback.format_exc()
        traceback.print_exc()
        print(description)
        frame = inspect.currentframe()
        function_name = inspect.getframeinfo(frame).function
        print(f"Error ocurrió en la función: {function_name}")
        print(f"Archivo: {inspect.getfile(frame)}")
        print(f"Error: {e}")

        html_msg = f"""<html>
        <body>
            <p>Error ocurrido en la función: {function_name}</p>
            <p>Archivo: {inspect.getfile(frame)}</p>
            <p>Error: {e}</p>
            <p>Descripción: {description}</p>
        </body>
        </html>"""
        smtp.smtp.SendMail(os.getenv('EMAIL_TICKETS', ''), f"Lectura de Archivo {CSV_PATH}", f"{description} {frame} {function_name}",html_msg , "")

db = db.DB()
main()