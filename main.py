from grammar import Grammar
from grammar_simplifier import GrammarSimplifier
from cyk_algorithm import CYKParser

def load_english_grammar():
    """Carga la gramática del inglés del proyecto"""
    grammar_text = """
    S -> NP VP
    VP -> VP PP
    VP -> V NP
    VP -> VI
    PP -> P NP
    NP -> Det N
    NP -> N
    NP -> he
    NP -> she
    V -> cooks
    V -> drinks
    V -> eats
    V -> cuts
    VI -> cooks
    VI -> drinks
    VI -> eats
    VI -> cuts 
    P -> in
    P -> with
    N -> cat
    N -> dog
    N -> beer
    N -> cake
    N -> juice
    N -> meat
    N -> soup
    N -> fork
    N -> knife
    N -> oven
    N -> spoon
    Det -> a
    Det -> the
    """
    
    grammar = Grammar()
    grammar.load_from_text(grammar_text)
    return grammar

def test_sentences():
    # Devuelve oraciones de prueba
    valid_sentences = [
        "she eats a cake with a fork",
        "the cat drinks the beer",
        "he cuts meat with a knife",
        "she cooks soup in the oven"
    ]
    
    invalid_sentences = [
        "cat the drinks beer",
        "with fork a cake",
        "the cat dog drinks",
        "fork eats she"
    ]
    
    return valid_sentences, invalid_sentences

def main():
    print("PROYECTO 2: ALGORITMO CYK")
    print("Teoría de la Computación 2024\n")
    
    # Cargar gramática original
    print("1. Cargando gramática original...")
    original_grammar = load_english_grammar()
    original_grammar.display()
    print()
    
    # Simplificar gramática
    print("2. Simplificando gramática...")
    simplifier = GrammarSimplifier(original_grammar)
    cnf_grammar = simplifier.simplify()
    
    print("Gramática en CNF:")
    cnf_grammar.display()
    print()
    
    # Crear parser CYK
    parser = CYKParser(cnf_grammar)
    
    # Obtener oraciones de prueba
    valid_sentences, invalid_sentences = test_sentences()
    
    print("3. Probando oraciones VÁLIDAS:")
    print("=" * 50)
    for sentence in valid_sentences:
        is_valid, parse_time, parse_tree = parser.parse(sentence)
        print(f"Oración: '{sentence}'")
        print(f"Resultado: {'ACEPTADA' if is_valid else 'RECHAZADA'}")
        print(f"Tiempo: {parse_time:.6f} segundos")
        
        if is_valid and parse_tree:
            print("Árbol de análisis:")
            parser.print_parse_tree(parse_tree)
        
        print("-" * 30)
    
    print("\n4. Probando oraciones INVÁLIDAS:")
    print("=" * 50)
    for sentence in invalid_sentences:
        is_valid, parse_time, parse_tree = parser.parse(sentence)
        print(f"Oración: '{sentence}'")
        print(f"Resultado: {'ACEPTADA' if is_valid else 'RECHAZADA'}")
        print(f"Tiempo: {parse_time:.6f} segundos")
        print("-" * 30)
    
    # Modo interactivo
    print("\n5. Modo interactivo:")
    print("Ingresa oraciones para analizar (escribe 'quit' para salir):")
    
    while True:
        sentence = input("\nOración: ").strip()
        if sentence.lower() == 'quit':
            break
        
        if sentence:
            is_valid, parse_time, parse_tree = parser.parse(sentence)
            print(f"Resultado: {'ACEPTADA' if is_valid else 'RECHAZADA'}")
            print(f"Tiempo: {parse_time:.6f} segundos")
            
            if is_valid and parse_tree:
                print("Árbol de análisis:")
                parser.print_parse_tree(parse_tree)
            
            # Mostrar tabla CYK para debug
            show_table = input("¿Mostrar tabla CYK? (s/n): ").lower()
            if show_table == 's':
                parser.print_table()

if __name__ == "__main__":
    main()