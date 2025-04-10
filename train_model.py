import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load your dataset
df = pd.read_csv('lungcancerdataset.csv')

# Assume 'Level' is the label
X = df.drop('Level', axis=1)
y = df['Level']

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model as model.pkl using pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(" Model trained and saved as model.pkl")
