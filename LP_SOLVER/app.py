from core_solver.nlp_parser import extract_json_from_text
from core_solver.lp_problem_parser import parse_json_from_json
from core_solver.lp_solver import solve_lp
from core_solver.explain_solution import explain_solution_from_json
from core_solver.json_to_colored_html import json_to_colored_html

from html import escape
import json


import time

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main HTML page for the user."""
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        lp_problem = request.form.get('problem_text')
        user_api_key = request.headers.get('X-Gemini-API-Key')
        
        if not lp_problem:
            return jsonify({"status": "error", "message": "No problem_text provided"}), 400

        start_time = time.perf_counter()
        response = extract_json_from_text(lp_problem, user_api_key)

        #print(response)

        if not response:
            return jsonify({"status": "error",
                            "message": "No response from model.",
                            "execution_time": 0})

        try:
            lp_json_data = json.loads(response)
        except json.JSONDecodeError as e:
            return jsonify({"status": "error",
                            "message": f"Invalid JSON from NLP parser: {e}",
                            "execution_time": 0})

        parsed_data_str = parse_json_from_json(lp_json_data, user_api_key)
        if not parsed_data_str:
            return jsonify({"status": "error",
                            "message": "Could not parse problem into LP format.",
                            "execution_time": 0})

        try:
            lp_data = json.loads(parsed_data_str)
            #print(lp_data)
        except json.JSONDecodeError as e:
            return jsonify({"status": "error",
                            "message": f"Parse step failed: {e}",
                            "execution_time": 0})

        solution = solve_lp(lp_data)
        explanation = explain_solution_from_json(lp_json_data, user_api_key)

        end_time = time.perf_counter()
        execution_time = f"{end_time - start_time:.4f} seconds"

        return jsonify({
            "status": "success",
            "parsed_data": json_to_colored_html(lp_data),
            "solution": json_to_colored_html(solution),
            "explained_solution": json_to_colored_html(explanation),
            "execution_time": json_to_colored_html(execution_time)
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
