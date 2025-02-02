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
letra_contador = Counter("".join(words))

# Calcular el total de letras en el archivo
total_letras = sum(letra_contador.values())

# Generar la tabla de frecuencia en porcentaje
letra_frecuencia = {letra.upper(): (cantidad / total_letras) * 100 for letra, cantidad in letra_contador.items()}

print("Tabla de frecuencia de letras actualizada a partir de wordleWords.txt:")
print(letra_frecuencia)

# 📌 2️⃣ Cargar el archivo de tríos de palabras
try:
    df = pd.read_csv("resultados_filtrados.csv")
except FileNotFoundError:
    print("No se encontró 'resultados_filtrados.csv'. Asegúrate de que el archivo existe.")
    exit()

# 📌 3️⃣ Función para calcular la probabilidad de cada trío basado en la frecuencia real
def calcular_probabilidad(trio):
    letras_unicas = set("".join(trio).upper())  # Convertir a mayúsculas y obtener letras únicas
    return sum(letra_frecuencia.get(letra, 0) for letra in letras_unicas)  # Sumar probabilidades

# 📌 4️⃣ Calcular la probabilidad de cada trío y ordenar
df["Probabilidad"] = df.apply(lambda row: calcular_probabilidad([row["Palabra 1"], row["Palabra 2"], row["Palabra 3"]]), axis=1)
df_ordenado = df.sort_values(by="Probabilidad", ascending=False)

# 📌 5️⃣ Guardar en un nuevo CSV ordenado
df_ordenado.to_csv("resultados_ordenados.csv", index=False)

print("\n✅ Resultados ordenados guardados en 'resultados_ordenados.csv'")
print(f"📊 Se ordenaron {len(df_ordenado)} combinaciones en función de la frecuencia real de letras en wordleWords.txt.")
