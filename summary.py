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