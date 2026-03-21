import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# ضع مفتاحك هنا
# نسحب المفتاح من إعدادات السيرفر السريّة بدلاً من كتابته هنا
my_api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=my_api_key)

# استخدم الموديل الذي نجح معك في آخر تجربة
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'لم يتم رفع صورة'}), 400
    
    file = request.files['image']
    image = Image.open(file.stream)
    
    # البرومبت الجديد: صارم جداً ومباشر
  # البرومبت الجديد مع أمر التنسيق الرياضي
    prompt = """
    أنت مصحح رياضيات صارم ومباشر. قم بتحليل حل المسألة الرياضية في الصورة.
    - إذا كان الحل صحيحاً 100%، اكتب فقط: "✅ الحل صحيح تماماً."
    - إذا كان هناك خطأ، اكتب فقط: "❌ الحل خاطئ." ثم في سطر جديد اكتب "الخطأ في الخطوة:" واذكر الخطوة الخاطئة باختصار شديد .
    مهم جداً: يجب كتابة أي معادلة رياضية، أو أس، أو كسر باستخدام صيغة LaTeX الرياضية (مثلاً استخدم $x^2$ بدلاً من x^2، واستخدم $\frac{a}{b}$ للكسور).
    استخدم علامة $ للمعادلات المدمجة في النص، وعلامة $$ للمعادلات في سطر منفصل.
    ممنوع كتابة أي مقدمات، أو مجاملات، أو إعادة كتابة الخطوات الصحيحة.
    """
    
    try:
        response = model.generate_content([prompt, image])
        return jsonify({'analysis': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)