import time
from grammar import Grammar

class CYKParser:
    # Implementación del algoritmo CYK para parsing
    
    def __init__(self, cnf_grammar):
        self.grammar = cnf_grammar
        self.table = None
        self.parse_table = None
        self.sentence = None
    
    def parse(self, sentence):
        # Ejecuta el algoritmo CYK en una oración
        print(f"Analizando: '{sentence}'")
        start_time = time.time()
        
        words = sentence.lower().split()
        self.sentence = words
        n = len(words)
        
        if n == 0:
            return False, 0, None
        
        # Inicializar tabla CYK
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        self.parse_table = [[{} for _ in range(n)] for _ in range(n)]
        
        # Llenar diagonal principal (palabras individuales)
        for j in range(n):
            word = words[j]
            for nt, productions in self.grammar.productions.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0] == word:
                        self.table[j][j].add(nt)
                        if nt not in self.parse_table[j][j]:
                            self.parse_table[j][j][nt] = []
                        self.parse_table[j][j][nt].append((word,))
        
        # Llenar resto de la tabla
        for length in range(2, n + 1):  # longitud de subcadena
            for i in range(n - length + 1):  # inicio de subcadena
                j = i + length - 1  # fin de subcadena
                
                for k in range(i, j):  # punto de división
                    # Buscar producciones A -> BC donde B está en [i][k] y C está en [k+1][j]
                    left_symbols = self.table[i][k]
                    right_symbols = self.table[k+1][j]
                    
                    for nt, productions in self.grammar.productions.items():
                        for prod in productions:
                            if len(prod) == 2:
                                B, C = prod[0], prod[1]
                                if B in left_symbols and C in right_symbols:
                                    self.table[i][j].add(nt)
                                    if nt not in self.parse_table[i][j]:
                                        self.parse_table[i][j][nt] = []
                                    self.parse_table[i][j][nt].append((B, C, k))
        
        end_time = time.time()
        parsing_time = end_time - start_time
        
        # Verificar si la oración es aceptada
        is_accepted = self.grammar.start_symbol in self.table[0][n-1]
        
        parse_tree = None
        if is_accepted:
            parse_tree = self.build_parse_tree(0, n-1, self.grammar.start_symbol)
        
        return is_accepted, parsing_time, parse_tree
    
    def build_parse_tree(self, i, j, symbol):
        # Construye el árbol de análisis sintáctico
        if i == j:
            # Hoja del árbol (terminal)
            return {
                'symbol': symbol,
                'word': self.sentence[i],
                'children': []
            }
        
        # Buscar la derivación en la tabla de análisis
        if symbol in self.parse_table[i][j]:
            derivations = self.parse_table[i][j][symbol]
            if derivations:
                # Tomar la primera derivación encontrada
                first_derivation = derivations[0]
                if len(first_derivation) == 3:  # Producción A -> BC
                    B, C, k = first_derivation
                    left_child = self.build_parse_tree(i, k, B)
                    right_child = self.build_parse_tree(k+1, j, C)
                    return {
                        'symbol': symbol,
                        'children': [left_child, right_child]
                    }
        
        return None
    
    def print_table(self):
        # Imprime la tabla CYK para debug
        if not self.table:
            print("No hay tabla para mostrar")
            return
        
        n = len(self.table)
        print("\nTABLA CYK")
        print("Palabras:", " ".join(self.sentence))
        print()
        
        for i in range(n-1, -1, -1):
            row = []
            for j in range(n):
                if j >= i:
                    cell_content = "{" + ", ".join(sorted(self.table[i][j])) + "}"
                    row.append(cell_content[:20].ljust(20))
                else:
                    row.append("".ljust(20))
            print(f"Fila {i}: " + " ".join(row))
        print()
    
    def print_parse_tree(self, tree, depth=0):
        # Imprime el árbol de análisis sintáctico
        if not tree:
            return
        
        indent = "  " * depth
        if 'word' in tree:
            print(f"{indent}{tree['symbol']} -> '{tree['word']}'")
        else:
            print(f"{indent}{tree['symbol']}")
            for child in tree.get('children', []):
                self.print_parse_tree(child, depth + 1)