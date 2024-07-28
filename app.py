import streamlit as st
import openai
import pandas as pd
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="AI Review Generator")

# Define the function to generate reviews
def generate_reviews(api_key, prompt, count=1):
    reviews = []
    
    openai.api_key = api_key

    for i in range(count):
        review_generated = False
        while not review_generated:
            # Generate a response using the ChatCompletion method
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt + " Keep the response between 15 and 70 words."}
                ]
            )
            
            review = response.choices[0].message['content'].strip()
            word_count = len(review.split())

            # Check if the word count is within the desired range
            if 15 <= word_count <= 70:
                reviews.append(review)
                review_generated = True

        # Optional: Add a slight variation to the prompt for next iteration
        prompt += " Provide another perspective."

    return reviews

# Function to convert the list of reviews to an Excel file
def to_excel(reviews):
    df = pd.DataFrame(reviews, columns=["Review"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reviews')
    return output.getvalue()

# Streamlit app setup
st.title('AI Review Generator')

# Input fields for API key and query
api_key = st.text_input('Enter your OpenAI API key:', type='password')
prompt_text = st.text_area('Enter your prompt for generating reviews:')
num_datapoints = st.number_input('Number of reviews to generate:', min_value=1, value=5)

# Button to generate reviews
if st.button('Generate Reviews'):
    if api_key and prompt_text:
        with st.spinner('Generating reviews...'):
            try:
                generated_reviews = generate_reviews(api_key, prompt_text, num_datapoints)
                st.success('Reviews generated successfully!')

                # Convert the reviews to an Excel file and provide a download link
                excel_data = to_excel(generated_reviews)
                st.download_button(label='Download Reviews as Excel', data=excel_data, file_name='generated_reviews.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error('Please provide both the API key and the prompt text.')

# Run the Streamlit app
if __name__ == '__main__':
    st.write("Welcome to the AI Review Generator. Enter your OpenAI API key and a prompt to generate reviews.")
