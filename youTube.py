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
