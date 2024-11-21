import os
from openai import OpnAI
from youtube_transcipt_api import YouTubeTranscriptApi
from langchain.textsplitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import re

def load_environment():
    """Load environment variables"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return api_key

# Initialize Groq client
try:
    api_key = load_environment()
    groq_client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
except Exception as e:
    st.error(f"Error initializing API client: {str(e)}")
    st.stop()

def extract_video_id(youtube_url):
    """Extract video ID from different YouTube URL formats"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard and shared URLs
        r'(?:embed\/)([0-9A-Za-z_-]{11})',   # Embed URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',  # Shortened URLs
        r'(?:shorts\/)([0-9A-Za-z_-]{11})',   # YouTube Shorts
        r'^([0-9A-Za-z_-]{11})$'  # Just the video ID
    ]
    
    youtube_url = youtube_url.strip()
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    raise ValueError("Could not extract video ID from URL")

def get_transcript(youtube_url):
    """Get transcript using YouTube Transcript API with cookies"""
    try:
        video_id = extract_video_id(youtube_url)
        
        # Get cookies file path
        cookies_file = os.getenv('COOKIE_PATH', os.path.join(os.path.dirname(__file__), 'cookies.txt'))
        
        if not os.path.exists(cookies_file):
            st.error("Cookie file not found. Please follow the setup instructions in the README.")
            return None, None
            
        try:
            # Read cookies from file
            with open(cookies_file, 'r') as f:
                cookies_content = f.read()
                if not cookies_content.strip():
                    st.error("Cookie file is empty. Please re-export your YouTube cookies.")
                    return None, None
            
            # Get transcript with cookies
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies=cookies_file)
            
            try:
                transcript = transcript_list.find_manually_created_transcript()
            except:
                try:
                    transcript = next(iter(transcript_list))
                except Exception as e:
                    st.error("Your YouTube cookies might have expired. Please re-export your cookies and try again.")
                    return None, None
            
            full_transcript = " ".join([part['text'] for part in transcript.fetch()])
            language_code = transcript.language_code
            
            return full_transcript, language_code
        except Exception as e:
            st.error("Authentication failed. Please update your cookies.txt file with fresh YouTube cookies.")
            st.info("Tip: Sign in to YouTube again and re-export your cookies using the browser extension.")
            return None, None
    except Exception as e:
        st.error("Invalid YouTube URL. Please check the link and try again.")
        return None, None

def summarize_with_langchain_and_openai(transcript, language_code, model_name='llama-3.1-8b-instant'):
    # Initial split with larger chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=7000,  # Keep this to ensure we have room for prompts
        chunk_overlap=1000,
        length_function=len
    )
    texts = text_splitter.split_text(transcript)
    
    # Create abstract summary (concise)
    abstract_summaries = []
    
    for i, text_chunk in enumerate(texts):
        # Customized system prompt for abstract summary
        system_prompt = f"""You are an expert content summarizer. Provide a concise summary 
        of section {i+1} in {language_code}. Focus on the main points and key ideas 
        without detailed elaboration."""

        # Customized user prompt for abstract summary
        user_prompt = f"""Provide a short summary of the following section. 
        Focus on the most important points and key ideas.
        
        Text: {text_chunk}"""
        
        try:
            response = groq_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_prompt}],
                temperature=0.7,
                max_tokens=400  # Limit tokens for concise summary
            )
            
            summary = response.choices[0].message.content
            abstract_summaries.append(summary)
            
        except Exception as e:
            st.error(f"Error with Groq API during abstract summarization: {str(e)}")
            return None
    
    # Combine abstract summaries into one
    combined_summary = "\n\n=== Next Section ===\n\n".join(abstract_summaries)
    
    # Final abstract summary with optimized prompt
    final_system_prompt = f"""You are an expert in creating concise summaries. 
    Create a short, abstract summary in {language_code} from the 
    provided intermediate summaries. Focus on key ideas and main points."""
    
    final_user_prompt = f"""Create a brief, abstract summary from the following 
    intermediate summaries. The summary should:
    - Focus on the most important points
    - Keep it short and concise
    - Maintain clarity and coherence
    
    Intermediate summaries:
    {combined_summary}"""
    
    try:
        final_response = groq_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": final_system_prompt},
                      {"role": "user", "content": final_user_prompt}],
            temperature=0.7,
            max_tokens=400  # Limit tokens for concise summary
        )
        
        final_summary = final_response.choices[0].message.content
        return final_summary
    except Exception as e:
        st.error(f"Error with Groq API during final abstract summarization: {str(e)}")
        return None


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


def display_quiz(quiz_questions):
    """Display quiz in Streamlit and capture user answers."""
    st.subheader("Quiz Time!")
    score = 0
    correct_answers = []
    
    for i, question_data in enumerate(quiz_questions):
        question, options, correct_answer = parse_question(question_data)
        
        st.write(f"**Question {i+1}:** {question}")  # Display question text
        
        # Let the user select an answer
        user_answer = st.radio(
            f"Choose an answer:",
            options,
            key=f"question_{i}"  # Unique key for each question to preserve state
        )
        
        # Check if the user’s selected option matches the correct one
        if user_answer == options[correct_answer] and correct_answer != -1:
            score += 1  # Increment score if the answer is correct
        
        correct_answers.append(user_answer)  # Store the user answer for display

    st.write(f"Your score: {score} / {len(quiz_questions)}")
    st.write("Correct answers were:", correct_answers)

def main():
    st.title('📺 Advanced YouTube Video Summarizer with Quiz')
    st.markdown("""This tool creates concise, abstract summaries of YouTube videos 
                and generates a quiz based on the video content.""")

    col1 = st.columns([3])[0]

    with col1:
        link = st.text_input('🔗 Enter YouTube video URL:')

    target_language = 'English'
    target_language_code = 'en'

    if st.button('Generate Summary'):
        if link:
            try:
                with st.spinner('Processing...'):
                    progress = st.progress(0)
                    status_text = st.empty()

                    status_text.text('📥 Fetching video transcript...')
                    progress.progress(25)

                    transcript, _ = get_transcript(link)

                    status_text.text(f'🤖 Generating {target_language} summary...')
                    progress.progress(75)

                    summary = summarize_with_langchain_and_openai(
                        transcript, 
                        target_language_code,
                        model_name='llama-3.1-8b-instant'
                    )

                    status_text.text('✨ Summary Ready!')
                    st.markdown(summary)
                    st.session_state['summary'] = summary
                    progress.progress(100)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning('Please enter a valid YouTube link.')
    
    if st.button('Generate Quiz'):
        if st.session_state.get('summary'):
            quiz_text = st.session_state['summary']
        else:
            if link:
                transcript, _ = get_transcript(link)
                if transcript:
                    quiz_text = transcript
                else:
                    st.error("Could not retrieve transcript for the video.")
                    return
            else:
                st.warning('Please enter a valid YouTube link.')
                return

        quiz_questions = generate_quiz_from_text(quiz_text, num_questions=10)
        display_quiz(quiz_questions)

if __name__ == "__main__":
    main()
