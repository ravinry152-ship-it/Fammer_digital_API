# import os
# import pdfplumber

# # ====== កំណត់ Path ======
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# pdf_folder = os.path.join(BASE_DIR, "pdfs")
# text_folder = os.path.join(BASE_DIR, "texts")
# os.makedirs(text_folder, exist_ok=True)


# def clean_khmer_text(text: str) -> str:
#     """សម្អាតអត្ថបទខ្មែរ លុបបន្ទាត់ទទេច្រើន និង space មិនចាំបាច់"""
#     if not text:
#         return ""
#     lines = text.splitlines()
#     cleaned = []
#     for line in lines:
#         line = line.strip()
#         if line:  # លុបបន្ទាត់ទទេទាំងស្រុង
#             cleaned.append(line)
#     return "\n".join(cleaned)


# def extract_pdf_to_text(pdf_path: str, txt_path: str) -> bool:
#     """
#     បំប្លែង PDF → Text ដោយប្រើ pdfplumber
#     Returns: True ប្រសិនបើជោគជ័យ
#     """
#     try:
#         full_text = ""
#         with pdfplumber.open(pdf_path) as pdf:
#             total_pages = len(pdf.pages)
#             print(f"   📄 ចំនួន Page: {total_pages}")

#             for i, page in enumerate(pdf.pages, 1):
#                 # ១. Extract text ធម្មតា
#                 text = page.extract_text(
#                     x_tolerance=3,       # ទំហំ tolerance ផ្នែក X (ជួយ spacing ខ្មែរ)
#                     y_tolerance=3,       # ទំហំ tolerance ផ្នែក Y
#                     layout=True,         # រក្សា layout ដើម
#                     x_density=7.25,      # ដង់ស៊ីតេ X សម្រាប់ detect columns
#                     y_density=13,        # ដង់ស៊ីតេ Y
#                 )

#                 if text:
#                     cleaned = clean_khmer_text(text)
#                     full_text += f"\n\n--- Page {i} ---\n{cleaned}"
#                 else:
#                     print(f"   ⚠️  Page {i}: គ្មានអត្ថបទ (អាចជា Image)")

#         if full_text.strip():
#             with open(txt_path, "w", encoding="utf-8") as f:
#                 f.write(full_text.strip())
#             return True
#         else:
#             print(f"   ❌ គ្មានអត្ថបទដែលអាច extract បានទេ!")
#             return False

#     except Exception as e:
#         print(f"   ❌ Error: {e}")
#         return False


# def convert_all_pdfs():
#     """បំប្លែង PDF ទាំងអស់ក្នុង /pdfs → /texts"""
#     pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

#     if not pdf_files:
#         print("❌ រកមិនឃើញ PDF ក្នុង /pdfs folder!")
#         return

#     print(f"🔄 ចាប់ផ្តើមបំប្លែង PDF {len(pdf_files)} ឯកសារ...\n")
#     success, failed = 0, 0

#     for pdf_file in pdf_files:
#         pdf_path = os.path.join(pdf_folder, pdf_file)
#         txt_name = pdf_file.replace(".pdf", ".txt")
#         txt_path = os.path.join(text_folder, txt_name)

#         print(f"📖 កំពុងបំប្លែង: {pdf_file}")

#         if extract_pdf_to_text(pdf_path, txt_path):
#             size = os.path.getsize(txt_path)
#             print(f"   ✅ រួចរាល់! → {txt_name} ({size:,} bytes)\n")
#             success += 1
#         else:
#             print(f"   ❌ បរាជ័យ: {pdf_file}\n")
#             failed += 1

#     print("=" * 50)
#     print(f"✅ ជោគជ័យ: {success} ឯកសារ")
#     print(f"❌ បរាជ័យ:  {failed} ឯកសារ")
#     print(f"📁 Text files ត្រូវបានរក្សាទុកក្នុង: {text_folder}")


# if __name__ == "__main__":
#     convert_all_pdfs()