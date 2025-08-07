# Logo Generator with Custom Text

A Python desktop application that takes a base logo (`logo.png`) and lets you add any custom text on top of it. Customize the text color, see a live preview, and save your personalized logo image directly to your Desktop.

## Features

- **Live Preview**: See your text update in real time as you type.  
- **Color Picker**: Choose any text color via a standard color‑chooser dialog.  
- **Automatic Wrapping**: Text automatically wraps to fit within the logo width.  
- **White Outline**: Ensures text remains legible over any background.  
- **Save to Desktop**: Saves the final image as `YourText_logo.png` on your Desktop.  
- **Dark Mode UI**: Built with CustomTkinter in a sleek dark‑blue theme.

## Prerequisites

- Python 3.7+  
- [Pillow](https://pypi.org/project/Pillow/)  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter/)  
- (Optional) `arial.ttf` on your system for a custom font; otherwise falls back to default.

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/cansi22/logo-generator.git
   cd logo-generator
   ```

2. **Create a virtual environment (recommended)**  
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your base logo**  
   Place your `logo.png` file in the project root (next to `generador_logo.py`).

## Usage

```bash
python generador_logo.py
```

1. Enter your desired text in the text box.  
2. Click **Color de texto** to choose a text color.  
3. Watch the live preview update automatically.  
4. Click **Guardar** to save the final image to your Desktop.

## File Structure

```
logo-generator/
├── generador_logo.py  # Main application script
├── logo.png           # Base logo image (replace with your own)
├── requirements.txt   # Python dependencies
├── LICENSE            # MIT License text
└── README.md          # This file
```

## Customization

- **Default Text Color**: Edit `self.text_color = "#273474"` in `generador_logo.py`.  
- **Font & Size**: Modify the `ImageFont.truetype("arial.ttf", 40)` call in `generar_imagen_con_texto()`.

## Packaging as Executable

To distribute without requiring Python installed on the user’s machine:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "logo.png;." generador_logo.py
```

The standalone executable will be in the `dist/` folder.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Author

Cansi – Version 1.0  

Feel free to open issues or submit pull requests!
