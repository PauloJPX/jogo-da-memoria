import tkinter as tk
from PIL import Image, ImageTk
import os,sys
import random
import threading
import time

# novo 15:30

def get_resource_path(relative_path):
    """Obter o caminho do recurso embutido ou do sistema de arquivos."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)



class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Configurar a geometria responsiva
        self.root.geometry(f"{self.screen_width - 100}x{self.screen_height - 100}")
        self.root.resizable(True, True)  # Permite redimensionamento

        # Inicializar variáveis do jogo
        self.pontos1 = 0
        self.pontos2 = 0
        self.jogador1 = True
        self.selected_buttons = []
        self.selected_positions = []
        self.partidas_1 = 0
        self.partidas_2 = 0

        #image_path = get_resource_path("cards/")
        self.image_folder = get_resource_path("cards/") # Caminho para as imagens

        self.card_images = []
        self.capa = None

        # Carregar as imagens
        self.load_images()

        # Widgets iniciais
        self.create_widgets()

        # Inicializar labels
        self.atualizar_labels()



    def load_images(self):
        """Carrega as imagens dos cards."""
        for filename in os.listdir(self.image_folder):
            if filename.endswith(".jpg"):
                img = Image.open(os.path.join(self.image_folder, filename))
                img = img.resize((100, 100))  # Ajuste inicial, depois será redimensionado dinamicamente
                if filename == "capa.jpg":
                    self.capa = ImageTk.PhotoImage(img)
                else:
                    self.card_images.append(ImageTk.PhotoImage(img))

        if not self.capa:
            raise ValueError("A imagem 'capa.jpg' não foi encontrada na pasta!")

    def create_widgets(self):
        """Cria os widgets do jogo."""
        # Entradas dos jogadores
        tk.Label(self.root, text="Jogador 1: ").grid(row=0, column=0, sticky="w", padx=10)
        tk.Label(self.root, text="Jogador 2:").grid(row=0, column=3, sticky="w", padx=10)

        self.jog1_entry = tk.Entry(self.root, width=15)
        self.jog1_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="w")

        self.jog2_entry = tk.Entry(self.root, width=15)
        self.jog2_entry.grid(row=0, column=4, padx=(0, 10), pady=5, sticky="w")

        # Labels de pontos e status
        self.pontos1_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.pontos1_label.grid(row=0, column=9, sticky="w", padx=10)

        self.pontos2_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.pontos2_label.grid(row=1, column=9, sticky="w", padx=10)

        self.jogador_atual_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.jogador_atual_label.grid(row=2, column=9, sticky="w", padx=10)

        self.partidas1_label = tk.Label(self.root, text="0", font=("Arial", 15), bg="green", fg="white")
        self.partidas1_label.grid(row=0, column=10, sticky="w")

        self.partidas2_label = tk.Label(self.root, text="0", font=("Arial", 15), bg="red", fg="white")
        self.partidas2_label.grid(row=1, column=10, sticky="w")

        self.lblvencedor = tk.Label(self.root, text="Quem será o Vencedor???", font=("Arial", 12))
        self.lblvencedor.grid(row=4, column=9, sticky="w")

        # Botão de reinício
        restart_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game, font=("Arial", 12))
        restart_button.grid(row=5, column=9, padx=10, pady=10)

        # Criar tabuleiro
        self.create_board()

    def create_board(self):
        """Cria o tabuleiro do jogo."""
        self.positions = list(range(1, 41))
        random.shuffle(self.positions)

        # Associar imagens às posições
        self.cards_with_positions = []
        for image in self.card_images:
            if len(self.positions) >= 2:
                pos1 = self.positions.pop()
                pos2 = self.positions.pop()
                self.cards_with_positions.append((image, pos1, pos2))

        # Criar botões
        self.buttons = []
        rows, cols = 5, 8
        position = 1
        for row in range(rows):
            for col in range(cols):
                def create_button(pos):
                    btn = tk.Button(self.root, image=self.capa, width=100, height=100)
                    btn.config(command=lambda b=btn, p=pos: self.on_button_click(p, b))
                    btn.grid(row=row + 1, column=col, padx=5, pady=5, sticky="nsew")
                    self.buttons.append(btn)

                create_button(position)
                position += 1

        # Ajustar layout para que os botões ocupem o espaço disponível
        for row in range(rows):
            self.root.grid_rowconfigure(row + 1, weight=1, minsize=100)  # Ajuste automático de altura
        for col in range(cols):
            self.root.grid_columnconfigure(col, weight=1, minsize=100)  # Ajuste automático de largura

    def atualizar_labels(self):
        """Atualiza os labels do jogo."""
        vez = self.jog1_entry.get() if self.jogador1 else self.jog2_entry.get()
        self.pontos1_label.config(text=f"{self.jog1_entry.get().upper()}: {self.pontos1} ",fg="green",bg="white")
        self.pontos2_label.config(text=f"{self.jog2_entry.get().upper()}: {self.pontos2} ",fg="red",bg="white")
        self.jogador_atual_label.config(text=f"{vez.upper()} ", font=("Arial", 20, "bold"))
        # Inicia o piscamento
        self.blink_text()

    def blink_text(self):

        """Cria o efeito de piscamento no texto do label."""
        current_color = self.jogador_atual_label.cget("fg")
        if self.jogador1:
             new_color = "green" if current_color == "white" else "white"
        else:
            new_color = "red" if current_color == "white" else "white"
        self.jogador_atual_label.config(fg=new_color)
        # Alterna a cor a cada 500 ms
        self.root.after(1000, self.blink_text)



    def on_button_click(self, position, button):
        if button in self.selected_buttons:
            # Se o botão já foi selecionado, não faz nada
            return
        """Lida com cliques nos botões do tabuleiro."""
        if len(self.selected_buttons) < 2:
            for card, pos1, pos2 in self.cards_with_positions:
                if position == pos1 or position == pos2:
                    print('escolhido na mesma posicao')
                    print(pos1,pos2)

                    button.config(image=card)
                    self.selected_buttons.append(button)
                    self.selected_positions.append(position)

            if len(self.selected_buttons) == 2:
                threading.Thread(target=self.check_match).start()

    def check_match(self):
        """Verifica se os cards selecionados formam um par."""
        if len(self.selected_buttons) == 2:
            btn1, btn2 = self.selected_buttons
            pos1, pos2 = self.selected_positions

            img1 = next(card[0] for card in self.cards_with_positions if pos1 in card[1:])
            img2 = next(card[0] for card in self.cards_with_positions if pos2 in card[1:])

            if img1 == img2 and pos1 != pos2:
                btn1.config(state=tk.DISABLED)
                btn2.config(state=tk.DISABLED)
                if self.jogador1:
                    self.pontos1 += 1
                else:
                    self.pontos2 += 1

                if self.pontos1 + self.pontos2 == 20:
                    if self.pontos1 > self.pontos2:
                        self.lblvencedor.config(text=f"Vencedor foi {self.jog1_entry.get()}")
                        self.partidas_1 += 1
                    elif self.pontos1 < self.pontos2:
                        self.lblvencedor.config(text=f"Vencedor foi {self.jog2_entry.get()}")
                        self.partidas_2 += 1
                    else:
                        self.lblvencedor.config(text="***E M P A T E***")
                    self.partidas1_label.config(text=self.partidas_1)
                    self.partidas2_label.config(text=self.partidas_2)
            else:
                time.sleep(2)
                btn1.config(image=self.capa)
                btn2.config(image=self.capa)
                self.jogador1 = not self.jogador1

            self.atualizar_labels()
            self.selected_buttons = []
            self.selected_positions = []

    def reset_game(self):
        """Reinicia o estado do jogo."""
        self.pontos1 = 0
        self.pontos2 = 0
        self.jogador1 = True
        self.selected_buttons = []
        self.selected_positions = []
        self.lblvencedor.config(text="Quem será o Vencedor???")
        for btn in self.buttons:
            btn.destroy()
        self.create_board()
        self.atualizar_labels()


# Executar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
