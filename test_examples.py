from main import load_english_grammar, test_sentences
from grammar_simplifier import GrammarSimplifier
from cyk_algorithm import CYKParser

def run_comprehensive_tests():
    """Ejecuta pruebas exhaustivas del sistema"""
    print("PRUEBAS EXHAUSTIVAS DEL SISTEMA\n")
    
    # Cargar y preparar gramática
    grammar = load_english_grammar()
    simplifier = GrammarSimplifier(grammar)
    cnf_grammar = simplifier.simplify()
    parser = CYKParser(cnf_grammar)
    
    # Casos de prueba adicionales
    test_cases = [
        # Casos válidos más complejos
        ("she eats cake with a fork", True),
        ("the dog drinks beer in the oven", True),
        ("he cuts the meat with the knife", True),
        
        # Casos inválidos específicos
        ("she eats with", False),
        ("the cat the dog", False),
        ("drinks beer she", False),
        ("a cuts meat", False),
        
        # Casos límite
        ("she cooks", True),
        ("he drinks", True),
        ("the cat eats", True),
        ("she", False),
    ]
    
    print("Ejecutando casos de prueba...")
    print("=" * 60)
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for sentence, expected in test_cases:
        is_valid, parse_time, parse_tree = parser.parse(sentence)
        
        status = "✓ CORRECTO" if is_valid == expected else "✗ ERROR"
        result_text = "ACEPTADA" if is_valid else "RECHAZADA"
        expected_text = "VÁLIDA" if expected else "INVÁLIDA"
        
        print(f"Oración: '{sentence}'")
        print(f"Esperado: {expected_text} | Obtenido: {result_text} | {status}")
        print(f"Tiempo: {parse_time:.6f}s")
        
        if is_valid == expected:
            correct_predictions += 1
        
        print("-" * 40)
    
    accuracy = (correct_predictions / total_tests) * 100
    print(f"\nRESULTADOS FINALES:")
    print(f"Pruebas correctas: {correct_predictions}/{total_tests}")
    print(f"Precisión: {accuracy:.1f}%")
    
    return accuracy >= 90  # Retorna True si la precisión es >= 90%

if __name__ == "__main__":
    success = run_comprehensive_tests()
    print(f"\nPruebas {'EXITOSAS' if success else 'FALLIDAS'}")