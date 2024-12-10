import os

def remove_comments():
    # طلب اسم الملف الذي يحتوي على الكود مع التعليقات
    input_file_name = input("أدخل اسم الملف الذي يحتوي على التعليقات (مع الامتداد .py): ").strip()
    if not input_file_name.endswith(".py"):
        print("يجب أن يكون الملف بامتداد .py")
        return

    # طلب اسم الملف لحفظ الكود بعد حذف التعليقات
    output_file_name = input("أدخل اسم الملف لحفظ التعديلات (مع الامتداد .py): ").strip()
    if not output_file_name.endswith(".py"):
        print("يجب أن يكون الملف بامتداد .py")
        return

    try:
        # قراءة محتوى الملف الأصلي
        with open(input_file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # إزالة جميع التعليقات التي تبدأ بـ "#"
        modified_lines = [line for line in lines if not line.strip().startswith("#")]

        # كتابة الكود المعدل إلى الملف الجديد
        with open(output_file_name, "w", encoding="utf-8") as output_file:
            output_file.writelines(modified_lines)

        print(f"تم حفظ الكود المعدل في الملف '{output_file_name}' بنجاح بدون التعليقات.")
    except FileNotFoundError:
        print(f"الملف '{input_file_name}' غير موجود. تأكد من صحة اسم الملف وحاول مرة أخرى.")
    except IOError as e:
        print(f"حدث خطأ أثناء التعامل مع الملف: {e}")

# استدعاء الدالة
remove_comments()
