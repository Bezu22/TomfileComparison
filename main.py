import os
import json
import xml.etree.ElementTree as ET
import customtkinter as ctk
from tkinter import messagebox

class AncaComparator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.load_config()
        self.title("ANCA .TOM Comparator")
        self.geometry("1200x800")

        # Zmienne do przechowywania wybranych ścieżek
        self.selected_left = None
        self.selected_right = None

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- GÓRNY PANEL: WYSZUKIWARKA ---
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_lists)
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Filtruj pliki...", textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # --- LEWY PANEL ---
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.left_frame, text="Symulator (Baza)", font=("Arial", 12, "bold")).pack(pady=5)
        
        # ZAMIANA: ScrollableFrame zamiast Listbox
        self.left_list_frame = ctk.CTkScrollableFrame(self.left_frame)
        self.left_list_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # --- PRAWY PANEL ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.right_frame, text="Maszyna (Wykonane)", font=("Arial", 12, "bold")).pack(pady=5)
        
        # ZAMIANA: ScrollableFrame zamiast Listbox
        self.right_list_frame = ctk.CTkScrollableFrame(self.right_frame)
        self.right_list_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # --- DOLNY PANEL ---
        self.compare_btn = ctk.CTkButton(self, text="PORÓWNAJ WYBRANE", command=self.compare_action, fg_color="#2ecc71", hover_color="#27ae60")
        self.compare_btn.grid(row=2, column=0, columnspan=2, pady=20)

        self.refresh_file_lists()

    def load_config(self):
        # Załóżmy domyślne ścieżki jeśli plik nie istnieje
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "path_left": "C:/symulator", 
                "path_right": "C:/wykonane", 
                "ignored_tags": ["modeRegrind318", "v_wheel_speed_rpm", "Image"]
            }

    def get_files_recursive(self, root_path):
        files_found = []
        if not os.path.exists(root_path):
            return []
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith(".tom"):
                    files_found.append(os.path.relpath(os.path.join(root, file), root_path))
        return files_found

    def update_lists(self, *args):
        search_term = self.search_var.get().lower()
        
        # Czyścimy listy przed ponownym załadowaniem
        for widget in self.left_list_frame.winfo_children():
            widget.destroy()
        for widget in self.right_list_frame.winfo_children():
            widget.destroy()

        # Budujemy lewą listę
        for f in self.all_left_files:
            if search_term in f.lower():
                btn = ctk.CTkButton(self.left_list_frame, text=f, anchor="w", fg_color="transparent", text_color="white",
                                   command=lambda path=f: self.select_file(path, "left"))
                btn.pack(fill="x", pady=1)

        # Budujemy prawą listę
        for f in self.all_right_files:
            if search_term in f.lower():
                btn = ctk.CTkButton(self.right_list_frame, text=f, anchor="w", fg_color="transparent", text_color="white",
                                   command=lambda path=f: self.select_file(path, "right"))
                btn.pack(fill="x", pady=1)

    def select_file(self, path, side):
        if side == "left":
            self.selected_left = path
            # Wizualne potwierdzenie wyboru (opcjonalne)
            print(f"Wybrano lewy: {path}")
        else:
            self.selected_right = path
            print(f"Wybrano prawy: {path}")

    def refresh_file_lists(self):
        self.all_left_files = self.get_files_recursive(self.config['path_left'])
        self.all_right_files = self.get_files_recursive(self.config['path_right'])
        self.update_lists()

    # ... tutaj reszta metod (parse_tom, compare_action, show_results) z poprzedniej wiadomości ...
    
    def compare_action(self):
        if not self.selected_left or not self.selected_right:
            messagebox.showwarning("Błąd", "Wybierz plik z lewej i prawej strony!")
            return
        # Reszta logiki porównania jak wcześniej
        print(f"Porównuję {self.selected_left} z {self.selected_right}")

if __name__ == "__main__":
    app = AncaComparator()
    app.mainloop()