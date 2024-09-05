import pandas as pd # type: ignore
from collections import Counter
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem import WordNetLemmatizer  # type: ignore
import matplotlib.pyplot as plt # type: ignore
import os
import string

# Descargar recursos necesarios de nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Inicializar lematizador y lista de stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
additional_stopwords = {"back", "get", "would", "one", "never", "rolex", "watch", "year", "like", "day", "week", "said", "told", "could"}  # Agregar más stopwords si es necesario
stop_words.update(additional_stopwords)

# Obtener la ruta absoluta del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa para el archivo CSV de entrada
input_path = os.path.join(script_dir, '..', 'data', 'reviews_with_emotion_score.csv')

# Comprobar si el archivo de entrada existe
if not os.path.exists(input_path):
    raise FileNotFoundError(f"The input file does not exist at the path: {input_path}")

# Leer el archivo CSV con las reseñas y sentimientos
review_data = pd.read_csv(input_path)

# Filtrar reseñas negativas (rating 1 o 2, o polaridad negativa)
negative_reviews = review_data[
    (review_data['Rating'] <= 2) | 
    (review_data['Polarity'] < 0)
]

# Obtener todas las reseñas negativas en una sola lista de palabras
all_words = []

for review in negative_reviews['Content']:
    # Tokenizar el texto de la reseña
    words = word_tokenize(review.lower())
    # Filtrar palabras no deseadas
    filtered_words = [
        lemmatizer.lemmatize(word)  # Lematización para reducir las palabras a su raíz
        for word in words
        if word.isalnum()  # Remover cualquier palabra que no sea alfanumérica
        and word not in stop_words  # Remover stop words
        and len(word) > 2  # Remover palabras con menos de 3 caracteres
        and not any(char.isdigit() for char in word)  # Remover palabras que contengan números
    ]
    all_words.extend(filtered_words)

# Contar las palabras clave
word_counts = Counter(all_words)

# Mostrar las 20 palabras más comunes en reseñas negativas
most_common_words = word_counts.most_common(20)

# Imprimir resultados
print("Most common keywords in negative reviews:")
for word, count in most_common_words:
    print(f"{word}: {count} times")

# Crear un gráfico de barras
words, counts = zip(*most_common_words)
plt.figure(figsize=(10, 5))
plt.bar(words, counts, color='skyblue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Keywords in Negative Reviews')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Guardar el gráfico de barras como una imagen en la carpeta Images
images_folder = os.path.join(script_dir, '..', 'Images')
os.makedirs(images_folder, exist_ok=True)
image_path = os.path.join(images_folder, 'negative_reviews_word_count.png')
plt.savefig(image_path)
plt.show()

print(f"Bar chart saved as '{image_path}'")

