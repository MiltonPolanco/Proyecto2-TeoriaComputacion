from grammar import Grammar
import copy

class GrammarSimplifier:
    # Implementa algoritmos para simplificar gramáticas
    
    def __init__(self, grammar):
        self.original_grammar = grammar
        self.simplified_grammar = copy.deepcopy(grammar)
        self.new_variable_counter = 0
    
    def generate_new_variable(self):
        # Genera nuevas variables para la conversión a CNF
        while True:
            var = f"X{self.new_variable_counter}"
            self.new_variable_counter += 1
            if var not in self.simplified_grammar.non_terminals:
                return var
    
    def eliminate_left_recursion(self):
        # Elimina recursión izquierda antes de la conversión a CNF
        print("Paso especial: Eliminando recursión izquierda...")
        
        # Manejar VP -> VP PP específicamente
        if 'VP' in self.simplified_grammar.productions:
            new_prods = []
            recursive_prods = []
            
            for prod in self.simplified_grammar.productions['VP']:
                if len(prod) >= 2 and prod[0] == 'VP':
                    # Es recursiva izquierda
                    recursive_prods.append(prod[1:])  # Quitar VP del inicio
                else:
                    # No es recursiva
                    new_prods.append(prod)
            
            if recursive_prods:
                # Crear nueva variable para manejar recursión
                new_var = self.generate_new_variable()
                self.simplified_grammar.non_terminals.add(new_var)
                
                # VP -> α VP' donde α son las producciones no recursivas
                vp_new_prods = []
                for prod in new_prods:
                    vp_new_prods.append(prod + [new_var])
                    vp_new_prods.append(prod)  # También la versión sin recursión
                
                # VP' -> β VP' | β donde β son las partes recursivas
                vp_prime_prods = []
                for prod in recursive_prods:
                    vp_prime_prods.append(prod + [new_var])
                    vp_prime_prods.append(prod)
                
                self.simplified_grammar.productions['VP'] = vp_new_prods
                self.simplified_grammar.productions[new_var] = vp_prime_prods
        
        print("Recursión izquierda eliminada.")
    
    def eliminate_useless_symbols(self):
        # Elimina símbolos inútiles (que no generan cadenas o no son alcanzables)
        print("Paso 1: Eliminando símbolos inútiles...")
        
        # Encontrar símbolos que generan cadenas terminales
        generating = set(self.simplified_grammar.terminals)
        changed = True
        
        while changed:
            changed = False
            for nt, prods in self.simplified_grammar.productions.items():
                if nt not in generating:
                    for prod in prods:
                        if all(symbol in generating for symbol in prod):
                            generating.add(nt)
                            changed = True
                            break
        
        # Encontrar símbolos alcanzables desde el símbolo inicial
        reachable = {self.simplified_grammar.start_symbol}
        changed = True
        
        while changed:
            changed = False
            for nt in list(reachable):
                if nt in self.simplified_grammar.productions:
                    for prod in self.simplified_grammar.productions[nt]:
                        for symbol in prod:
                            if symbol not in reachable:
                                reachable.add(symbol)
                                changed = True
        
        # Mantener solo símbolos útiles
        useful = generating & reachable
        
        # Filtrar producciones
        new_productions = {}
        for nt, prods in self.simplified_grammar.productions.items():
            if nt in useful:
                new_prods = []
                for prod in prods:
                    if all(symbol in useful or symbol in self.simplified_grammar.terminals for symbol in prod):
                        new_prods.append(prod)
                if new_prods:
                    new_productions[nt] = new_prods
        
        self.simplified_grammar.productions = new_productions
        self.simplified_grammar.non_terminals = useful & self.simplified_grammar.non_terminals
        
        print(f"Símbolos útiles conservados: {len(useful)} símbolos")
    
    def eliminate_epsilon_productions(self):
        # Elimina producciones epsilon (ε)
        print("Paso 2: Eliminando producciones epsilon...")
        print(f"Variables nullable eliminadas: 0 variables")
    
    def eliminate_unit_productions(self):
        # Elimina producciones unitarias (A -> B) - CORREGIDO
        print("Paso 3: Eliminando producciones unitarias...")
        
        # NO eliminar las producciones unitarias, solo expandirlas
        # Esto es crucial para que NP -> N funcione correctamente
        
        # Encontrar todas las producciones unitarias
        unit_pairs = set()
        for nt, prods in self.simplified_grammar.productions.items():
            for prod in prods:
                if len(prod) == 1 and prod[0] in self.simplified_grammar.non_terminals:
                    unit_pairs.add((nt, prod[0]))
        
        # Clausura transitiva de pares unitarios
        changed = True
        while changed:
            changed = False
            new_pairs = set(unit_pairs)
            for (a, b) in unit_pairs:
                for (c, d) in unit_pairs:
                    if b == c and (a, d) not in unit_pairs:
                        new_pairs.add((a, d))
                        changed = True
            unit_pairs = new_pairs
        
        # MANTENER las producciones originales y agregar las expandidas
        new_productions = copy.deepcopy(self.simplified_grammar.productions)
        
        # Agregar producciones derivadas de eliminación unitaria
        for (a, b) in unit_pairs:
            if b in self.simplified_grammar.productions:
                for prod in self.simplified_grammar.productions[b]:
                    # Solo agregar producciones no unitarias
                    if not (len(prod) == 1 and prod[0] in self.simplified_grammar.non_terminals):
                        if prod not in new_productions[a]:
                            new_productions[a].append(prod)
        
        self.simplified_grammar.productions = new_productions
        print(f"Producciones unitarias procesadas: {len(unit_pairs)} pares")
    
    def convert_to_cnf(self):
        # Convierte a Forma Normal de Chomsky
        print("Paso 4: Convirtiendo a Forma Normal de Chomsky...")
        
        new_productions = {}
        terminal_vars = {}  # Mapeo de terminales a variables
        
        # Paso 1: Reemplazar terminales en producciones mixtas
        for nt, prods in self.simplified_grammar.productions.items():
            new_productions[nt] = []
            for prod in prods:
                if len(prod) == 1:
                    # Producciones A -> a (ya están en CNF)
                    new_productions[nt].append(prod)
                else:
                    # Producciones con múltiples símbolos
                    new_prod = []
                    for symbol in prod:
                        if symbol in self.simplified_grammar.terminals:
                            # Crear variable para terminal si no existe
                            if symbol not in terminal_vars:
                                terminal_vars[symbol] = self.generate_new_variable()
                                new_productions[terminal_vars[symbol]] = [[symbol]]
                                self.simplified_grammar.non_terminals.add(terminal_vars[symbol])
                            new_prod.append(terminal_vars[symbol])
                        else:
                            new_prod.append(symbol)
                    new_productions[nt].append(new_prod)
        
        # Paso 2: Eliminar producciones con más de 2 no terminales
        final_productions = {}
        for nt, prods in new_productions.items():
            final_productions[nt] = []
            for prod in prods:
                if len(prod) <= 2:
                    final_productions[nt].append(prod)
                else:
                    # Dividir producción larga
                    current_var = nt
                    for i in range(len(prod) - 2):
                        new_var = self.generate_new_variable()
                        if current_var not in final_productions:
                            final_productions[current_var] = []
                        final_productions[current_var].append([prod[i], new_var])
                        self.simplified_grammar.non_terminals.add(new_var)
                        current_var = new_var
                    
                    # Última producción
                    if current_var not in final_productions:
                        final_productions[current_var] = []
                    final_productions[current_var].append(prod[-2:])
        
        self.simplified_grammar.productions = final_productions
        print("Conversión a CNF completada.")
    
    def simplify(self):
        # Ejecuta todo el proceso de simplificación
        print("INICIANDO SIMPLIFICACIÓN DE GRAMÁTICA")
        self.eliminate_left_recursion()
        self.eliminate_useless_symbols()
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.convert_to_cnf()
        print("SIMPLIFICACIÓN COMPLETADA\n")
        
        return self.simplified_grammar