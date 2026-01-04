"""
Módulo de gerenciamento de dados em JSON.
Responsável por carregar e salvar dados de projetos e parcelas.
"""

import json

# Constante
JSON_FILE = 'data.json'


def load_data(file_path):
    """
    Carrega dados do arquivo JSON.
    
    Args:
        file_path (str): Caminho do arquivo JSON
        
    Returns:
        dict: Dados carregados ou dicionário vazio se arquivo não existir
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

    
def save_data(data, file_path):
    """
    Salva dados no arquivo JSON.
    
    Args:
        data (dict): Dados a serem salvos
        file_path (str): Caminho do arquivo JSON
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

