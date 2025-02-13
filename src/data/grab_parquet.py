from minio import Minio
import urllib.request
import pandas as pd
import datetime
import sys  
import os.path
import os
from minio import Minio
import logging
def main():
 #   grab_data_range()
    write_data_minio()

def grab_data_range() -> None:
    """Grab the data from New York Yellow Taxi for January 2023 to August 2023"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the relative path to the folder
    folder_path = os.path.join(script_dir, '..', '..', 'data', 'raw')
    # URL des données des taxis de NYC
    data_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023'
    # Répertoire pour récupérer les données
    save_dir = '../../data/raw'
    script_dir = os.path.dirname(os.path.abspath(__file__))
   

    os.makedirs(save_dir, exist_ok=True)
    # Téléchargement
    for month in range(1, 9):  # Récupérer de janvier à août
        month_str = str(month).zfill(2)  # Formatage du mois sur deux chiffres avec un zéro devant si nécessaire
        file_url = f'{data_url}-{month_str}.parquet'
        file_path = os.path.join(folder_path, f'2023-{month_str}-tripdata.parquet')
        try:
            urllib.request.urlretrieve(file_url, file_path)
            print(f'Downloaded: {file_path}')
        except urllib.error.HTTPError as e:
            print(f"Error downloading {file_url}: {e}")
    
    # Obtenir la liste des fichiers dans le répertoire
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data', 'raw')
def write_data_minio():
 
    """
    This method puts all downloaded files into Minio
    """
    # Créez une instance Minio avec les détails de connexion
    
    client = Minio(
        "localhost:9000",
        secure=False,
        access_key="minio",
        secret_key="minio123"
    )

    bucket_name = "test"  # Nom du bucket Minio

    # Vérifiez si le bucket existe, sinon, créez-le
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print("Le bucket existe déjà")
  


    # Parcourez les fichiers dans le dossier de destination
    for filename in os.listdir(data_dir):
        # Assurez-vous que le fichier est un fichier (pas un répertoire) avant de l'envoyer à Minio
        if os.path.isfile(os.path.join(data_dir, filename)):
            file_path = os.path.join(data_dir, filename)
            # Téléversez le fichier dans Minio
            object_name = os.path.basename(file_path)
            client.fput_object(bucket_name, object_name, file_path)
            print(f"Fichier téléchargé dans Minio : {object_name}")

if __name__ == '__main__':
        main()