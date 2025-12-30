import google.generativeai as genai
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def parse_json_from_json(lp_json: dict, api_key: str) -> dict :
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    try:
        data_extraction_json = """
        You are an expert in linear programming (LP) and operations research.
        Your task is to parse a JSON description of an optimization problem into a canonical LP representation.

        Instructions

        Always return valid JSON (strict format, no explanations).

        Extract:

        "objective_coefficients": coefficients in the objective function, in the order the variables appear.

        "constraint_matrix": each constraint’s left-hand-side (LHS) coefficients in the same variable order.

        "constraint_rhs": constants on the right-hand side (RHS).

        "optimization_type": directly from "objective.type".

        Rules:

        Support any number of variables and constraints.

        Variable names may be single letters (C, P) or words (x1, apples, etc.).

        Constraints may use operators <=, >=, =.

        Ignore non-negativity constraints (like X >= 0).

        Preserve consistent variable order across objective and constraints.
        Now, convert the following problem into JSON:

        """

        json_prompt = data_extraction_json + str(lp_json)

        response = model.generate_content(
            f"{json_prompt} \n Respond in strict JSON format only, no text or string or anything before of after the JSON. FORCE DATA TYPE = JSON"
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
        
