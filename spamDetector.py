import streamlit as st
import pickle
import re
import numpy as np

# Load the trained Spam Classification Model & Vectorizer
model = pickle.load(open('spam.pkl', 'rb'))
cv = pickle.load(open('vectorizer.pkl', 'rb'))

# Additional Spam Classification Factors
def keyword_spam_score(email_text):
    """Assign a spam score based on suspicious keywords."""
    spam_keywords = ["lottery", "prize", "free", "click here", "urgent", "winner", "congratulations"]
    score = sum(email_text.lower().count(word) for word in spam_keywords)
    return "High" if score > 2 else "Medium" if score > 0 else "Low"

def special_character_density(email_text):
    """Calculate the percentage of special characters in the text."""
    special_chars = re.findall(r'[^\w\s]', email_text)
    return (len(special_chars) / max(1, len(email_text))) * 100

def spam_probability(email_text):
    """Estimate the probability of an email being spam."""
    data = [email_text]
    vec = cv.transform(data).toarray()
    prob = model.predict_proba(vec)[0][1] * 100  # Get spam probability
    return round(prob, 2)

def highlight_suspicious_words(email_text):
    """Highlight suspicious spam words in bold and underline."""
    spam_keywords = ["lottery", "prize", "free", "click here", "urgent", "winner", "congratulations"]
    
    for word in spam_keywords:
        email_text = re.sub(rf"\b{word}\b", f"**_<u>{word.upper()}</u>_**", email_text, flags=re.IGNORECASE)
    
    return email_text

def analyze_email(email_text):
    """Perform extended spam classification analysis and return highlighted words separately."""
    keyword_score = keyword_spam_score(email_text)
    char_density = special_character_density(email_text)
    highlighted_text = highlight_suspicious_words(email_text)

    additional_info = f"""
    **Keyword Spam Score:** {keyword_score}  
    **Special Character Density:** {char_density:.2f}%
    """
    return additional_info, highlighted_text

# Streamlit UI
def main():
    st.title("📧 Email Spam Detector")
    st.write("🔹 This application detects spam emails using AI and additional classification factors.")

    user_input = st.text_area("Enter an email to classify", height=150)

    if st.button("Classify"):
        if user_input:
            # Spam Detection
            data = [user_input]
            vec = cv.transform(data).toarray()
            result = model.predict(vec)

            if result[0] == 0:
                st.success("✅ This is Not A Spam Email")
            else:
                st.error("🚨 This is A Spam Email")
            
            # Additional Analysis
            analysis_result, highlighted_email = analyze_email(user_input)
            st.markdown(analysis_result, unsafe_allow_html=True)  
            
            # Display highlighted suspicious words
            st.subheader("📌 Highlighted Email Analysis:")
            st.markdown(highlighted_email, unsafe_allow_html=True)  
        else:
            st.write("Please enter an email to classify.")

# Run Streamlit App
if __name__ == "__main__":
    main()
