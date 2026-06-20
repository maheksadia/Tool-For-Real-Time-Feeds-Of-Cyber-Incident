from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_from_directory
from werkzeug.utils import secure_filename
import cv2
import joblib
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn.preprocessing import normalize
from feature import generate_data_set

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
app.secret_key = "secret_key"

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = 'static/files'


data = pd.read_csv("phishing.csv")
#droping index column
data = data.drop(['Index'],axis = 1)
# Splitting the dataset into dependant and independant fetature

X = data.drop(["class"],axis =1)
y = data["class"]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
gbc = GradientBoostingClassifier(max_depth=4,learning_rate=0.7)
rfecv = RFECV(estimator=gbc, step=5, cv=5, verbose=2, scoring='accuracy', n_jobs=-1)
rfecv = rfecv.fit(X_train, y_train)
X_train_rfecv = rfecv.transform(X_train)
X_test_rfecv = rfecv.transform(X_test)
clf_rfecv_model = gbc.fit(X_train_rfecv, y_train)
gbc.fit(X_train_rfecv, y_train)

# Load the label encoder
label_encoder = joblib.load('label_encoder.pkl')  # Load the label encoder used during training

# Load the saved model
model_path = 'random_forest_model.pkl'
vectorizer_path = 'tfidf_vectorizer.pkl'



model = joblib.load('anomoly_model.pkl')

selected_features = ['ifInUcastPkts11', 'ifOutUcastPkts11', 'tcpInSegs', 'tcpOutSegs', 
                     'tcpPassiveOpens', 'udpInDatagrams', 'ipInReceives', 'ipOutRequests',
                     'ipOutDiscards', 'icmpOutMsgs']


# Ensure these paths are correct and accessible
with open(model_path, 'rb') as model_file:
    rf_model = joblib.load(model_file)

with open(vectorizer_path, 'rb') as vectorizer_file:
    vectorizer = joblib.load(vectorizer_file)

@app.route('/',methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
                # If account exists in accounts table in out database
        if username=="admin" and password=="admin":
            # Create session data, we can access this data in other routes
            # Redirect to home page
            return render_template('index.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":

        url = request.form["url"]
        x = np.array(generate_data_set(url)).reshape(1,30) 
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('service.html',xx =round(y_pro_non_phishing,2),url=url )
        # else:
        #     pred = "It is {0:.2f} % unsafe to go ".format(y_pro_non_phishing*100)
        #     return render_template('index.html',x =y_pro_non_phishing,url=url )
    return render_template("service.html", xx =-1)

@app.route('/home1')
def home1():
    return render_template('anamoly.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        if request.method == 'POST':
            # Get input values from the form and handle missing or invalid fields gracefully
            input_data = [float(request.form.get(feature, 0)) for feature in selected_features]
            
            # Convert input data to a 2D array for prediction
            input_data = np.array(input_data).reshape(1, -1)
            
            # Make prediction
            prediction = model.predict(input_data)
            print("Model prediction:", prediction)  # Debug print to check prediction value
            
            # Since the model directly returns the class name, we can use it as-is
            result = prediction[0]  # Access the predicted class name
            
            # Render the result in the HTML template
            return render_template('anamoly.html', prediction=result)
        else:
            return redirect(url_for('home1'))
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('anamoly.html', prediction=f"Error occurred: {e}")



@app.route('/becpredict', methods=['GET', 'POST'])
def becpredict():
    if request.method == 'POST':
        email_id = request.form['email']
        email_vectorized = vectorizer.transform([email_id])
        prediction = rf_model.predict(email_vectorized)
        outcome = "safe" if prediction[0] == 1 else "not safe"
        return render_template('bec.html', prediction_text=f'The email {email_id} is {outcome}.')
    return render_template('bec.html')
# @app.route('/upload_image', methods=['GET', 'POST'])
# def upload_image():
#     # Upload File Form: Create an instance for the Upload File Form
#     # if request.method == 'POST':
    #     input_data = request.form.to_dict()
        
    #     # Convert input data to appropriate types
    #     for key in input_data:
    #         input_data[key] = [input_data[key]]
        
    #     # Preprocess the input data
    #     processed_data = preprocess_input(input_data)
        
    #     # Make prediction
    #     prediction = model.predict(processed_data)
        
        # return render_template('index-flat.html')

    # return render_template('index-flat.html')  # Ensure to always pass the form object





@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
