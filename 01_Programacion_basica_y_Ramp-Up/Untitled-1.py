ejer_3 = ["Un", "árbol", "binario", "es", "una", "estructura",\
          "de", "un", "tipo", "particular", "a", "veces", "no",\
          "es", "ni", "binario"]

# Creo una lista vacía a la que le iré añadiendo valores
duplicados = []

# Creo una función con un argumento: el elemento que quiero saber si está duplicado
def elementos_duplicados(duplicado):
    # Creo una lista vacía donde voy a almacenar los índices de los elementos duplicados
    indices = []
    for indice, elemento in enumerate(ejer_3):
        # Voy añadiendo los indices de los elementos duplicados a la lista 'indices',
        # independientemente de si están escritos con mayúsculas o minúsculas
        if elemento == duplicado:
            indices.append(indice)
    return indices

elemento_un = elementos_duplicados("un")
elemento_es = elementos_duplicados("es")
elemento_binario = elementos_duplicados("binario")

print(f"'un' se repite en los siguientes índices: {elemento_un}\n"\
     f"'es' se repite en los siguientes índices: {elemento_es}\n"\
     f"'binario' se repite en los siguientes índices: {elemento_binario}")