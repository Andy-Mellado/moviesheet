import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests
import pandas as pd
from googletrans import Translator
from movie_details import get_movie_details

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Info App")

        # Define fonts and colors
        self.font_label = ("Arial", 12, "bold")
        self.font_text = ("Arial", 11)
        self.bg_color = "lightblue"

        # Configura la grilla principal
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=3)

        # Parte superior: Entrada y botón de búsqueda
        self.entry_frame = tk.Frame(self.root, bg=self.bg_color)
        self.entry_frame.grid(row=0, column=0, columnspan=2, pady=10)

        self.label = tk.Label(self.entry_frame, text="Ingrese el título de la película:", font=self.font_label, bg=self.bg_color)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        self.entry = tk.Entry(self.entry_frame, width=40, font=self.font_text)
        self.entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.entry_frame, text="Buscar", command=self.get_movie_info, font=self.font_label)
        self.search_button.grid(row=0, column=2, padx=10, pady=5)

        # Parte izquierda: Imagen de la película
        self.image_frame = tk.Frame(self.root, bg=self.bg_color)
        self.image_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame, bg=self.bg_color)
        self.image_label.pack()

        # Parte inferior de la imagen: Detalles
        self.details_frame = tk.Frame(self.image_frame, bg=self.bg_color)
        self.details_frame.pack(fill="x", pady=10)

        self.details_text = tk.Text(self.details_frame, height=6, width=40, font=self.font_text)
        self.details_text.pack()

        # Parte inferior izquierda: Descripción (más pequeña)
        self.description_frame = tk.Frame(self.root, bg=self.bg_color)
        self.description_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.description_text = tk.Text(self.description_frame, height=7, width=60, font=self.font_text, wrap="word")
        self.description_text.pack(fill="both", expand=True)

        # Parte inferior derecha: Otras películas del director
        self.director_frame = tk.Frame(self.root, bg=self.bg_color)
        self.director_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.director_text = tk.Text(self.director_frame, height=10, width=60, font=self.font_text, wrap="word")
        self.director_text.pack(fill="both", expand=True)

    def get_movie_info(self):
        api_key = 'ca4eedbef7c1befd3e215c4f598fb1d9'
        translator = Translator()

        movie_title = self.entry.get()
        movie_details = get_movie_details(movie_title, api_key)

        if movie_details:
            translated = translator.translate(movie_details['overview'], dest='es')

            # Mostrar la información en las áreas correspondientes
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Puntuación: {movie_details['rating']}\n")
            self.details_text.insert(tk.END, f"Idioma: {movie_details['languaje']}\n")
            self.details_text.insert(tk.END, f"Actores: {', '.join(movie_details['actors'])}\n")

            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, translated.text)

            self.director_text.delete(1.0, tk.END)
            self.director_text.insert(tk.END, pd.DataFrame(movie_details['director']).to_string())

            if movie_details['poster']:
                poster_url = f"https://image.tmdb.org/t/p/w500{movie_details['poster']}"
                response = requests.get(poster_url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))

                # Mantener la proporción de la imagen
                img.thumbnail((300, 450), Image.Resampling.LANCZOS)  # Tamaño máximo permitido manteniendo la proporción
                img_tk = ImageTk.PhotoImage(img)

                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
            else:
                self.image_label.config(image=None)
        else:
            messagebox.showinfo("No encontrado", f"No se encontraron resultados para '{movie_title}'")

def main():
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
