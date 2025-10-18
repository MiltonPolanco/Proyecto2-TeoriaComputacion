# Proyecto2-TeoriaComputacion

## Descripción

Implementación del algoritmo CYK (Cocke-Younger-Kasami) para el análisis sintáctico de oraciones en inglés. El proyecto incluye simplificación de gramáticas libres de contexto y conversión a Forma Normal de Chomsky (CNF).

## Características

- **Simplificación automática de gramáticas** con eliminación de símbolos inútiles, producciones epsilon y unitarias
- **Conversión a CNF** completa y funcional
- **Algoritmo CYK** con construcción de árboles de análisis sintáctico
- **Modo interactivo** para probar oraciones
- **Visualización de tablas CYK** para debugging
- **Suite de pruebas** con casos válidos e inválidos

## Estructura del Proyecto

```
├── main.py                  # Archivo principal con demo y modo interactivo
├── grammar.py               # Clase para representar gramáticas
├── grammar_simplifier.py    # Simplificación y conversión a CNF
├── cyk_algorithm.py         # Implementación del algoritmo CYK
└── test_examples.py         # Suite de pruebas exhaustivas
```

## Instalación y Uso

### Requisitos

- Python
- No requiere librerías externas

### Ejecución

```bash
# Ejecutar demo completo
python main.py

# Ejecutar suite de pruebas
python test_examples.py
```

## Funcionalidades

### Oraciones Soportadas

El sistema reconoce oraciones en inglés con la siguiente estructura:

- **Simples**: "she eats", "he drinks"
- **Con objetos**: "she eats cake", "the cat drinks beer"
- **Con frases preposicionales**: "she eats cake with a fork"
- **Complejas**: "the cat drinks beer in the oven"

### Vocabulario Incluido

- **Sujetos**: she, he, the cat, the dog
- **Verbos**: cooks, drinks, eats, cuts
- **Objetos**: cake, beer, meat, soup, fork, knife, oven, spoon
- **Preposiciones**: in, with
- **Determinantes**: a, the

## Ejemplo de Uso

```python
from main import load_english_grammar
from grammar_simplifier import GrammarSimplifier
from cyk_algorithm import CYKParser

# Cargar y simplificar gramática
grammar = load_english_grammar()
simplifier = GrammarSimplifier(grammar)
cnf_grammar = simplifier.simplify()

# Analizar oración
parser = CYKParser(cnf_grammar)
result = parser.parse("she eats cake with a fork")
print(f"Resultado: {'ACEPTADA' if result else 'RECHAZADA'}")
```

## Resultados de Pruebas

- **Precisión**: 100% (11/11 casos correctos)
- **Tiempo promedio**: < 0.0003 segundos por oración
- **Cobertura**: Oraciones simples, complejas y casos límite

## Autores

- Milton Giovanni Polanco Serrano 23471
- Gadiel Ocaña 231270

## Notas Técnicas

- La gramática se convierte automáticamente a CNF
- Se maneja recursión izquierda mediante variables auxiliares
- El algoritmo construye árboles de análisis sintáctico completos
- Incluye visualización detallada de tablas CYK para debugging

# Video 


Link: https://youtu.be/CZHhezXbEBA


