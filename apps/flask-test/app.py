from flask import Flask, render_template

app = Flask(__name__)

# Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
