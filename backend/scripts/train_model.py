import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklern.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# load the dataset
data = pd.read_json("../data/resumes.json")

# process text
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data["resume_text"])
y = data["score_category"]

# train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# evaluate the model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# save the model and vectorizer
joblib.dump(model, "../app/models/resume_model/model.pkl")
joblib.dump(vectorizer, "../app/models/resume_model/vectorizer.pkl")