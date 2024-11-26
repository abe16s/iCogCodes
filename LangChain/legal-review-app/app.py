from flask import Flask, request, render_template
from models.contract_analysis_model import analyze_document

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file:
        file_path = f"data/{file.filename}"
        file.save(file_path)

        analysis_report = analyze_document(file_path)

        return render_template('result.html', analysis=analysis_report)

if __name__ == '__main__':
    app.run(debug=True)
