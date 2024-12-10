import lzma
import os
import sys

def compress_and_embed_execution(input_file, output_file):
    """
    تضغط ملف باستخدام lzma وتضيف شفرة لفك الضغط التلقائي عند تشغيل الملف.
    """
    try:
        # قراءة البيانات الأصلية من الملف
        with open(input_file, 'rb') as f_in:
            original_data = f_in.read()

        # ضغط البيانات باستخدام lzma
        compressed_data = lzma.compress(original_data)

        # إنشاء السكربت الذاتي التشغيل
        executable_code = f"""
import lzma, os, sys
compressed_data = {repr(compressed_data)}

# فك ضغط البيانات
decompressed_data = lzma.decompress(compressed_data)

# حفظ الملف المؤقت
temp_file = "temp_extracted_file.py"
with open(temp_file, "wb") as f_out:
    f_out.write(decompressed_data)

# تنفيذ الملف
os.system(f'python {{temp_file}}')

# حذف الملف المؤقت
os.remove(temp_file)
"""

        # كتابة السكربت المضغوط
        with open(output_file, 'w') as f_out:
            f_out.write(executable_code)

        print(f"تم ضغط الملف وحفظه كأداة تنفيذية في: {output_file}")
    except Exception as e:
        print(f"حدث خطأ أثناء عملية الضغط: {e}")


if __name__ == "__main__":
    print("اختر العملية التي ترغب في تنفيذها:")
    print("1. ضغط ملف وتحويله إلى أداة ذاتية التشغيل")
    choice = input("أدخل رقم العملية: ").strip()

    if choice == "1":
        input_file = input("أدخل اسم الملف الذي ترغب في ضغطه (مع الامتداد): ").strip()
        output_file = input("أدخل اسم الملف المضغوط الناتج (مع الامتداد): ").strip()
        compress_and_embed_execution(input_file, output_file)
    else:
        print("خيار غير صحيح! يرجى اختيار 1.")
