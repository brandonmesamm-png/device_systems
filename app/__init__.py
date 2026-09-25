# Definición de conjuntos
A = {"Ana", "Luis", "Carlos", "María", "Pedro"}      # Saben Python
B = {"Luis", "María", "Sofía", "Jorge"}              # Saben Docker

print("Conjunto A (Python):", A)
print("Conjunto B (Docker):", B)

# 1. Unión: saben Python o Docker (o ambos)
union = A | B                  # también: A.union(B)
print("\nUnión (A ∪ B):", union)

# 2. Intersección: saben ambas cosas
interseccion = A & B           # también: A.intersection(B)
print("Intersección (A ∩ B):", interseccion)

# 3. Diferencia: saben Python pero NO Docker
diferencia_A_B = A - B         # también: A.difference(B)
print("Diferencia (A - B):", diferencia_A_B)

# 4. Diferencia: saben Docker pero NO Python
diferencia_B_A = B - A
print("Diferencia (B - A):", diferencia_B_A)

# 5. Diferencia simétrica: los que saben solo una de las dos
dif_simetrica = A ^ B          # también: A.symmetric_difference(B)
print("Diferencia simétrica (A △ B):", dif_simetrica)

# 6. Complemento (respecto a un universo U)
U = {"Ana", "Luis", "Carlos", "María", "Pedro", "Sofía", "Jorge", "Daniel"}
complemento_A = U - A
print("Complemento de A:", complemento_A)

# 7. Subconjunto
C = {"Luis", "María"}
print("\n¿C es subconjunto de B?", C.issubset(B))   # True

# 8. Conjunto vacío
vacio = set()
print("¿Está vacío?", len(vacio) == 0)

# 9. Elementos comunes (verificación rápida)
print("\n¿Hay intersección entre A y B?", not A.isdisjoint(B))