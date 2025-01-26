from flask import Flask, jsonify

app = Flask(__name__)
data = {
    "Chicken": 76,
    "Computer Science (Major)": 11,
    "Computer Science (Special)": 37,
    "Fish": 6,
    "Information Technology (Major)": 26,
    "Information Technology (Special)": 18,
    "Vegetable": 10
}

@app.route('/', methods=['GET'])
def home():
    return jsonify(data)
@app.route('/stats', methods=['GET'])
def stats():
    meal_preferences = {key: value for key, value in data.items() if key in ["Chicken", "Fish", "Vegetable"]}
    program_counts = {key: value for key, value in data.items() if key not in ["Chicken", "Fish", "Vegetable"]}

    result = {
        "meal_preferences": meal_preferences,
        "program_counts": program_counts
    }
    return jsonify(result)
@app.route('/add/<int:a>/<int:b>', methods=['GET'])
def add(a, b):
    return jsonify({"operation": "add", "a": a, "b": b, "result": a + b})

@app.route('/subtract/<int:a>/<int:b>', methods=['GET'])
def subtract(a, b):
    return jsonify({"operation": "subtract", "a": a, "b": b, "result": a - b})

@app.route('/multiply/<int:a>/<int:b>', methods=['GET'])
def multiply(a, b):
    return jsonify({"operation": "multiply", "a": a, "b": b, "result": a * b})

@app.route('/divide/<int:a>/<int:b>', methods=['GET'])
def divide(a, b):
    if b == 0:
        return jsonify({"error": "Division by zero is not allowed"}), 400
    return jsonify({"operation": "divide", "a": a, "b": b, "result": a / b})
if __name__ == '__main__':
    app.run(debug=True)










