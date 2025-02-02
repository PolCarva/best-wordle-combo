import pandas as pd
from collections import Counter

# 📌 1️⃣ Cargar palabras desde wordleWords.txt y calcular la frecuencia real de letras
try:
    with open("wordleWords.txt", "r", encoding="utf-8") as file:
        words = [line.strip().lower() for line in file.readlines()]
except FileNotFoundError:
    print("No se encontró 'wordleWords.txt'. Asegúrate de crearlo con palabras válidas.")
    exit()

# Contar la frecuencia de cada letra en todas las palabras
letter_counter = Counter("".join(words))

# Calcular el total de letras en el archivo
total_letters = sum(letter_counter.values())

# Generar la tabla de frecuencia en porcentaje
letter_frequency = {letter.upper(): (count / total_letters) * 100 for letter, count in letter_counter.items()}

print("Tabla de frecuencia de letras actualizada a partir de wordleWords.txt:")
print(letter_frequency)

# 📌 2️⃣ Cargar el archivo de tríos de palabras
try:
    df = pd.read_csv("resultados_filtrados.csv")
except FileNotFoundError:
    print("No se encontró 'resultados_filtrados.csv'. Asegúrate de que el archivo existe.")
    exit()

# 📌 3️⃣ Función para calcular la probabilidad de cada trío basado en la frecuencia real
def calculate_probability(trio):
    unique_letters = set("".join(trio).upper())  # Convertir a mayúsculas y obtener letras únicas
    return sum(letter_frequency.get(letter, 0) for letter in unique_letters)  # Sumar probabilidades

# 📌 4️⃣ Calcular la probabilidad de cada trío y ordenar
df["Probabilidad"] = df.apply(lambda row: calculate_probability([row["Palabra 1"], row["Palabra 2"], row["Palabra 3"]]), axis=1)
df_sorted = df.sort_values(by="Probabilidad", ascending=False)

# 📌 5️⃣ Guardar en un nuevo CSV ordenado
df_sorted.to_csv("resultados_ordenados.csv", index=False)

print("\n✅ Resultados ordenados guardados en 'resultados_ordenados.csv'")
print(f"📊 Se ordenaron {len(df_sorted)} combinaciones en función de la frecuencia real de letras en wordleWords.txt.")
