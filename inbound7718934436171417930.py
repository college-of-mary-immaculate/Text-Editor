from tkinter import *
from tkinter import font, colorchooser
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno, showinfo
import os
import nltk
from nltk.corpus import words

nltk.download('words')

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Text Editor")
        
        self.toolbar = Frame(self.root)
        self.toolbar.pack(side=TOP, fill=X)
        
        self.text_area = Text(self.root, wrap='word', undo=True)
        self.text_area.pack(fill=BOTH, expand=True)

        self.scroll_bar = Scrollbar(self.text_area)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.scroll_bar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)

        self.setup_menu()
        self.setup_toolbar()

    def set_theme(self):
        theme = self.theme_choice.get()
        if theme == "light":
            self.text_area.config(bg="white", fg="black")
        elif theme == "dark":
            self.text_area.config(bg="black", fg="white")
        elif theme == "pink":
            self.text_area.config(bg="pink", fg="black")

    def setup_menu(self):
        menu_bar = Menu(self.root)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.theme_choice = StringVar()
        self.theme_choice.set("light")

        theme_menu = Menu(menu_bar, tearoff=0)
        theme_menu.add_radiobutton(label="Light", variable=self.theme_choice, value="light", command=self.set_theme)
        theme_menu.add_radiobutton(label="Dark", variable=self.theme_choice, value="dark", command=self.set_theme)
        theme_menu.add_radiobutton(label="Pink", variable=self.theme_choice, value="pink", command=self.set_theme)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)

        tools_menu = Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Spell Check", command=self.spell_check)
        tools_menu.add_command(label="Word Count", command=self.word_count)
        tools_menu.add_command(label="Find and Replace", command=self.find_replace)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        self.root.config(menu=menu_bar)

    def setup_toolbar(self):
        font_families = font.families()
        self.font_families_variable = StringVar()
        self.font_families_variable.set('Arial')
        fontfamily_combobox = Combobox(self.toolbar, width=15, values=font_families, state='readonly',
                                       textvariable=self.font_families_variable)
        fontfamily_combobox.grid(row=0, column=0)

        self.font_size_variable = IntVar()
        self.font_size_variable.set(12)
        font_size_combobox = Combobox(self.toolbar, width=3, values=list(range(1, 39)), state='readonly',
                                      textvariable=self.font_size_variable)
        font_size_combobox.grid(row=0, column=1)

        apply_button = Button(self.toolbar, text="Apply to Selected Text", command=self.apply_to_selected_text)
        apply_button.grid(row=0, column=2)

        bold_button = Button(self.toolbar, text="B", command=self.bold_text)
        bold_button.grid(row=0, column=3)

        underline_button = Button(self.toolbar, text="U", command=self.underline_text)
        underline_button.grid(row=0, column=4)
        
        color_button = Button(self.toolbar, text="Color", command=self.change_font_color)
        color_button.grid(row=0, column=5)
        
    def change_font_color(self):
        color = colorchooser.askcolor(title="Choose font color")[1]
        if color:
            self.apply_tag(foreground=color)   

    def apply_to_selected_text(self):
        font_style = self.font_families_variable.get()
        font_size = self.font_size_variable.get()
        self.apply_tag(font=(font_style, font_size))

    def apply_tag(self, **kwargs):
        selected_text = self.text_area.tag_ranges(SEL)
        if selected_text:
            tag_components = []
            if 'font' in kwargs:
                font_tuple = kwargs['font']
                tag_components.extend(font_tuple)
            if 'foreground' in kwargs:
                tag_components.append(kwargs['foreground'])
            tag_name = f"custom_{'_'.join(map(str, tag_components))}"
            self.text_area.tag_add(tag_name, selected_text[0], selected_text[1])
            self.text_area.tag_configure(tag_name, **kwargs)

    def bold_text(self):
        font_style = self.font_families_variable.get()
        font_size = self.font_size_variable.get()
        self.apply_tag(font=(font_style, font_size, 'bold'))

    def underline_text(self):
        font_style = self.font_families_variable.get()
        font_size = self.font_size_variable.get()
        self.apply_tag(font=(font_style, font_size, 'underline'))

    def new_file(self):
        self.text_area.delete(1.0, END)
        self.root.title("Untitled - Text Editor")

    def open_file(self):
        file_path = askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, END)
                self.text_area.insert(END, file.read())
                self.root.title(os.path.basename(file_path) + " - Text Editor")

    def save_file(self):
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                text_content = self.text_area.get("1.0", END)
                file.write(text_content)

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def exit_program(self):
        if askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            s1, s2 = s2, s1

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def spell_checker(self, input_word, word_list):
        threshold = 1
        corrections = []
        for word in word_list:
            distance = self.levenshtein_distance(input_word, word)
            if distance <= threshold:
                corrections.append((word, distance))
        corrections.sort(key=lambda x: x[1])
        return corrections

    def spell_check(self):
        if self.text_area.tag_ranges(SEL):
            start_index = self.text_area.index(SEL_FIRST)
            end_index = self.text_area.index(SEL_LAST)
            selected_text = self.text_area.get(start_index, end_index).strip()
            words_in_text = selected_text.split()
            misspelled_words = {}
            all_words = set(words.words())
            for word in words_in_text:
                if word.lower() not in all_words:
                    corrections = self.spell_checker(word.lower(), all_words)
                    if corrections:
                        misspelled_words[word] = [corr[0] for corr in corrections]
            self.display_misspelled_words(misspelled_words)
        else:
            showinfo("Spell Checker", "Please select text to spell check.")

    def display_misspelled_words(self, misspelled_words):
        if misspelled_words:
            message = "Misspelled Words:\n\n"
            for word, suggestions in misspelled_words.items():
                suggestion_text = ', '.join(suggestions)
                message += f"'{word}': {suggestion_text}\n"
            showinfo("Spell Checker", message)

    def word_count(self):
        text_content = self.text_area.get("1.0", END)
        word_list = text_content.split()
        word_count = len(word_list)
        showinfo("Word Count", f"Word Count: {word_count}")

    def find_replace(self):
        find_replace_window = Toplevel(self.root)
        find_replace_window.title("Find and Replace")

        Label(find_replace_window, text="Find:").grid(row=0, column=0, padx=4, pady=4)
        find_entry = Entry(find_replace_window)
        find_entry.grid(row=0, column=1, padx=4, pady=4)

        Label(find_replace_window, text="Replace:").grid(row=1, column=0, padx=4, pady=4)
        replace_entry = Entry(find_replace_window)
        replace_entry.grid(row=1, column=1, padx=4, pady=4)

        def find():
            self.text_area.tag_remove('found', '1.0', END)
            find_text = find_entry.get()
            if find_text:
                start_pos = '1.0'
                while True:
                    start_pos = self.text_area.search(find_text, start_pos, stopindex=END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(find_text)}c"
                    self.text_area.tag_add('found', start_pos, end_pos)
                    start_pos = end_pos
                self.text_area.tag_config('found', foreground='red', background='yellow')

        def replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text_area.get("1.0", END)
            new_content = content.replace(find_text, replace_text)
            self.text_area.delete("1.0", END)
            self.text_area.insert("1.0", new_content)

        Button(find_replace_window, text="Find", command=find).grid(row=2, column=0, padx=4, pady=4)
        Button(find_replace_window, text="Replace", command=replace).grid(row=2, column=1, padx=4, pady=4)

def main():
    root = Tk()
    editor = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
