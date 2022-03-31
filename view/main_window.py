import tkinter
import tkinter as tk
from tkinter import END
#https://github.com/emilmont/pyStatParser
from stat_parser import Parser

import nltk
from nltk import Tree
from nltk.corpus import treebank
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame


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
        self._canvas_frame = CanvasFrame(self._tree_frame)
        self._tree = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP pretty)))')
        self._tree_widget = TreeWidget(self._canvas_frame.canvas(), self._tree)

        self._parser = Parser()

    def start(self):
        self._configure_window()
        self._window.mainloop()

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

        self._tree_frame.configure(background='black')

        self._canvas_frame.pack(fill=tk.BOTH, expand=1)
        self._canvas_frame.add_widget(self._tree_widget, 10, 10)  # (10,10) offsets

    def open_file(self):
        return

    def about(self):
        return

    def generate(self):
        tokens = nltk.word_tokenize(self._text_field.get("1.0", END))
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)
        nltk.corpus.brown.tagged_words()
        self._tree_widget.canvas().delete("all")
        self._tree = Tree.fromstring(self._parser.parse(self._text_field.get("1.0", END)))
        self._tree_widget = TreeWidget(self._canvas_frame.canvas(), self._tree)
        self._canvas_frame.add_widget(self._tree_widget)  # (10,10) offsets

        return

    def save(self):
        return
