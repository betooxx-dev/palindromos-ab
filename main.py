import tkinter as tk
from tkinter import ttk

class PalindromeValidator:
    def __init__(self):
        self.current_state = 'q0'
        self.valid_chars = {'a', 'b'}
        
    def validate(self, input_string):
        # Primero verificamos que solo contenga caracteres válidos
        if not all(c in self.valid_chars for c in input_string):
            return False
            
        # Inicializamos los apuntadores para comparar desde los extremos
        left = 0
        right = len(input_string) - 1
        
        # Comparamos caracteres desde los extremos hacia el centro
        while left < right:
            if input_string[left] != input_string[right]:
                return False
            left += 1
            right -= 1
            
        return True
        
    def process_transitions(self, input_string):
        # Esta función retorna los estados por los que pasa para la GUI
        transitions = []
        
        if not all(c in self.valid_chars for c in input_string):
            transitions.append(('q0', 'error', 'Caracteres inválidos'))
            return transitions
            
        transitions.append(('q0', 'q1', 'Inicio de validación'))
        
        left = 0
        right = len(input_string) - 1
        
        while left < right:
            current_pair = f"Comparando {input_string[left]} con {input_string[right]}"
            if input_string[left] != input_string[right]:
                transitions.append(('q1', 'qr', f"{current_pair} - No coinciden"))
                return transitions
            transitions.append(('q1', 'q1', f"{current_pair} - Coinciden"))
            left += 1
            right -= 1
            
        transitions.append(('q1', 'qa', 'Palíndromo válido'))
        return transitions

class ModernPalindromeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Validador de Palíndromos")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E3B4E")
        
        self.validator = PalindromeValidator()
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2E3B4E')
        self.style.configure('TLabel', 
                           background='#2E3B4E', 
                           foreground='white',
                           font=('Helvetica', 10))
        self.style.configure('Header.TLabel',
                           background='#2E3B4E',
                           foreground='white',
                           font=('Helvetica', 24, 'bold'))
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(self.main_frame,
                 text="Validador de Palíndromos (a,b)",
                 style='Header.TLabel').pack(pady=(0,20))
        
        # Frame de entrada
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Entrada
        self.input_var = tk.StringVar()
        entry = tk.Entry(
            input_frame,
            textvariable=self.input_var,
            font=('Helvetica', 14),
            bg='#3E4C63',
            fg='white',
            width=30
        )
        entry.pack(side=tk.LEFT, padx=10)
        
        # Botón de validación
        validate_button = tk.Button(
            input_frame,
            text="Validar",
            command=self.validate_palindrome,
            font=('Helvetica', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10
        )
        validate_button.pack(side=tk.LEFT, padx=10)
        
        # Frame para transiciones
        self.transitions_frame = tk.Frame(
            self.main_frame,
            bg='#3E4C63'
        )
        self.transitions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Resultado
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(
            self.main_frame,
            textvariable=self.result_var,
            font=('Helvetica', 12, 'bold'),
            style='TLabel'
        )
        self.result_label.pack(pady=10)
        
    def update_transitions_display(self, transitions):
        # Limpiar transiciones anteriores
        for widget in self.transitions_frame.winfo_children():
            widget.destroy()
            
        # Mostrar nuevas transiciones
        for i, (from_state, to_state, description) in enumerate(transitions):
            frame = tk.Frame(self.transitions_frame, bg='#3E4C63')
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Indicador de paso
            step = tk.Label(frame, 
                          text=f"Paso {i+1}:", 
                          font=('Helvetica', 10),
                          bg='#3E4C63',
                          fg='#B0B9C6')
            step.pack(side=tk.LEFT, padx=5)
            
            # Estados
            states = tk.Label(frame,
                            text=f"{from_state} → {to_state}",
                            font=('Helvetica', 10, 'bold'),
                            bg='#3E4C63',
                            fg='white')
            states.pack(side=tk.LEFT, padx=5)
            
            # Descripción
            desc = tk.Label(frame,
                          text=description,
                          font=('Helvetica', 10),
                          bg='#3E4C63',
                          fg='#B0B9C6')
            desc.pack(side=tk.LEFT, padx=5)
    
    def validate_palindrome(self):
        input_string = self.input_var.get().lower()
        
        # Obtener las transiciones del proceso
        transitions = self.validator.process_transitions(input_string)
        self.update_transitions_display(transitions)
        
        # Verificar el resultado final
        final_state = transitions[-1][1]
        if final_state == 'qa':
            self.result_var.set("¡Es un palíndromo!")
            self.result_label.configure(foreground="#4CAF50")
        else:
            self.result_var.set("No es un palíndromo")
            self.result_label.configure(foreground="#FF5252")

if __name__ == "__main__":
    app = ModernPalindromeGUI()
    app.root.mainloop()