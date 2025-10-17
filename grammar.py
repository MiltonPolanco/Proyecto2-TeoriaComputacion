class Grammar:
    """Clase para representar y manipular gramáticas libres de contexto"""
    
    def __init__(self):
        self.productions = {}
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = None
        
    def add_production(self, left, right):
        # Agrega una producción a la gramática
        if left not in self.productions:
            self.productions[left] = []
        self.productions[left].append(right)
        self.non_terminals.add(left)
        
        # Identificar terminales (palabras en minúsculas que no aparecen como lado izquierdo)
        for symbol in right:
            if symbol.islower() or symbol in ['(', ')', '+', '*']:
                self.terminals.add(symbol)
    
    def set_start_symbol(self, symbol):
        # Establece el símbolo inicial
        self.start_symbol = symbol
    
    def load_from_text(self, grammar_text):
        # Carga gramática desde texto
        lines = grammar_text.strip().split('\n')
        for line in lines:
            if '->' in line:
                left, right_side = line.split('->', 1)
                left = left.strip()
                
                # Manejar múltiples producciones separadas por |
                alternatives = right_side.split('|')
                for alt in alternatives:
                    right = alt.strip().split()
                    if right:  # Solo agregar si no está vacío
                        self.add_production(left, right)
        
        # El primer símbolo es el inicial por defecto
        if self.productions and not self.start_symbol:
            self.start_symbol = list(self.productions.keys())[0]
        
        # Limpiar terminales: remover símbolos que son no terminales
        self.terminals = self.terminals - self.non_terminals
    
    def display(self):
        # Muestra la gramática de forma legible
        print("GRAMÁTICA")
        print(f"Símbolo inicial: {self.start_symbol}")
        print("Producciones:")
        for nt in sorted(self.productions.keys()):
            for prod in self.productions[nt]:
                print(f"  {nt} -> {' '.join(prod)}")
        print(f"Terminales: {sorted(self.terminals)}")
        print(f"No terminales: {sorted(self.non_terminals)}")