from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def Hello():
    return render_template("index.html")

@app.route("/capture_image")
def capture_image():
    try:
        subprocess.run(['python', 'camera.py'])
        return jsonify({'message': 'Image captured successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)