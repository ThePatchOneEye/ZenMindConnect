# core/AI.py
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from django.conf import settings
import json

# Ruta al directorio del modelo
directorio_modelo = os.path.join(settings.BASE_DIR, 'core', 'AI ZenMindConnect')

# Ruta al archivo del modelo
ruta_modelo_sentimientos = os.path.join(directorio_modelo, 'modelo_sentimientos_tf_despues_de_cargar.h5')

# Cargar el modelo
modelo_sentimientos = tf.keras.models.load_model(ruta_modelo_sentimientos)

# Ruta al archivo del tokenizador
ruta_tokenizador = os.path.join(directorio_modelo, 'tokenizador.json')

# Cargar el tokenizador
with open(ruta_tokenizador, 'r') as file:
    tokenizador_config = json.load(file)
    tokenizador_config_str = json.dumps(tokenizador_config)  # Convertir el diccionario a cadena JSON
    tokenizador = tf.keras.preprocessing.text.tokenizer_from_json(tokenizador_config_str)
    
# Función para predecir sentimientos
def predecir_sentimiento(comentario):
    # Asegúrate de obtener el texto del comentario
    texto_comentario = comentario.body if hasattr(comentario, 'body') else str(comentario)

    # Tokenizar el comentario
    comentario_tokenizado = tokenizador.texts_to_sequences([texto_comentario])
    comentario_pad = pad_sequences(comentario_tokenizado, maxlen=modelo_sentimientos.input_shape[1])

    # Ajusta según la longitud de entrada del modelo
    prediccion = modelo_sentimientos.predict(comentario_pad)

    # Obtén la etiqueta del sentimiento detectado
    if prediccion > 0.5:
        sentimiento_predicho = "positivo"
    else:
        sentimiento_predicho = "negativo"

    # Imprime el sentimiento en la consola
    print(f"Sentimiento detectado: {sentimiento_predicho}")
    return sentimiento_predicho

