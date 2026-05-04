import pandas as pd
import requests
from datetime import datetime

# URL REAL dataset Barcelona
URL = "https://opendata-ajuntament.barcelona.cat/data/dataset/accidents/resource/4e7c9b4c.csv"
OUTPUT_FILE = "data_cleaned.csv"

def download_data(url):
    print("Descargando datos...")
    response = requests.get(url)

    if response.status_code == 200:
        with open("raw_data.csv", "wb") as f:
            f.write(response.content)
        print("Descarga completada")
    else:
        raise Exception("Error al descargar datos")

def clean_data():
    print("Limpiando datos...")
    df = pd.read_csv("raw_data.csv")

    df = df.drop_duplicates()

    # eliminar datos no válidos
    if "Nom_districte" in df.columns:
        df = df[df["Nom_districte"] != "Desconegut"]

    if "Codi_districte" in df.columns:
        df = df[df["Codi_districte"] != -1]

    # eliminar coordenadas vacías
    df = df.dropna(subset=["Latitud", "Longitud"])

    # convertir fecha
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    df["last_update"] = datetime.now()

    return df

def save_data(df, output_file):
    df.to_csv(output_file, index=False)
    print("Datos guardados")

def run_pipeline():
    download_data(URL)
    df = clean_data()
    save_data(df, OUTPUT_FILE)
    print("Pipeline completado")

if __name__ == "__main__":
    run_pipeline()

import os

os.system("git config --global user.name 'github-actions'")
os.system("git config --global user.email 'actions@github.com'")
os.system("git add data_cleaned.csv")
os.system("git commit -m 'Update dataset'")
os.system("git push")
