import os
import hashlib
import zlib
import marshal
import subprocess
import ast as a
import pickle


class MultiLayerObfuscator:
    """
    أداة لتشويش كود Python باستخدام تقنيات متعددة: AST + Marshal + Zlib.
    """
    def __init__(self):
        pass

    def obfuscate(self, code):
        """
        تشويش الكود باستخدام AST، Marshal و Zlib.
        """
        print("🔍 الخطوة 1: تشويش الكود باستخدام AST...")
        obfuscated_code = self._obfuscate_with_ast(code)

        print("🔐 الخطوة 2: تشفير وضغط الكود باستخدام Marshal و Zlib...")
        final_code = self._obfuscate_with_marshal_zlib(obfuscated_code)

        return final_code

    def _obfuscate_with_ast(self, code):
        """
        تشويش الكود باستخدام AST.
        """
        obfuscated_code = "import pickle\nimport zlib\nimport marshal\n"
        pickled_objects = self._get_pickled_object_list(code)
        for i, obj in enumerate(pickled_objects):
            compressed = zlib.compress(obj, level=9)
            obfuscated_code += f"var_{i} = pickle.loads(zlib.decompress({compressed}))\n"

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

    def _obfuscate_with_marshal_zlib(self, code):
        """
        تشفير وضغط الكود باستخدام Marshal و Zlib.
        """
        compressed_code = zlib.compress(marshal.dumps(compile(code, '<string>', 'exec')))
        obfuscated_code = f"import marshal, zlib\nexec(marshal.loads(zlib.decompress({compressed_code})))"
        return obfuscated_code


def compile_with_pyarmor(input_file, output_file):
    """
    استخدام PyArmor لحماية كود Python.
    """
    try:
        print("🔒 حماية الكود باستخدام PyArmor...")
        command = [
            "pyarmor",
            "pack",
            "-e",
            "--clean",
            "-x", " --disable-restrict-mode",
            input_file,
            "-o", os.path.dirname(output_file)
        ]
        subprocess.run(command, check=True)
        print(f"✅ تم حماية الكود بنجاح بواسطة PyArmor. الملف المحمي موجود في: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ أثناء حماية الكود باستخدام PyArmor: {e}")
        raise


def create_multi_layer_obfuscated_file(input_file, output_file):
    """
    إنشاء ملف Python جديد يحتوي على الكود المشفر والمضغوط.
    """
    try:
        # قراءة الكود الأصلي
        with open(input_file, "r") as f:
            code = f.read()

        # تشويش الكود باستخدام الطبقات المتعددة
        obfuscator = MultiLayerObfuscator()
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
        # الخطوة 1: إنشاء ملف مشفر باستخدام الطبقات المتعددة
        obfuscated_file = create_multi_layer_obfuscated_file(input_file, output_file)

        # الخطوة 2: حماية الكود باستخدام PyArmor (اختياري)
        if input("هل تريد حماية إضافية باستخدام PyArmor؟ (y/n): ").strip().lower() == "y":
            compile_with_pyarmor(obfuscated_file, output_file)

        print(f"\n✅ تم بنجاح! يمكنك تشغيل الكود المحمي من الملف: {output_file}")
    except Exception as e:
        print(f"❌ خطأ: {e}")


if __name__ == "__main__":
    main()
