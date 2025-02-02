import pandas as pd

# 📌 1️⃣ Cargar la lista de palabras de Wordle para hacer búsquedas rápidas
try:
    with open("wordleWords.txt", "r", encoding="utf-8") as file:
        wordle_words = set(line.strip().lower() for line in file.readlines())  # Usamos un set para búsquedas rápidas
except FileNotFoundError:
    print("No se encontró 'wordleWords.txt'. Asegúrate de que el archivo existe.")
    exit()

# 📌 2️⃣ Cargar el archivo de tríos ordenados por probabilidad
try:
    df = pd.read_csv("resultados_ordenados.csv")
except FileNotFoundError:
    print("No se encontró 'resultados_ordenados.csv'. Asegúrate de que el archivo existe.")
    exit()

# 📌 3️⃣ Verificar qué palabras del trío están en wordleWords.txt
def obtener_palabras_existentes(row):
    palabras_en_wordle = [word.lower() for word in [row["Palabra 1"], row["Palabra 2"], row["Palabra 3"]] if word.lower() in wordle_words]
    return ", ".join(palabras_en_wordle) if palabras_en_wordle else None  # Devolver palabras separadas por coma o None si no hay coincidencias

# Aplicar la función a cada fila
df["Palabras que se repiten"] = df.apply(obtener_palabras_existentes, axis=1)

# Contar cuántas palabras coinciden en cada fila
df["Cantidad de coincidencias"] = df["Palabras que se repiten"].apply(lambda x: len(x.split(", ")) if pd.notna(x) else 0)

# Filtrar solo los tríos que contienen al menos una palabra en wordleWords.txt
df_filtrado = df[df["Cantidad de coincidencias"] > 0]

# 📌 4️⃣ Ordenar por cantidad de coincidencias (de mayor a menor), luego por probabilidad
df_filtrado = df_filtrado.sort_values(by=["Cantidad de coincidencias", "Probabilidad"], ascending=[False, False])

# 📌 5️⃣ Guardar los resultados en un nuevo CSV
df_filtrado.to_csv("resultados_con_palabra_existe.csv", index=False)

print("\n✅ Resultados guardados en 'resultados_con_palabra_existe.csv'")
print(f"📊 Se encontraron {len(df_filtrado)} tríos donde al menos una palabra exacta está en wordleWords.txt.")
