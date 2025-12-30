import google.generativeai as genai
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def explain_solution_from_json(lp_json: dict, api_key: str) -> str :
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    try:
        prompt = """
        You are an expert in linear programming and operations research.
        Your task is to take a JSON object describing an optimization problem and explain the solution in plain English.

        Instructions

        Summarize the objective (maximize/minimize, and what function is being optimized).

        State the optimal decision variable values (e.g., how many units of each product to produce).

        State the optimal objective value (e.g., maximum profit).

        Explain the binding constraints (resources that are fully used at the solution).

        Mention any slack/unused resources (remaining capacity).

        Keep the explanation clear, concise, and non-technical, suitable for business users.

        Output format

        Produce a short, well-structured paragraph explanation.

        Now Explain this JSON:
        """

        explain_prompt = prompt + str(lp_json)

        response = model.generate_content(
            f"{explain_prompt} \n Respond in strict string or text format only, no JSON or anything before of after the text."
        )
        gemini_response = response.text
        return (gemini_response)
    except Exception as e:
        # Handle the error or return None
        print("Error calling Gemini API:", e)
        return "{}"  # return empty JSON string instead of None
        
