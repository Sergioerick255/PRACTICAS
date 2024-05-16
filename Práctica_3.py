"""Traduccion de un Codigo Binario"""
import gspread
from google.colab import auth
from google.auth import default
from google.colab import drive
from googleapiclient.discovery import build
import pandas as pd


class Trie:
    def __init__(self):
        """
        Inicializa un Trie vacío.
        """
        self.root = {}

    def insert(self, key, value):
        """
        Inserta una clave (letra) y un valor (cadena binaria) en el Trie.
        """
        node = self.root
        for char in value:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['value'] = key

    def decodificacion(self, binary_str):
        """
        Decodifica una cadena binaria a su cadena de caracteres original usando el Trie.
        """
        cadena = ''
        node = self.root
        temp_node = node

        for bit in binary_str:
            if bit in temp_node:
                temp_node = temp_node[bit]
                if 'value' in temp_node:
                    cadena += temp_node['value']
                    temp_node = self.root
            else:
                raise ValueError(
                    f"El bit {bit} no se pudo decodificar; no existe un camino en el Trie."
                )

        return cadena


# Montar Google Drive
drive.mount('/content/drive')

# Autenticación y acceso a Google Sheets
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)
worksheet = gc.open('Code.xlsx').sheet1
rows = worksheet.get_all_values()

# Convertir los datos en un DataFrame de pandas si es necesario
df = pd.DataFrame.from_records(rows[1:], columns=rows[0])

# Construcción del Trie
trie = Trie()
for index, row in df.iterrows():
    trie.insert(row['Letters'], row['Binary coding'])

# Construir el servicio para acceder a Google Docs
service = build('docs', 'v1', credentials=creds)

# Utilizar el ID del documento
DOCUMENT_ID = '1VyisLskAn35zKb9UwFBbftkAzyc32-Qm0gL6-JQLERs'

# Cómo obtener el contenido del documento
document = service.documents().get(documentId=DOCUMENT_ID).execute()
doc_content = document.get('body').get('content')

# Extracción del texto del documento
text = ''
for element in doc_content:
    if 'paragraph' in element:
        for para_element in element['paragraph']['elements']:
            if 'textRun' in para_element:
                text += para_element['textRun']['content']

binary_message = text.strip()

# Lectura del mensaje binario
print("Mensaje binario leído:", binary_message)  # Verificar el mensaje leído

# Decodificación del mensaje
try:
    decoded_message = trie.decodificacion(binary_message)
    print("Mensaje decodificado:", decoded_message)  # Mostrar el mensaje decodificado
except ValueError as e:
    print("Error en la decodificación:", e)  # Capturar y mostrar errores en la decodificación

codigo_file_path = '/content/drive/My Drive/Mensaje_Codificado.txt'
with open(codigo_file_path, 'w') as f:
    f.write(f'Mensaje binario leído:\n{binary_message}\n')
    f.write(f'Mensaje decodificado:\n{decoded_message}\n')
