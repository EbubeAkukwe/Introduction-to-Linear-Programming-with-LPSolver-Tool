import google.generativeai as genai
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def extract_json_from_text(lp_problem: str, api_key: str) -> dict :
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        data_extraction_prompt = """
        You are a data extraction assistant. 
        Your task is to convert a linear programming problem written in natural language into a structured JSON format. 

        The JSON should contain the following fields:
        - "objective_function": The objective function as a symbolic string (e.g., "3x1 + 5x2").
        - "objective_coefficients": A list of coefficients of the objective function in order (e.g., [3, 5]).
        - "optimization_type": Either "maximize" or "minimize".
        - "constraints": An array of objects where each object contains:
            - "expression": The constraint equation as a symbolic string (e.g., "2x1 + x2 ≤ 10").
            - "coefficients": A list of coefficients for the variables (e.g., [2, 1]).
            - "type": The type of inequality ("<=", ">=", "=").
            - "rhs": The right-hand side value (e.g., 10).
        - "variables": A list of variable names (e.g., ["x1", "x2"]).

        ### Example Input:
        "Maximize 3x1 + 5x2 subject to 2x1 + x2 ≤ 10, x1 + 3x2 ≤ 12, x1 ≥ 0, x2 ≥ 0."

        ### Example Output:
        {
        "objective_function": "3x1 + 5x2",
        "objective_coefficients": [3, 5],
        "optimization_type": "maximize",
        "constraints": [
            {
            "expression": "2x1 + x2 ≤ 10",
            "coefficients": [2, 1],
            "type": "<=",
            "rhs": 10
            },
            {
            "expression": "x1 + 3x2 ≤ 12",
            "coefficients": [1, 3],
            "type": "<=",
            "rhs": 12
            },
            {
            "expression": "x1 ≥ 0",
            "coefficients": [1, 0],
            "type": ">=",
            "rhs": 0
            },
            {
            "expression": "x2 ≥ 0",
            "coefficients": [0, 1],
            "type": ">=",
            "rhs": 0
            }
        ],
        "variables": ["x1", "x2"]
        }

        Now, convert the following problem into JSON:

        """

        nlp_problem_prompt = data_extraction_prompt + lp_problem

        response = model.generate_content(
            f"{lp_problem} \n Respond in strict JSON format only, no text or string or anything before of after the JSON. FORCE DATA TYPE = JSON"
        )
        gemini_response = response.text
        if gemini_response.startswith("```"):
            gemini_response = gemini_response.lstrip("```json").lstrip("```").strip()
        if gemini_response.endswith("```"):
            gemini_response = gemini_response[:-3].strip()

        return (gemini_response)
    except Exception as e:
        # Handle the error or return None
        print("Error calling Gemini API:", e)
        return "{}"  # return empty JSON string instead of None
        
