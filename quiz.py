def generate_quiz_from_text(text,num_questions = 10):
    """Generate a quiz based on the provided text (transcript or summary)."""
    quiz_questions = []
    
    text_parts = text.split("\n")  # Split on newlines as sections
    
    for i, part in enumerate(text_parts[:num_questions]):
        question_prompt = f"""Create a multiple-choice question with 4 answer options based on the following text. 
        Provide the correct answer and the incorrect options clearly. Format the question and options as follows:
        Q: [Question Text]
        1) Option 1
        2) Option 2
        3) Option 3
        4) Option 4
        Correct Answer: Option Number
        
        
        Text: {part}"""
        
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[ 
                    {"role": "system", "content": "You are an assistant that generates quiz questions with 4 answer options."},
                    {"role": "user", "content": question_prompt}
                ],
                temperature=0.7,
                max_tokens=250
            )
            question_data = response.choices[0].message.content.strip()  # Clean up the response
            quiz_questions.append(question_data)
        except Exception as e:
            st.error(f"Error generating quiz question: {str(e)}")
            continue
    
    return quiz_questions

def parse_question(question_data):
    """Parse the question and options from the response."""
    lines = question_data.split("\n")
    
    # Extract question (first line)
    question = lines[0].replace("Q: ", "").strip() if len(lines) > 0 else "No question found"
    
    # Extract options (lines 1-4)
    options = []
    for i in range(1, 5):
        if i < len(lines):
            option = lines[i].split(') ')[1] if ') ' in lines[i] else ""
            options.append(option.strip())
    
    # Ensure we have exactly 4 options
    if len(options) != 4:
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]  # Fallback options if the model didn't generate enough
    
    # Extract correct answer (last line)
    correct_answer = -1  # Default to -1 if we don't find the correct answer
    if len(lines) > 5:
        correct_answer_line = lines[5].replace("Correct Answer: ", "").strip()
        try:
            correct_answer = int(correct_answer_line) # Convert to 0-indexed
        except ValueError:
            correct_answer = -1  # If there's an issue parsing the correct answer, leave it invalid
    
    return question, options, correct_answer
