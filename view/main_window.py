import tkinter
import tkinter as tk
from tkinter import END
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import spacy
from spacy import displacy
from pathlib import Path
from PIL import ImageTk, Image as PIL_image
from io import BytesIO

class MainWindow:
    def __init__(self):
        self._window = tk.Tk()
        self._is_window_opened = False
        self._tree_frame = tkinter.Frame(self._window)
        self._dictionary_documentation_txt_edit = tk.Text(self._window)
        self._text_field = tkinter.Text(self._window)
        self._generate_button = tkinter.Button(self._window, text="Сформировать дерево", command=self.generate)
        self._left_frame_buttons = tk.Frame(self._window)
        self._dictionary_documentation_label = tk.Label(self._window, text="Документирование анализа текста")
        self._button_open = tk.Button(self._left_frame_buttons, text="Открыть файл", command=self.open_file)
        self._save_button = tk.Button(self._left_frame_buttons, text="Сохранить",
                                      command=self.save)

        self._button_help = tk.Button(self._left_frame_buttons, text="Помощь",
                                      command=self.about)

        self._hbar = tk.Scrollbar(self._tree_frame, orient=tk.HORIZONTAL)
        self._vbar = tk.Scrollbar(self._tree_frame, orient=tk.VERTICAL)

        self._imageCanvas = tk.Canvas(self._tree_frame, bg='white', width=300, height=300,
                                      scrollregion=(0, 0, 500, 500))
        self._configureScrollBars()

        self._imageCanvas.config(width=300, height=300)
        self._imageCanvas.config(xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)
        self._imageCanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._nlp = spacy.load("en_core_web_sm")

    def start(self):
        self._configure_window()
        self._window.mainloop()
        return

    def _generateTree(self, message):
        doc = self._nlp(message)
        svg = displacy.render(doc, style="dep", jupyter=False)
        drawing = svg2rlg(path=BytesIO(bytes(svg, 'ascii')))
        out = BytesIO()
        renderPM.drawToFile(drawing, out, fmt="PNG")
        img = PIL_image.open(out)
        pimg = ImageTk.PhotoImage(img)

        self._imageCanvas.config(scrollregion=(0, 0, img.size[0], img.size[1]))
        self._imageCanvas.create_image(0, 0, image=pimg, anchor="nw")
        return

    def _configureScrollBars(self):
        self._hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self._hbar.config(command=self._imageCanvas.xview)

        self._vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._vbar.config(command=self._imageCanvas.yview)

    def _configure_window(self):
        self._window.title("Синтаксический анализ текстов")

        self._left_frame_buttons.grid(row=0, column=0, rowspan=2, sticky="ns")
        self._button_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self._save_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self._button_help.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self._text_field.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        self._text_field.configure(height=2, border=3)
        self._generate_button.grid(row=0, column=2, sticky="ns", padx=5, pady=5)

        self._tree_frame.grid(row=1, column=1, rowspan=3, columnspan=4, sticky="nsew")

        self._dictionary_documentation_label.grid(row=2, column=0, ipady=5)
        self._dictionary_documentation_txt_edit.grid(row=3, column=0, sticky="e", ipady=5)
        self._dictionary_documentation_txt_edit.configure(width=25, borderwidth=10)

    def open_file(self):
        return

    def about(self):
        return

    def generate(self):
        self._generateTree(self._text_field.get("1.0", END))
        return

    def save(self):
        return
