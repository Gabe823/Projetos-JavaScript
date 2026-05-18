import tkinter as tk
from tkinter import font as tkfont

class CalculadoraWindows:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora")
        self.janela.geometry("360x520")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#1e1e1e")
        
        # Fonte
        self.fonte_display = tkfont.Font(family="Segoe UI", size=28, weight="normal")
        self.fonte_botoes = tkfont.Font(family="Segoe UI", size=14)
        
        self.expressao = ""
        self.resultado = ""
        
        # Display
        self.frame_display = tk.Frame(self.janela, bg="#1e1e1e")
        self.frame_display.pack(pady=20, padx=20, fill="x")
        
        self.display = tk.Label(
            self.frame_display,
            text="0",
            anchor="e",
            bg="#1e1e1e",
            fg="#ffffff",
            font=self.fonte_display,
            height=2
        )
        self.display.pack(fill="x", padx=10)
        
        # Frame dos botões
        self.frame_botoes = tk.Frame(self.janela, bg="#1e1e1e")
        self.frame_botoes.pack(padx=20, pady=10)
        
        self.criar_botoes()
        
        # Bind de teclado
        self.janela.bind("<Key>", self.tecla_pressionada)
        
    def criar_botoes(self):
        botoes = [
            ('%', 0, 0), ('CE', 0, 1), ('C', 0, 2), ('⌫', 0, 3),
            ('¹/ₓ', 1, 0), ('x²', 1, 1), ('√x', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('−', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3),
        ]
        
        self.botoes_dict = {}
        
        for (texto, linha, coluna) in botoes:
            if texto in ['=', '÷', '×', '−', '+']:
                cor_bg = "#ff9500"
                cor_fg = "white"
            elif texto in ['C', 'CE', '⌫']:
                cor_bg = "#a6a6a6"
                cor_fg = "black"
            else:
                cor_bg = "#333333"
                cor_fg = "white"
            
            btn = tk.Button(
                self.frame_botoes,
                text=texto,
                font=self.fonte_botoes,
                bg=cor_bg,
                fg=cor_fg,
                activebackground="#555555",
                relief="flat",
                height=2,
                width=6 if texto != '=' else 6,
                command=lambda t=texto: self.clicar(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew")
            self.botoes_dict[texto] = btn
            
        # Configurar peso das colunas e linhas
        for i in range(4):
            self.frame_botoes.columnconfigure(i, weight=1)
        for i in range(6):
            self.frame_botoes.rowconfigure(i, weight=1)
    
    def clicar(self, valor):
        if valor == 'C':
            self.expressao = ""
            self.resultado = ""
            self.atualizar_display("0")
            
        elif valor == 'CE':
            self.expressao = ""
            self.atualizar_display("0")
            
        elif valor == '⌫':
            if self.expressao:
                self.expressao = self.expressao[:-1]
                if not self.expressao:
                    self.atualizar_display("0")
                else:
                    self.atualizar_display(self.expressao)
                    
        elif valor == '=':
            try:
                # Substituir símbolos para eval
                expr = self.expressao.replace('×', '*').replace('÷', '/').replace('−', '-')
                resultado = eval(expr)
                # Formatar resultado
                if isinstance(resultado, float):
                    if resultado.is_integer():
                        resultado = int(resultado)
                self.resultado = str(resultado)
                self.atualizar_display(self.resultado)
                self.expressao = self.resultado
            except:
                self.atualizar_display("Erro")
                self.expressao = ""
                
        elif valor == '±':
            if self.expressao and self.expressao != "0":
                if self.expressao.startswith('-'):
                    self.expressao = self.expressao[1:]
                else:
                    self.expressao = '-' + self.expressao
                self.atualizar_display(self.expressao)
                
        elif valor == '%':
            try:
                if self.expressao:
                    resultado = float(self.expressao) / 100
                    self.expressao = str(resultado)
                    self.atualizar_display(self.expressao)
            except:
                pass
                
        elif valor == 'x²':
            try:
                if self.expressao:
                    resultado = float(self.expressao) ** 2
                    self.expressao = str(resultado)
                    self.atualizar_display(self.expressao)
            except:
                pass
                
        elif valor == '√x':
            try:
                if self.expressao:
                    resultado = float(self.expressao) ** 0.5
                    self.expressao = str(resultado)
                    self.atualizar_display(self.expressao)
            except:
                pass
                
        elif valor == '¹/ₓ':
            try:
                if self.expressao:
                    resultado = 1 / float(self.expressao)
                    self.expressao = str(resultado)
                    self.atualizar_display(self.expressao)
            except:
                pass
                
        else:
            # Dígitos, operadores e ponto
            if valor in '0123456789.' or valor in '+-×÷':
                if self.resultado and valor in '+-×÷':
                    self.expressao = self.resultado
                    self.resultado = ""
                self.expressao += valor
                self.atualizar_display(self.expressao)
    
    def atualizar_display(self, texto):
        # Limitar tamanho do display
        if len(texto) > 20:
            texto = texto[:20]
        self.display.config(text=texto)
    
    def tecla_pressionada(self, evento):
        tecla = evento.char
        if tecla in '0123456789.':
            self.clicar(tecla)
        elif tecla == '+':
            self.clicar('+')
        elif tecla == '-':
            self.clicar('−')
        elif tecla == '*':
            self.clicar('×')
        elif tecla == '/':
            self.clicar('÷')
        elif tecla == '\r' or tecla == '=':
            self.clicar('=')
        elif tecla == '\x08':  # Backspace
            self.clicar('⌫')
        elif tecla.lower() == 'c':
            self.clicar('C')
    
    def rodar(self):
        self.janela.mainloop()


# ==================== EXECUTAR ====================
if __name__ == "__main__":
    calc = CalculadoraWindows()
    calc.rodar()