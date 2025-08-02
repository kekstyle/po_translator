import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import polib
import os
import gettext
from deep_translator import GoogleTranslator
import re
import random

# 🔧 Fonctions utilitaires
def segment_text(text):
    pattern = r'(<[^>]+>)|(%\d*\$?\w)|(\b[FYmjdDHis]+\b)|(\b[Ymd]+\b)'
    return [seg for seg in re.split(pattern, text) if seg]

def fix_html_entities(text):
    return re.sub(r'&\s?#\s?(\d+);', r'&#\1;', text)

def fix_spacing(text):
    text = re.sub(r'(?<!\s)(%(\d+\$)?[a-zA-Z])', r' \1', text)
    return re.sub(r'(</[^>]+>)(?=\w)', r'\1 ', text)

def sanitize_translated_html(text):
    return fix_html_entities(fix_spacing(text))

def translate_segmented_text(segments, source, target):
    translated = []
    for seg in segments:
        if re.match(r'(<[^>]+>)|(%\d*\$?\w)|(\b[FYmjdDHis]+\b)|(\b[Ymd]+\b)', seg):
            translated.append(seg)
        else:
            try:
                t = GoogleTranslator(source=source, target=target).translate(seg)
                translated.append(t if t else seg)
            except:
                translated.append(seg)
    return sanitize_translated_html(''.join(translated))

def generate_alternative(text, source="en", target="fr"):
    segs = segment_text(text)
    base = translate_segmented_text(segs, source, target)
    variations = [
        base,
        base.replace("Vous", "Tu"),
        base.replace("Veuillez", "Merci de"),
        base + " !",
        base.replace("Appuyez", "Cliquez"),
    ]
    return random.choice(variations)

# 🧩 Module éditeur .mo
def module_edit_mo():
    def load_mo():
        file = filedialog.askopenfilename(filetypes=[("MO files", "*.mo")])
        if file:
            try:
                with open(file, 'rb') as mo_file:
                    trans = gettext.GNUTranslations(mo_file)
                table.delete(*table.get_children())
                for msgid, msgstr in trans._catalog.items():
                    if msgid:
                        table.insert("", "end", values=(msgid, msgstr))
            except Exception as e:
                messagebox.showerror("Erreur", f"Lecture échouée : {e}")

    def show_edit_popup(msgid, msgstr, row_id):
        edit_win = tk.Toplevel(window)
        edit_win.title("Édition msgstr")
        tk.Message(edit_win, text=msgid, width=400).pack()
        new_val = tk.StringVar(value=msgstr)
        entry = tk.Entry(edit_win, textvariable=new_val, width=60)
        entry.pack(); entry.focus()

        def auto_fill():
            segs = segment_text(msgid)
            translation = translate_segmented_text(segs, "en", "fr")
            new_val.set(translation)

        tk.Button(edit_win, text="Traduire automatiquement", command=auto_fill).pack(pady=5)

        def save():
            table.item(row_id, values=(msgid, new_val.get()))
            edit_win.destroy()

        tk.Button(edit_win, text="Sauvegarder", command=save).pack()
        edit_win.bind('<Return>', lambda e: save())

    def auto_translate_line(msgid, row_id):
        segs = segment_text(msgid)
        translation = translate_segmented_text(segs, "en", "fr")
        table.item(row_id, values=(msgid, translation))

    def generate_alternative(text):
        segs = segment_text(text)
        base = translate_segmented_text(segs, "en", "fr")
        variations = [
            base,
            base.replace("Vous", "Tu"),
            base.replace("Veuillez", "Merci de"),
            base + " !",
            base.replace("Appuyez", "Cliquez"),
        ]
        return random.choice(variations)

    def on_select(event):
        selected = table.focus()
        if not selected: return
        msgid, msgstr = table.item(selected, "values")
        for widget in action_panel.winfo_children(): widget.destroy()

        tk.Label(action_panel, text="Actions :", font=("Segoe UI", 10, "bold")).pack(pady=5)
        tk.Button(action_panel, text="✏️ Éditer", width=25, command=lambda: show_edit_popup(msgid, msgstr, selected)).pack(pady=5)
        tk.Button(action_panel, text="⚡ Traduire automatiquement", width=25, command=lambda: auto_translate_line(msgid, selected)).pack(pady=5)

        alt = generate_alternative(msgid)
        tk.Label(action_panel, text="💡 Suggestion alternative :", font=("Segoe UI", 10, "bold")).pack(pady=(15,5))
        tk.Message(action_panel, text=alt, width=200, font=("Segoe UI", 9)).pack()

    def save_po():
        save_path = filedialog.asksaveasfilename(defaultextension=".po", filetypes=[("PO files", "*.po")])
        if save_path:
            po = polib.POFile()
            for row in table.get_children():
                msgid, msgstr = table.item(row, "values")
                po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))
            po.save(save_path)
            messagebox.showinfo("Sauvegardé", f".po généré :\n{save_path}")

    window = tk.Toplevel(root)
    window.title("Éditeur .MO")
    window.geometry("1000x600")

    tk.Button(window, text="📂 Charger fichier .mo", command=load_mo).pack(pady=5)

    content_frame = tk.Frame(window)
    content_frame.pack(fill=tk.BOTH, expand=True)

    table = ttk.Treeview(content_frame, columns=("msgid", "msgstr"), show="headings")
    table.heading("msgid", text="msgid")
    table.heading("msgstr", text="msgstr")
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
    table.bind("<<TreeviewSelect>>", on_select)

    action_panel = tk.Frame(content_frame, width=250)
    action_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

    tk.Button(window, text="💾 Sauvegarder en .po", command=save_po).pack(pady=5)


