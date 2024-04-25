from tkinter import *
from tkinter import messagebox 
from tkinter import PhotoImage

import random

class SnakeApp():
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.geometry("450x480")
        self.root.configure(bg='#654321')
        self.root.resizable(width=False, height=False)

        # Crear un lienzo (canvas) en el centro de la ventana
        self.canvas = Canvas(root, width=400, height=400, bg='black', highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Etiqueta para mostrar la puntuación
        self.score_label = Label(root, text="Puntuación: 0", font=("Arial", 14), bg='#654321', fg='white')
        self.score_label.place(relx=0.5, rely=0.05, anchor=CENTER)

        # Tamaño de cada cuadrado
        self.square_size = 20

        # Arreglo para almacenar los cuadrados que forman la serpiente
        self.snake = []

        # Posición inicial de la serpiente
        self.snake_x = 100
        self.snake_y = 100

        # Dirección inicial de la serpiente (derecha)
        self.direction = {'x': 1, 'y': 0}

        #Longitud de la serpiente (inicial)
        self.initial_length = 3 

        # Agregar una variable para verificar si el juego está en curso o no
        self.game_over = False

        # Asociar eventos de teclado para cambiar la dirección de la serpiente
        self.root.bind("<Up>", lambda event: self.change_direction(0, -1))
        self.root.bind("<Down>", lambda event: self.change_direction(0, 1))
        self.root.bind("<Left>", lambda event: self.change_direction(-1, 0))
        self.root.bind("<Right>", lambda event: self.change_direction(1, 0))

        # Dibujar la serpiente inicialmente
        self.create_snake()

        # Dibujar un cuadro rojo de manera aleatoria en el lienzo
        self.place_red_square()

        # Comenzar el movimiento de la serpiente
        self.move()

        # Puntuación inicial
        self.score = 0

    def change_direction(self, x, y):
        # Cambiar la dirección de la serpiente según las teclas de dirección
        if (self.direction['x'] == 0 and x != 0) or (self.direction['y'] == 0 and y != 0):
            self.direction['x'] = x
            self.direction['y'] = y

    def create_snake(self):
        # Dibujar la serpiente inicialmente
        for i in range(self.initial_length):  # Cambiado a 3 para crear tres cuadrados iniciales
            x1 = self.snake_x - i * self.square_size
            y1 = self.snake_y
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            square = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#568203')
            self.snake.append(square)

    def place_red_square(self):
        # Dibujar un cuadro rojo de manera aleatoria en el lienzo
        self.x1_r = (400 - self.square_size) / 2
        self.y1_r = (400 - self.square_size) / 2
        self.x2_r = self.x1_r + self.square_size
        self.y2_r = self.y1_r + self.square_size

        # Crear el rectángulo rojo
        self.rect_2  = self.canvas.create_rectangle(self.x1_r, self.y1_r, self.x2_r, self.y2_r, fill='red')



    def move(self):
        if not self.game_over:
            # Mover la serpiente en la dirección actual
            self.snake_x += self.direction['x'] * self.square_size 
            self.snake_y += self.direction['y'] * self.square_size

            # Limitar la serpiente dentro del área del canvas
            self.snake_x %= 400
            self.snake_y %= 400

            # Verificar si la cabeza de la serpiente choca consigo misma
            if self.check_collision():
                self.end_game()

            # Actualizar la posición de cada cuadrado de la serpiente
            for i in range(len(self.snake)-1, 0, -1):
                x1, y1, x2, y2 = self.canvas.coords(self.snake[i-1])
                self.canvas.coords(self.snake[i], x1, y1, x2, y2)

            x1 = self.snake_x
            y1 = self.snake_y
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            self.canvas.coords(self.snake[0], x1, y1, x2, y2)

            # Verificar si hay colisión entre la serpiente y el cuadrado rojo
            head_coords = self.canvas.coords(self.snake[0])
            x1_r, y1_r, x2_r, y2_r = self.canvas.coords(self.rect_2)
            if (head_coords[0] < x2_r and head_coords[2] > x1_r) and (head_coords[1] < y2_r and head_coords[3] > y1_r):
                # Si hay colisión, mover el cuadrado rojo a una nueva posición aleatoria
                self.randomize_red_square_position()
                # Aumentar la longitud de la serpiente
                self.extend_snake()
                # Actualizar la puntuación
                self.score += 1
                self.score_label.config(text=f"Puntuación: {self.score}")

        # Repetir el movimiento después de un cierto tiempo (en milisegundos)
        self.root.after(100, self.move)

    def randomize_red_square_position(self):
        # Mover el cuadrado rojo a una nueva posición aleatoria
        r = random.choice(range(0, 400, self.square_size))  # Nueva posición aleatoria múltiplo del tamaño del cuadrado
        self.canvas.coords(self.rect_2, r, r, r + self.square_size, r + self.square_size)

    def extend_snake(self):
        # Aumentar la longitud de la serpiente
        tail_coords = self.canvas.coords(self.snake[-1])
        x1 = tail_coords[0]
        y1 = tail_coords[1]
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        square = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#568203')
        self.snake.append(square)

    def check_collision(self):
        # Verificar si la cabeza de la serpiente choca consigo misma
        head_coords = self.canvas.coords(self.snake[0])
        for segment in self.snake[3:]:
            if self.canvas.coords(segment) == head_coords:
                return True
        return False

    def end_game(self):
        # Mostrar un mensaje de juego terminado si el juego no se ha reiniciado
        if not self.game_over:
            self.game_over = True
            messagebox.showinfo("Game Over", "¡Has perdido!\nPresiona aceptar")
      
            # Reiniciar el juego
            self.game_over = False
            self.reset_game()

    def reset_game(self):
        # Reiniciar el juego
        self.game_over = False

        # Restablecer la posición y dirección de la serpiente
        self.snake_x = 100
        self.snake_y = 100
        self.direction = {'x': 1, 'y': 0}

        # Borrar todos los elementos en el lienzo
        self.canvas.delete("all")

        # Recrear la serpiente inicial
        self.snake.clear()
        self.create_snake()

        # Dibujar un cuadro rojo de manera aleatoria en el lienzo
        self.place_red_square()
        # Restablecer la puntuación
        self.score = 0
        self.score_label.config(text="Puntuación: 0")

if __name__ == "__main__":
    root = Tk()
    root.iconbitmap("C:/Users/Eduardo/OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO/Escritorio/tictac/snake/snake.ico")
    game = SnakeApp(root)
    root.mainloop()
