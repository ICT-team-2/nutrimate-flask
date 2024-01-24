from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Serve your HTML file
@app.route('/')
def index():
    return render_template('your_html_file.html')

# Serve the Teachable Machine model and metadata
@app.route('/get_model')
def get_model():
    return send_from_directory('path_to_your_model_directory', 'model.json')

@app.route('/get_metadata')
def get_metadata():
    return send_from_directory('path_to_your_model_directory', 'metadata.json')

if __name__ == '__main__':
    app.run(debug=True)