# 🧩 Module traduction .po
def module_translate_po():
    def browse_po(): file_path.set(filedialog.askopenfilename(filetypes=[("PO files", "*.po")]))
    def run_translation():
        path = file_path.get()
        source = source_lang.get()
        target = target_lang.get()
        if not os.path.exists(path): return messagebox.showerror("Erreur", "Fichier introuvable.")
        log.delete(1.0, tk.END); progress.set(0)
        po = polib.pofile(path)
        total = len(po.untranslated_entries())
        for idx, entry in enumerate(po.untranslated_entries()):
            segs = segment_text(entry.msgid)
            entry.msgstr = translate_segmented_text(segs, source, target)
            progress.set(int((idx+1)/total*100)); progress_bar.update()
            log.insert(tk.END, f"{entry.msgid} → {entry.msgstr}\n"); log.see(tk.END)
        out_file = path.replace(".po", f"_{target}.po")
        po.save(out_file)
        messagebox.showinfo("Terminé", f"Fichier traduit : {out_file}")

    window = tk.Toplevel(root)
    window.title("Traduction .PO")
    file_path, source_lang, target_lang = tk.StringVar(), tk.StringVar(value="en"), tk.StringVar(value="fr")
    progress = tk.IntVar()

    tk.Label(window, text="Fichier .po :").pack()
    tk.Entry(window, textvariable=file_path, width=50).pack()
    tk.Button(window, text="Parcourir...", command=browse_po).pack()

    tk.Label(window, text="Langue source :").pack()
    tk.Entry(window, textvariable=source_lang).pack()
    tk.Label(window, text="Langue cible :").pack()
    tk.Entry(window, textvariable=target_lang).pack()
    tk.Button(window, text="Traduire", command=run_translation).pack(pady=5)

    progress_bar = ttk.Progressbar(window, variable=progress, length=400)
    progress_bar.pack(pady=5)

    log = tk.Text(window, height=10, width=70)
    log.pack(pady=5)

# 🧩 Compilation .po → .mo
def module_compile_po():
    file = filedialog.askopenfilename(filetypes=[("PO files", "*.po")])
    if file:
        try:
            po = polib.pofile(file)
            mo_file = file.replace(".po", ".mo")
            po.save_as_mofile(mo_file)
            messagebox.showinfo("Compilé", f".mo généré : {mo_file}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec : {e}")

# 🏠 Interface principale
root = tk.Tk()
root.title("Traducteur .PO - Menu principal")
root.geometry("500x300")

tk.Label(root, text="Bienvenue sur Po Translator ! Que souhaites-tu faire ?", font=("Segoe UI", 12, "bold")).pack(pady=20)

tk.Button(root, text="📤 Traduire un fichier .po", command=module_translate_po, width=40).pack(pady=5)
tk.Button(root, text="🧾 Ouvrir et éditer un fichier .mo", command=module_edit_mo, width=40).pack(pady=5)
tk.Button(root, text="🛠 Compiler un fichier .po en .mo", command=module_compile_po, width=40).pack(pady=5)

root.mainloop()
