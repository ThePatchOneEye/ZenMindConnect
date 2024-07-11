# core/comment_processing.py
from .AI import predecir_sentimiento
from .models import Notificacion

def procesar_comentario(comentario):
    print("Procesando comentario...")
    print(f"Contenido del comentario: {comentario.body}")
    # Utiliza la función predefinida para predecir el sentimiento
    sentimiento_predicho = predecir_sentimiento(comentario.body)
    # Imprime el sentimiento en la consola
    print(f"Sentimiento detectado: {sentimiento_predicho}")
    # Devuelve la variable sentimiento_predicho
    return sentimiento_predicho