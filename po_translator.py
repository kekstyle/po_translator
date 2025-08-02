import os
import re
import polib
from deep_translator import GoogleTranslator, MyMemoryTranslator

def segment_text(text):
    # Séparer les balises HTML, placeholders, formats de date
    pattern = r'(<[^>]+>)|(%\d*\$?\w)|(\b[FYmjdDHis]+\b)|(\b[Ymd]+\b)'
    segments = re.split(pattern, text)
    return [seg for seg in segments if seg is not None and seg != '']

def fix_spacing(text):
    # Ajoute un espace avant les placeholders s'ils sont collés au mot précédent
    return re.sub(r'(?<!\s)(%(\d+\$)?[a-zA-Z])', r' \1', text)

def translate_segmented_text(segments, source, target):
    translated_segments = []
    for seg in segments:
        if re.match(r'(<[^>]+>)|(%\d*\$?\w)|(\b[FYmjdDHis]+\b)|(\b[Ymd]+\b)', seg):
            translated_segments.append(seg)
        else:
            try:
                translated = GoogleTranslator(source=source, target=target).translate(seg)
                translated_segments.append(translated if translated else seg)
            except Exception as e:
                print(f"\n❌ Google a échoué sur : '{seg}' → {e}")
                choice = input("⏳ Essayer MyMemory ? (o/n) ").strip().lower()
                if choice == "o":
                    try:
                        translated = MyMemoryTranslator(source=source, target=target).translate(seg)
                        translated_segments.append(translated if translated else seg)
                    except Exception as e2:
                        print(f"💥 MyMemory a aussi échoué sur : '{seg}' → {e2}")
                        translated_segments.append(seg)
                else:
                    translated_segments.append(seg)
    combined = ''.join(seg if isinstance(seg, str) else '' for seg in translated_segments)
    return fix_spacing(combined)

# === 🚀 Traitement du fichier .po
po_file_path = "default.po"
source_lang = "en"
target_lang = "fr"

print("🔍 Chargement du fichier PO...")

if not os.path.exists(po_file_path):
    print(f"❌ Fichier introuvable : {po_file_path}")
    exit(1)
else:
    print(f"✅ Fichier trouvé : {po_file_path}")

try:
    po = polib.pofile(po_file_path)
    print(f"📄 {len(po)} entrées chargées")
except Exception as e:
    print(f"❌ Erreur lors de la lecture du fichier : {e}")
    exit(1)

entries = po.untranslated_entries()
print(f"✏️ {len(entries)} entrées non traduites détectées")

for entry in entries:
    print(f"\n⏳ Traduction de : {entry.msgid}")
    segments = segment_text(entry.msgid)
    translation = translate_segmented_text(segments, source_lang, target_lang)
    entry.msgstr = translation
    print(f"✅ {entry.msgid} → {translation}")

output_file = f"default_{target_lang}.po"
po.save(output_file)
print(f"\n🎉 Traduction terminée. Fichier enregistré sous : {output_file}")
