from itertools import combinations
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# Cargar lista de palabras desde words.txt
try:
    with open("words.txt", "r", encoding="utf-8") as file:
        words = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    print("No se encontró 'words.txt'. Asegúrate de crearlo con palabras válidas.")
    exit()

# Cargar lista de palabras con una vocal desde oneVowel.txt
try:
    with open("oneVowel.txt", "r", encoding="utf-8") as file:
        one_vowel_words = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    print("No se encontró 'oneVowel.txt'. Asegúrate de crearlo con palabras válidas.")
    exit()

# Función para verificar combinaciones válidas
def check_combination(word1, word2, word3):
    combined = word1 + word2 + word3
    return (word1, word2, word3) if len(set(combined)) == 15 else None

# Función para procesar en paralelo con tqdm
def process_combinations(chunk):
    results = []
    for word1 in tqdm(chunk, desc="Procesando", position=0, leave=True):
        remaining_words = [w for w in words if not set(w) & set(word1)]
        for word2, word3 in combinations(remaining_words, 2):
            result = check_combination(word1, word2, word3)
            if result:
                results.append(result)
    return results

if __name__ == "__main__":
    num_workers = max(1, cpu_count() - 1)  # Usamos todos los núcleos menos uno

    print(f"Usando {num_workers} procesos en paralelo...")

    # Dividir las palabras de oneVowel.txt en chunks
    chunk_size = max(1, len(one_vowel_words) // num_workers)
    chunks = [one_vowel_words[i:i + chunk_size] for i in range(0, len(one_vowel_words), chunk_size)]

    print(f"Total de lotes a procesar: {len(chunks)}")

    # Crear un pool de procesos
    with Pool(num_workers) as pool:
        results = pool.map(process_combinations, chunks)

    # Flatten de la lista de resultados
    unique_combinations = [combo for sublist in results for combo in sublist]

    # Guardar resultados en un CSV
    df = pd.DataFrame(unique_combinations, columns=["Palabra 1", "Palabra 2", "Palabra 3"])
    df.to_csv("resultados_filtrados.csv", index=False)

    print("Resultados guardados en 'resultados_filtrados.csv'")
    print(f"Se encontraron {len(unique_combinations)} tríos de palabras que suman 15 letras únicas.")
