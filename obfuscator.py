import os
import hashlib
import zlib
import marshal
import subprocess
import ast as a
import pickle
import time
from tqdm import tqdm  # مكتبة شريط التقدم


class MultiLayerObfuscator:
    """
    أداة لتشويش كود Python باستخدام تقنيات متعددة: AST + Marshal + Zlib.
    """
    def __init__(self, layers=5000):
        self.layers = layers  # عدد الطبقات

    def obfuscate(self, code):
        """
        تشويش الكود باستخدام AST، Marshal و Zlib مع عدة طبقات.
        """
        print("🔍 الخطوة 1: تشويش الكود باستخدام AST...")
        obfuscated_code = self._obfuscate_with_ast(code)

        print(f"🔐 الخطوة 2: إضافة {self.layers} طبقة من Marshal و Zlib...")
        start_time = time.time()  # وقت بدء العملية
        final_code = self._obfuscate_with_multiple_layers(obfuscated_code)
        elapsed_time = time.time() - start_time  # الوقت المنقضي

        print(f"⏱️ الوقت المستغرق لإضافة {self.layers} طبقة: {elapsed_time:.2f} ثانية")
        return final_code

    def _obfuscate_with_ast(self, code):
        """
        تشويش الكود باستخدام AST.
        """
        obfuscated_code = "import pickle\nimport zlib\nimport marshal\n"
        pickled_objects = self._get_pickled_object_list(code)
        for i, obj in enumerate(pickled_objects):
            compressed = zlib.compress(obj, level=9)
            obfuscated_code += f"var_{i} = pickle.loads(zlib.decompress({repr(compressed)}))\n"

        # إضافة منطق التنفيذ
        obfuscated_code += "\nexec(compile(var_0, '<string>', 'exec'))\n"
        return obfuscated_code

    def _get_pickled_object_list(self, code):
        """
        معالجة الكود إلى كائنات pickle.
        """
        ast_tree = a.parse(code)
        pickled_objects = []
        for node in a.walk(ast_tree):
            if isinstance(node, a.AST):
                pickled_objects.append(pickle.dumps(node))
        return pickled_objects

    def _obfuscate_with_multiple_layers(self, code):
        """
        إضافة طبقات متعددة من Marshal و Zlib مع شريط تقدم.
        """
        for _ in tqdm(range(self.layers), desc="🔄 تشفير الطبقات", unit="طبقة"):
            code = self._obfuscate_with_marshal_zlib(code)
        return code

    def _obfuscate_with_marshal_zlib(self, code):
        """
        تشفير وضغط الكود باستخدام Marshal و Zlib.
        """
        compressed_code = zlib.compress(marshal.dumps(compile(code, '<string>', 'exec')))
        obfuscated_code = f"import marshal, zlib\nexec(marshal.loads(zlib.decompress({repr(compressed_code)})))"
        return obfuscated_code


def create_multi_layer_obfuscated_file(input_file, output_file, layers=5000):
    """
    إنشاء ملف Python جديد يحتوي على الكود المشفر والمضغوط.
    """
    try:
        # قراءة الكود الأصلي
        with open(input_file, "r") as f:
            code = f.read()

        # تشويش الكود باستخدام الطبقات المتعددة
        obfuscator = MultiLayerObfuscator(layers=layers)
        obfuscated_code = obfuscator.obfuscate(code)

        # كتابة الكود المشفر إلى ملف جديد
        with open(output_file, "w") as f:
            f.write(obfuscated_code)
        print(f"✅ تم إنشاء الكود المشفر في الملف: {output_file}")

        return output_file
    except Exception as e:
        print(f"❌ خطأ أثناء إنشاء الملف المشفر: {e}")
        raise


def main():
    print("أداة تشويش وحماية أكواد Python باستخدام تقنيات متعددة")
    print("===========================================================")

    # إدخال اسم الملف الأصلي
    input_file = input("أدخل ملف Python الأصلي لتشفيره (مثل script.py): ").strip()
    if not os.path.isfile(input_file):
        print(f"❌ خطأ: الملف {input_file} غير موجود.")
        return

    # إدخال اسم الملف النهائي
    output_file = input("أدخل اسم الملف النهائي لحفظ الكود المحمي (مثل output.py): ").strip()
    output_folder = os.path.dirname(output_file)
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # عدد الطبقات
        layers = int(input("أدخل عدد الطبقات (مثال: 5000): ").strip())

        print(f"⏳ بدء عملية التشفير مع {layers} طبقة...")
        # إنشاء ملف مشفر باستخدام الطبقات المتعددة
        create_multi_layer_obfuscated_file(input_file, output_file, layers=layers)

        print(f"\n✅ تم بنجاح! يمكنك تشغيل الكود المحمي من الملف: {output_file}")
    except Exception as e:
        print(f"❌ خطأ: {e}")


if __name__ == "__main__":
    main()
