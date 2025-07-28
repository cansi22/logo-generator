#################################################################
#########                   CHANGELOG                   #########
#################################################################
#
# v1.0 - Initial Version
# 
#################################################################

import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import customtkinter as ctk
import sys
import os

# === EXTERNAL VARIABLES ===
COLOR_TEXTO_DEFAULT = "#273474" # Default text color
FAVICON_PATH = "favicon.ico"  # Favicon file name, must be in the same folder as the script
LOGO_BASE_FILENAME = "logo.png"  # Base logo file name, must be in the same folder as the script

# Set dark mode and theme for the interface
ctk.set_appearance_mode("dark")  # Modes: "light", "dark", "system"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

class LogoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Logos con Nombre")
        self.resizable(False, False)  # Window is not resizable

        # Favicon (window icon)
        try:
            self.iconbitmap(FAVICON_PATH)
        except Exception:
            pass  # If favicon does not exist, do nothing

        # Get the script directory path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # Temporary folder if packaged with PyInstaller
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.image_path = os.path.join(base_path, LOGO_BASE_FILENAME)  # Path to base logo
        self.text_color = COLOR_TEXTO_DEFAULT  # Default text color

        # Load the base image
        self.original_image = Image.open(self.image_path)
        self.display_image = ImageTk.PhotoImage(self.original_image)

        # Configure the main column to expand
        self.grid_columnconfigure(0, weight=1)

        # Label to display the image (preview)
        self.image_label = ctk.CTkLabel(self, image=self.display_image, text="")
        self.image_label.grid(row=0, column=0, padx=20, pady=20)

        # Controls frame (inputs and buttons)
        controls = ctk.CTkFrame(self)
        controls.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        controls.grid_columnconfigure(0, weight=1)

        # Label and textbox for the name (multiline)
        name_label = ctk.CTkLabel(controls, text="Nombre:")
        name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = ctk.CTkTextbox(controls, width=400, height=80)
        self.name_entry.grid(row=1, column=0, pady=(5, 10))
        self.name_entry.insert("1.0", "Usuario")  # Default text

        # Frame for the buttons
        btn_frame = ctk.CTkFrame(controls)
        btn_frame.grid(row=2, column=0, pady=5, sticky="ew")
        btn_frame.grid_columnconfigure((0,1,2), weight=1)

        # Button to choose text color
        self.color_button = ctk.CTkButton(btn_frame, text="Color de texto", command=self.elegir_color)
        self.color_button.grid(row=0, column=0, padx=5)

        # Square showing the selected color
        self.color_preview = ctk.CTkLabel(btn_frame, text="", width=30, height=30, fg_color=self.text_color)
        self.color_preview.grid(row=0, column=1, padx=5)

        # Button to save the generated image
        self.save_button = ctk.CTkButton(btn_frame, text="Guardar", command=self.guardar_imagen)
        self.save_button.grid(row=0, column=2, padx=5)
    
        # Update preview when the text is modified
        self.name_entry.bind("<<Modified>>", self._on_text_change)
    
        self.previsualizar()  # Initial preview

        # Footer with author and version
        footer = ctk.CTkLabel(self, text="Realizado por Carlos - Versión 1.0", font=("Arial", 12, "italic"))
        footer.grid(row=2, column=0, pady=(0, 10), sticky="s")
    
    def _on_text_change(self, event):
        # Update the preview live when the text is modified
        self.name_entry.edit_modified(False)  # Reset the modified flag
        self.previsualizar()

    def elegir_color(self):
        # Open the color picker and update the text color
        _, hex_color = colorchooser.askcolor(title="Selecciona un color")
        if hex_color:
            self.text_color = hex_color
            self.color_preview.configure(fg_color=hex_color)

    def generar_imagen_con_texto(self):
        # Generate a new image with the text over the logo
        raw_text = self.name_entry.get("1.0", "end").strip()
        if not raw_text:
            raw_text = "Nombre"

        imagen = self.original_image.copy()
        draw = ImageDraw.Draw(imagen)

        # Try to load a font, use default if it fails
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        max_width = imagen.width * 0.9  # Maximum allowed text width
        palabras = raw_text.split()
        lineas = []
        linea_actual = ""

        # Split the text into lines so it doesn't overflow the image
        for palabra in palabras:
            prueba = f"{linea_actual} {palabra}".strip()
            bbox = draw.textbbox((0, 0), prueba, font=font)
            ancho = bbox[2] - bbox[0]
            if ancho <= max_width:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        if linea_actual:
            lineas.append(linea_actual)

        # Calculate the total text height to center it vertically
        text_sizes = [draw.textbbox((0, 0), linea, font=font) for linea in lineas]
        text_heights = [bbox[3] - bbox[1] for bbox in text_sizes]
        interlineado = 10
        total_height = sum(text_heights) + interlineado * (len(lineas) - 1)
        y = (imagen.height - total_height) / 2

        # Draw each line of text (with white outline)
        for i, linea in enumerate(lineas):
            bbox = text_sizes[i]
            text_width = bbox[2] - bbox[0]
            x = (imagen.width - text_width) / 2
            # White outline
            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), linea, font=font, fill="white")
            # Main text
            draw.text((x, y), linea, fill=self.text_color, font=font)
            y += text_heights[i] + interlineado

        return imagen

    def previsualizar(self):
        # Update the displayed image with the current text
        imagen = self.generar_imagen_con_texto()
        preview = ImageTk.PhotoImage(imagen)
        self.image_label.configure(image=preview)
        self.image_label.image = preview

    def guardar_imagen(self):
        # Save the generated image to the desktop with the entered name
        nombre_archivo = "".join(
            c for c in (self.name_entry.get("1.0", "end").strip() or "nombre")
            if c.isalnum() or c in (" ","_","-")
        ).strip().replace(" ","_")
        imagen = self.generar_imagen_con_texto()
        escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"{nombre_archivo}_logo.png"
        output_path = os.path.join(escritorio, filename)
        imagen.save(output_path)
        messagebox.showinfo("Imagen guardada", f"Imagen guardada como:\n{output_path}")

if __name__ == "__main__":
    app = LogoApp()
    app.mainloop()