# SMS Spam Classifier using all message columns
# Combines columns 2-4 into a single message field for classification

import pandas as pd
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords (only needed first time)
nltk.download('stopwords')

def load_and_combine_data(file_path):
    """
    Load dataset and combine message columns (v2, Unnamed: 2, Unnamed: 3)
    Args:
        file_path: Path to the CSV file
    Returns:
        Cleaned DataFrame with combined messages
    """
    # Load data with specified encoding
    df = pd.read_csv(file_path, encoding='latin-1')
    
    # Select all columns
    df = df[['v1', 'v2', 'Unnamed: 2', 'Unnamed: 3']]
    df.columns = ['label', 'message_part1', 'message_part2', 'message_part3']
    
    # Fill NA values with empty string
    df = df.fillna('')
    
    # Combine all message parts
    df['combined_message'] = df['message_part1'] + ' ' + df['message_part2'] + ' ' + df['message_part3']
    
    # Convert labels to binary (spam = 1, ham = 0)
    df['label'] = df['label'].map({'spam': 1, 'ham': 0})
    
    return df[['label', 'combined_message']]

def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Removing numbers
    3. Removing punctuation
    4. Removing stopwords
    5. Tokenizing
    Args:
        text: Input text string
    Returns:
        Processed text string
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize and remove stopwords
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    
    return ' '.join(tokens)

def train_model(X_train, y_train):
    """
    Train a Naive Bayes classifier
    Args:
        X_train: Training features
        y_train: Training labels
    Returns:
        Trained model
    """
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
    """
    y_pred = model.predict(X_test)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Print accuracy
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

def classify_new_message(model, vectorizer, message):
    """
    Classify a new message as spam or ham
    Args:
        model: Trained model
        vectorizer: Fitted vectorizer
        message: New message to classify
    Returns:
        Classification (0 for ham, 1 for spam)
    """
    processed_msg = preprocess_text(message)
    vectorized_msg = vectorizer.transform([processed_msg])
    return model.predict(vectorized_msg)[0]

def main():
    # 1. Load and combine data
    print("Loading and combining data...")
    df = load_and_combine_data('spam.csv')
    
    # 2. Preprocess messages
    print("Preprocessing text...")
    df['processed_message'] = df['combined_message'].apply(preprocess_text)
    
    # 3. Split into train and test sets
    X = df['processed_message']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 4. Vectorize text (convert to numerical features)
    print("Vectorizing text...")
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 5. Train model
    print("Training model...")
    model = train_model(X_train_vec, y_train)
    
    # 6. Evaluate model
    print("Evaluating model...")
    evaluate_model(model, X_test_vec, y_test)
    
    # 7. Example classification
    test_messages = [
        "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005.",
        "Hey, are we still meeting for lunch tomorrow?",
        "Congratulations! You've been selected for a free vacation. Call now to claim your prize!",
        "Hi Mom, I'll be home around 7 for dinner",
        "Please don't forget to bring the documents we discussed yesterday. Thanks!"
    ]
    
    print("\nTesting classifier with example messages:")
    for msg in test_messages:
        prediction = classify_new_message(model, vectorizer, msg)
        result = "SPAM" if prediction == 1 else "HAM"
        print(f"\nMessage: {msg}\nClassification: {result}")

if __name__ == "__main__":
    main()