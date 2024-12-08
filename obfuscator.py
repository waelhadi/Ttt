import os
import base64
import zlib
import marshal
import tempfile
import subprocess
import ast as a
import pickle


class MultiLayerObfuscator:
    def __init__(self, layers=500):
        self.layers = layers  # عدد طبقات التشفير

    def obfuscate(self, code):
        """
        تشويش الكود باستخدام AST، Marshal، Zlib و Pickle.
        """
        print("🔍 الخطوة 1: تشويش الكود باستخدام AST...")
        obfuscated_code = self._obfuscate_with_ast(code)

        print(f"🔐 الخطوة 2: إضافة {self.layers} طبقة تشفير باستخدام Pickle...")
        obfuscated_code = self._add_multiple_pickle_layers(obfuscated_code)

        print("🔄 الخطوة 3: إضافة ملف مؤقت للتنفيذ...")
        wrapped_code = self._wrap_with_temp_file_execution(obfuscated_code)

        return wrapped_code

    def _obfuscate_with_ast(self, code):
        obfuscated_code = "import pickle\nimport zlib\nimport marshal\n"
        pickled_objects = self._get_pickled_object_list(code)
        for i, obj in enumerate(pickled_objects):
            compressed = zlib.compress(obj, level=9)
            encoded = base64.b64encode(compressed).decode('utf-8')
            obfuscated_code += f"var_{i} = pickle.loads(zlib.decompress(base64.b64decode('{encoded}')))\n"
        obfuscated_code += "\nexec(compile(var_0, '<string>', 'exec'))\n"
        return obfuscated_code

    def _get_pickled_object_list(self, code):
        ast_tree = a.parse(code)
        pickled_objects = []
        for node in a.walk(ast_tree):
            if isinstance(node, a.AST):
                pickled_objects.append(pickle.dumps(node))
        return pickled_objects

    def _add_multiple_pickle_layers(self, code):
        """
        تطبيق 500 طبقة تشفير باستخدام Pickle.
        """
        print("📦 إنشاء الطبقات...")
        encoded_code = code
        for i in range(self.layers):
            pickled_code = pickle.dumps(encoded_code)
            encoded_code = base64.b64encode(pickled_code).decode('utf-8')
            print(f"🔒 الطبقة {i + 1} تمت بنجاح.")
        
        # إعادة فك الطبقات للوصول إلى الكود الأصلي
        obfuscated_code = f"""
import base64
import pickle

encoded_code = '{encoded_code}'
for _ in range({self.layers}):
    encoded_code = pickle.loads(base64.b64decode(encoded_code))

exec(encoded_code)
"""
        return obfuscated_code

    def _wrap_with_temp_file_execution(self, obfuscated_code):
        wrapped_code = f"""
import os
import tempfile
import subprocess

with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as temp_file:
    temp_file.write(\"\"\"{obfuscated_code}\"\"\")
    temp_file_path = temp_file.name

try:
    subprocess.run(["python", temp_file_path], check=True)
finally:
    os.remove(temp_file_path)
"""
        return wrapped_code


def create_multi_layer_obfuscated_file(input_file, output_file, layers=500):
    try:
        with open(input_file, "r") as f:
            code = f.read()

        obfuscator = MultiLayerObfuscator(layers)
        obfuscated_code = obfuscator.obfuscate(code)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(obfuscated_code)
        print(f"✅ تم إنشاء الكود المشفر في الملف: {output_file}")

        return output_file
    except Exception as e:
        print(f"❌ خطأ أثناء إنشاء الملف المشفر: {e}")
        raise


def main():
    print("أداة تشويش وحماية أكواد Python باستخدام تقنيات متعددة")
    print("===========================================================")

    input_file = input("أدخل ملف Python الأصلي لتشفيره (مثل script.py): ").strip()
    if not os.path.isfile(input_file):
        print(f"❌ خطأ: الملف {input_file} غير موجود.")
        return

    output_file = input("أدخل اسم الملف النهائي لحفظ الكود المحمي (مثل output.py): ").strip()
    output_folder = os.path.dirname(output_file)
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    layers = int(input("أدخل عدد طبقات التشفير المطلوبة (مثل 500): ").strip())
    try:
        create_multi_layer_obfuscated_file(input_file, output_file, layers)
        print(f"\n✅ تم بنجاح! يمكنك تشغيل الكود المحمي من الملف: {output_file}")
    except Exception as e:
        print(f"❌ خطأ: {e}")


if __name__ == "__main__":
    main()
