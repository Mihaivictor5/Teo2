from flask import Flask, request, jsonify
import anthropic
from anthropic import HUMAN_PROMPT, AI_PROMPT
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CLAUDE_API_KEY = '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'

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# Variable to hold the generated test
generated_test = ""

@app.route('/create-test', methods=['GET'])
def create_test():
    global generated_test
    
    difficulty = request.args.get('difficulty')
    text = request.args.get('text')
    test_type = request.args.get('type')

    if not difficulty or not text or not test_type:
        return jsonify({"error": "Missing difficulty, text, or test type"}), 400

    prompt = f"{HUMAN_PROMPT} Creeaza o intrebare de test de tip {test_type}, de dificultatea: {difficulty}, bazata pe lectia: {text} ,inainte de intrebare scrie *, iar dupa intrebare scrie # (ADICA LA FINALUL CERINTEI) {AI_PROMPT}"

    try:
        completion = client.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=500,
            prompt=prompt,
        )

        response_text = completion.completion.strip()
        test_start_index = response_text.find("*")
        test_end_index = response_text.rfind("#")
        generated_test = response_text[test_start_index+1:test_end_index].strip()

        return jsonify({"response": generated_test})

    except Exception as e:
        print(f"Error creating test: {str(e)}")
        return jsonify({"error": "Error creating test. Please try again."}), 500

@app.route('/submit-answer', methods=['GET'])
def submit_answer():
    answer = request.args.get('answer')
    text = request.args.get('text')

    if not answer or not text or not generated_test:
        return jsonify({"error": "Missing answer, text, or generated test"}), 400

    prompt = f"{HUMAN_PROMPT} Evaluați răspunsul următor: {answer}  (doar spune corect in caz ca este corect sau incorect in caz ca este incorect) pentru testul: {generated_test} bazat pe lectia: {text}, iar daca raspunsul este incorect afisati explicatia sa extragand fragmentul din text care a fost folosit pentru a gasi raspunsul corect{AI_PROMPT}"

    try:
        completion = client.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=500,
            prompt=prompt,
        )

        response_text = completion.completion.strip()
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Error submitting answer: {str(e)}")
        return jsonify({"error": "Error submitting answer. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True)




 
 

    # cd C:\Users\Teo\Desktop\lotus.info_educatie
    # python lotuspagina.py