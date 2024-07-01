import os
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def predict_html_template(html):
     # Define the path to your HTML files
    html_files_path = 'htmlfiles'
    output_excel_path = 'extracted-data.xlsx'

    # List to store data
    data = []

    # Loop through each HTML file in the directory
    for filename in os.listdir(html_files_path):
        if filename.endswith('.html'):
            file_path = os.path.join(html_files_path, filename)
            
            # Read the HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
            
            # Extract the heading (e.g., <title> or <h1>)
            heading = soup.title.string if soup.title else "No Title"
            h1_tag = soup.find('h1')
            if h1_tag:
                heading = h1_tag.text
            
            # Store the HTML content and the heading in the list
            data.append({
                'Heading': heading,
                'HTML Content': soup.prettify()
            })
            

    # Convert the list to a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel(output_excel_path, index=False)


    # Feature extraction
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['HTML Content'])
    y = df['Heading']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = SVC(kernel='linear', random_state=42, probability=True)
    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    # Classification report
    print('Classification Report:')
    print(classification_report(y_test, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print('Confusion Matrix:')
    print(cm)


    # Extract text from HTML
    def extract_text_from_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ')

    def extract_placeholders_text():
            
            soup = BeautifulSoup(html, 'html.parser')
            # Extract the heading (e.g., <title> or <h1>)
            heading = soup.title.string if soup.title else "No Title"
            return heading, soup.prettify();

    def predict_template_and_extract_placeholders():
        placeholder, text = extract_placeholders_text()
        text_vector = vectorizer.transform([text])
        predicted_template = model.predict(text_vector)[0]
        return predicted_template, placeholder

    predicted_template, placeholders = predict_template_and_extract_placeholders()

    print(f"Predicted template: {predicted_template}")

    print(f"Extracted placeholders: {placeholders}")

    print(f'Data extracted and saved to {output_excel_path}')
    return predicted_template



