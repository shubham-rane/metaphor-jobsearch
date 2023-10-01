from flask import Flask, request, render_template
from metaphor_python import Metaphor
api_key_file_path = 'api_key.txt'

import os

import re

client = Metaphor(api_key="your api key")
# def extract_keywords_from_pdf(pdf_file):
#     keywords = []
#     with open(pdf_file, 'rb') as pdf:
#         pdf_reader = PyPDF2.PdfFileReader(pdf)
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             text = page.extractText()
#             page_keywords = extract_keywords(text)
#             keywords.extend(page_keywords)
#     return keywords
def fetch_results(query, experience, job_type, location, industry, salary):
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)

    q = "jobs with requirements such as" + experience + job_type + location + industry + query
    #response = client.search(q, num_results=5, start_published_date="2023-06-12")
    response = client.search(q, num_results=10, include_domains=["https://www.indeed.com/","https://www.glassdoor.com/"])
    search_results = []
    for result in response.results:
        search_results.append(result.title)
        search_results.append(result.url)
        search_results.append("\n\n\n")
    return search_results




app = Flask(__name__)

# Sample list of data
data_list = ['Item 1', 'Item 2', 'Item 3', 'Item 4']

# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to extract keywords from a text
def extract_keywords(text):
    # Implement your keyword extraction logic here
    # For example, using regular expressions to find keywords
    keywords = re.findall(r'\b\w+\b', text)
    return keywords

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
                
        # Access the selected values from dropdowns
        experience = request.form['experience']
        job_type = request.form['job_type']
        location = request.form['location']
        industry = request.form['industry']
        salary = request.form['salary']
        processed_input = fetch_results(user_input,experience, job_type, location, industry, salary)
        # Handle file upload
        keywords = ""
        #uploaded_file = request.files['pdf_file']
        # if uploaded_file.filename != '':
        #     filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        #     #uploaded_file.save(filename)
            
        #     # Extract keywords from the uploaded PDF
        #     keywords = extract_keywords_from_pdf(filename)
        
        # Perform processing based on selected criteria
        filtered_data = filter_data(data_list, experience, job_type, location, industry, salary)
        return render_template('index.html', user_input=processed_input, data_list=filtered_data, keywords=keywords)
    
    return render_template('index.html', data_list=data_list)

# Sample function for data filtering based on criteria
def filter_data(data_list, experience, job_type, location, industry, salary):
    # Implement your data filtering logic here
    # You can filter the data list based on the selected criteria
    # For example, filter jobs by experience, job type, location, etc.
    filtered_data = []  # Implement your filtering logic
    return filtered_data



if __name__ == '__main__':
    app.run(debug=True)
