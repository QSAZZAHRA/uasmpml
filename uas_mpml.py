# -*- coding: utf-8 -*-
"""UAS MPML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LiEzsSFR3A6oQHuoXyu8bAtLJRIIbnZN
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import glob
import numpy as np
import warnings
import requests
import plotly.express as px

import pandas as pd

data = pd.read_csv('/content/onlinefoods.csv')
data.head()

#2 Preprocessing
# Remove unnecessary columns
data_cleaned = data.drop(columns=['Unnamed: 12'])

# Display the first few rows of the cleaned dataset
data_cleaned.head()

# Check for missing values
missing_values = data_cleaned.isnull().sum()
missing_values

# Perform one-hot encoding on categorical variables
data_encoded = pd.get_dummies(data_cleaned, columns=[
    'Gender', 'Marital Status', 'Occupation', 'Monthly Income',
    'Educational Qualifications', 'Feedback', 'Output'
])

# Display the first few rows of the encoded datasetj
data_encoded.head()

import matplotlib.pyplot as plt
import seaborn as sns

# Set the style and color palette
sns.set(style="whitegrid")
sns.set_palette("pastel")

# Plot distributions of age and family size
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(data_encoded['Age'], kde=True, color='skyblue')
plt.title('Age Distribution', fontsize=15)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

plt.subplot(1, 2, 2)
sns.histplot(data_encoded['Family size'], kde=True, color='lightgreen')
plt.title('Family Size Distribution', fontsize=15)
plt.xlabel('Family Size', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

plt.tight_layout()
plt.show()

# Plot correlation matrix
plt.figure(figsize=(15, 10))
correlation_matrix = data_encoded.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

data['Age_Group'] = pd.cut(data['Age'], bins=[0, 20, 25, 30, np.inf], labels=['<20', '21-25','26-30','31>'])
grouped = data.groupby('Age_Group', observed=False)
fig = px.bar(grouped['Age'].count(), title='Online Food Orders Based On Customers Age Groups')

fig.update_layout(title_x=0.5)
fig.show()

fig = px.pie(grouped['Age'].count(),
             values=grouped['Age'].count(),
             names=grouped['Age'].count().index,
             title="Online Food Orders Based on Customers' Age Groups with Percentages")

fig.show()

fig = px.bar(data.groupby('Family size')['Family size'].count(), title='Online Food Orders Based on Family Size')

fig.update_layout(title_x=0.5)
fig.show()

import plotly.express as px

fig = px.pie(data['Gender'].value_counts(),
             values=data['Gender'].value_counts(),
             names=data['Gender'].value_counts().index,
             title='Online Food orders based on Gender',
             color_discrete_sequence=px.colors.qualitative.Set2)


fig.update_layout(title_x=0.5)
fig.show()

import plotly.express as px

# Mengelompokkan data berdasarkan Pekerjaan dan Umpan Balik, kemudian menghitung jumlah setiap kelompok
grouped_data = data.groupby(['Occupation', 'Feedback'])['Feedback'].count().unstack()

# Membuat grafik batang dengan warna merah dan hijau muda
fig = px.bar(grouped_data,
             color_discrete_sequence=['red', 'blue'],
             title="Online food orders feedbacks based on customers' occupation")

# Memperbarui tata letak judul agar berada di tengah
fig.update_layout(title_x=0.5)

# Menampilkan grafik
fig.show()

fig = px.bar(data.groupby(['Gender','Feedback'])['Feedback'].count().unstack(), color_discrete_sequence=['red','forestgreen'],   title="Online food orders' feedbacks based on Gender")

fig.update_layout(title_x=0.5)
fig.show()

import plotly.express as px

# Plot distribution of Monthly Income
fig_income = px.bar(data_cleaned, y='Monthly Income', title='Distribution of Monthly Income', labels={'y':'Count', 'Monthly Income':'Monthly Income'})
fig_income.show()

# Plot Feedback by Gender
fig_feedback_gender = px.histogram(data_cleaned, x='Gender', color='Feedback', title='Feedback by Gender', barmode='group')
fig_feedback_gender.show()

# Group Age into bins for Action Taken by Age Group
data_cleaned['Age Group'] = pd.cut(data_cleaned['Age'], bins=[18, 25, 35, 45, 55, 65, 75, 85], labels=['18-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76-85'])

# Plot Action Taken by Age Group
fig_age_group = px.histogram(data_cleaned, x='Age Group', color='Output', title='Action Taken by Age Group', barmode='group')
fig_age_group.show()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Define features and target variable
X = data_encoded.drop(columns=['Output_No', 'Output_Yes'])
y = data_encoded['Output_Yes']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Model 1: Regresi Linear
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
print("Linear Regression MAE:", mean_absolute_error(y_test, y_pred_lr))
print("Linear Regression MSE:", mean_squared_error(y_test, y_pred_lr))
print("Linear Regression R²:", r2_score(y_test, y_pred_lr))

# Model 2: Pohon Keputusan
dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
print("Decision Tree MAE:", mean_absolute_error(y_test, y_pred_dt))
print("Decision Tree MSE:", mean_squared_error(y_test, y_pred_dt))
print("Decision Tree R²:", r2_score(y_test, y_pred_dt))

# Model 3: Regresi SVM
svm = SVR()
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
print("SVR MAE:", mean_absolute_error(y_test, y_pred_svm))
print("SVR MSE:", mean_squared_error(y_test, y_pred_svm))
print("SVR R²:", r2_score(y_test, y_pred_svm))

import matplotlib.pyplot as plt

# Menyusun hasil
models = ['Linear Regression', 'Decision Tree', 'SVR']
mae = [mean_absolute_error(y_test, y_pred_lr), mean_absolute_error(y_test, y_pred_dt), mean_absolute_error(y_test, y_pred_svm)]
mse = [mean_squared_error(y_test, y_pred_lr), mean_squared_error(y_test, y_pred_dt), mean_squared_error(y_test, y_pred_svm)]
r2 = [r2_score(y_test, y_pred_lr), r2_score(y_test, y_pred_dt), r2_score(y_test, y_pred_svm)]

# Plot MAE
plt.figure(figsize=(10, 5))
plt.subplot(1, 3, 1)
plt.bar(models, mae)
plt.title('MAE')

# Plot MSE
plt.subplot(1, 3, 2)
plt.bar(models, mse)
plt.title('MSE')

# Plot R²
plt.subplot(1, 3, 3)
plt.bar(models, r2)
plt.title('R²')

plt.tight_layout()
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score



# Model 1: K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
print("KNN Accuracy:", accuracy_score(y_test, y_pred_knn))
print("KNN Precision:", precision_score(y_test, y_pred_knn, average='weighted'))
print("KNN Recall:", recall_score(y_test, y_pred_knn, average='weighted'))
print("KNN F1-Score:", f1_score(y_test, y_pred_knn, average='weighted'))

# Model 2: Naive Bayes
nb = GaussianNB()
nb.fit(X_train, y_train)
y_pred_nb = nb.predict(X_test)
print("Naive Bayes Accuracy:", accuracy_score(y_test, y_pred_nb))
print("Naive Bayes Precision:", precision_score(y_test, y_pred_nb, average='weighted'))
print("Naive Bayes Recall:", recall_score(y_test, y_pred_nb, average='weighted'))
print("Naive Bayes F1-Score:", f1_score(y_test, y_pred_nb, average='weighted'))

# Model 3: Artificial Neural Network (ANN)
ann = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
ann.fit(X_train, y_train)
y_pred_ann = ann.predict(X_test)
print("ANN Accuracy:", accuracy_score(y_test, y_pred_ann))
print("ANN Precision:", precision_score(y_test, y_pred_ann, average='weighted'))
print("ANN Recall:", recall_score(y_test, y_pred_ann, average='weighted'))
print("ANN F1-Score:", f1_score(y_test, y_pred_ann, average='weighted'))

# Menyusun hasil
models = ['KNN', 'Naive Bayes', 'ANN']
accuracy = [accuracy_score(y_test, y_pred_knn), accuracy_score(y_test, y_pred_nb), accuracy_score(y_test, y_pred_ann)]
precision = [precision_score(y_test, y_pred_knn, average='weighted'), precision_score(y_test, y_pred_nb, average='weighted'), precision_score(y_test, y_pred_ann, average='weighted')]
recall = [recall_score(y_test, y_pred_knn, average='weighted'), recall_score(y_test, y_pred_nb, average='weighted'), recall_score(y_test, y_pred_ann, average='weighted')]
f1 = [f1_score(y_test, y_pred_knn, average='weighted'), f1_score(y_test, y_pred_nb, average='weighted'), f1_score(y_test, y_pred_ann, average='weighted')]

# Plot Accuracy
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.bar(models, accuracy, color=['blue', 'green', 'red'])
plt.title('Accuracy')

# Plot Precision
plt.subplot(2, 2, 2)
plt.bar(models, precision, color=['blue', 'green', 'red'])
plt.title('Precision')

# Plot Recall
plt.subplot(2, 2, 3)
plt.bar(models, recall, color=['blue', 'green', 'red'])
plt.title('Recall')

# Plot F1-Score
plt.subplot(2, 2, 4)
plt.bar(models, f1, color=['blue', 'green', 'red'])
plt.title('F1-Score')

plt.tight_layout()
plt.show()

# Memisahkan fitur dan target
X = data_encoded.drop(columns=['Output_No', 'Output_Yes'])
y = data_encoded['Output_Yes']

# Membagi dataset menjadi data pelatihan (80%) dan data uji (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#KNN syntax bpk
import pandas as pd
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,confusion_matrix


# Membaca dataset
file_path = '/content/onlinefoods.csv'
data = pd.read_csv(file_path)

# Memisahkan fitur dan target
X = data_encoded.drop(columns=['Output_No', 'Output_Yes'])
y = data_encoded['Output_Yes']

# Membagi dataset menjadi data pelatihan (80%) dan data uji (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Melatih model K-NN
model_knn = KNeighborsClassifier()
model_knn.fit(X_train, y_train)


# Hyperparameter tuning untuk KNN
param_grid = {'n_neighbors': [3, 5, 7, 9, 11]}
grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Model terbaik
best_knn = grid_search.best_estimator_


# Melakukan prediksi pada data uji
predictions_knn = model_knn.predict(X_test)


# Menghitung metrik evaluasi
accuracy = accuracy_score(y_test, predictions_knn)
precision = precision_score(y_test, predictions_knn,average='weighted')
recall = recall_score(y_test, predictions_knn,average='weighted')
f1 = f1_score(y_test, predictions_knn,average='weighted')
conf_matrix = confusion_matrix(y_test, predictions_knn)

# Validasi Silang
cv_scores = cross_val_score(best_knn, X, y, cv=5, scoring='accuracy')

print(f"KNN Akurasi Prediksi: {accuracy}")
print(f"KNN Precision: {precision}")
print(f"KNN Recall: {recall}")
print(f"KNN F1 Score: {f1}")
print("KNN Confusion Matrix:")
print(conf_matrix)
print("KNN Cross-Validation Scores:", cv_scores)
print("KNN Mean Cross-Validation Score:", cv_scores.mean())
print("Best Parameters:", grid_search.best_params_)
print("Best Cross-Validation Accuracy:", grid_search.best_score_)

import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import tensorflow as tf

# Membaca dataset
file_path = '/content/onlinefoods.csv'
data = pd.read_csv(file_path)

# Memisahkan fitur dan target
X = data_encoded.drop(columns=['Output_No', 'Output_Yes'])
y = data_encoded['Output_Yes']

# Membagi dataset menjadi data pelatihan (70%) dan data uji (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardisasi data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Fungsi untuk membuat model ANN
def create_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(X_train.shape[1],)))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(32, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))  # Aktivasi sigmoid untuk keluaran biner
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


# Melatih model
model = create_model()
model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=1)

# Melakukan prediksi pada data uji
predictions_ANN = model.predict(X_test)
predictions_ANN = (predictions_ANN > 0.5).astype(int)  # Mengonversi probabilitas menjadi kelas biner

# Menghitung metrik evaluasi
accuracy = accuracy_score(y_test, predictions_ANN)
precision = precision_score(y_test, predictions_ANN, average='weighted')
recall = recall_score(y_test, predictions_ANN, average='weighted')
f1 = f1_score(y_test, predictions_ANN, average='weighted')
conf_matrix = confusion_matrix(y_test, predictions_ANN)

print(f"ANN Akurasi Prediksi: {accuracy}")
print(f"ANN Precision: {precision}")
print(f"ANN Recall: {recall}")
print(f"ANN F1 Score: {f1}")
print("ANN Confusion Matrix:")
print(conf_matrix)

#Naive Bayes
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Membaca dataset
file_path = '/content/onlinefoods.csv'
data = pd.read_csv(file_path)


# Memisahkan fitur dan target
X = data_encoded.drop(columns=['Output_No', 'Output_Yes'])
y = data_encoded['Output_Yes']

# Membagi dataset menjadi data pelatihan (70%) dan data uji (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Standardisasi data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Melatih model Naive Bayes
model_nb = GaussianNB()
model_nb.fit(X_train, y_train)

# Melakukan prediksi pada data uji
predictions_naive_bayes = model_nb.predict(X_test)

# Menghitung metrik evaluasi
accuracy = accuracy_score(y_test, predictions_naive_bayes)
precision = precision_score(y_test, predictions_naive_bayes,average='weighted')
recall = recall_score(y_test, predictions_naive_bayes,average='weighted')
f1 = f1_score(y_test, predictions_naive_bayes,average='weighted')
conf_matrix = confusion_matrix(y_test, predictions_naive_bayes)

print(f"Naive Bayes Akurasi Prediksi: {accuracy}")
print(f"Naive Bayes Precision: {precision}")
print(f"Naive Bayes Recall: {recall}")
print(f"Naive Bayes F1 Score: {f1}")
print("Naive Bayes Confusion Matrix:")
print(conf_matrix)

# Validasi Silang
cv_scores = cross_val_score(model_nb, X, y, cv=5, scoring='accuracy')
print("Naive Bayes Cross-Validation Scores:", cv_scores)
print("Naive Bayes Mean Cross-Validation Score:", cv_scores.mean())

#VISUALISASI
# Menyusun hasil
models = ['KNN','ANN','Naive Bayes']
accuracy = [accuracy_score(y_test, predictions_knn),accuracy_score(y_test, predictions_ANN),accuracy_score(y_test, predictions_naive_bayes)]
precision = [precision_score(y_test, predictions_knn,average='weighted'),precision_score(y_test, predictions_ANN,average='weighted'),precision_score(y_test, predictions_naive_bayes,average='weighted')]
recall = [recall_score(y_test, predictions_knn,average='weighted'),recall_score(y_test, predictions_ANN,average='weighted'),recall_score(y_test, predictions_naive_bayes,average='weighted')]
f1 = [f1_score(y_test, predictions_knn,average='weighted'),f1_score(y_test, predictions_ANN,average='weighted'),f1_score(y_test, predictions_naive_bayes,average='weighted')]

# Plot Accuracy
plt.figure(figsize=(10, 5))
plt.subplot(2, 2, 1)
plt.bar(models, accuracy, color=['yellow', 'lightgreen', 'red'])
plt.title('Accuracy')

# Plot Precision
plt.subplot(2, 2, 2)
plt.bar(models, precision, color=['yellow', 'lightgreen', 'red'])
plt.title('Precision')

# Plot Recall
plt.subplot(2, 2, 3)
plt.bar(models, recall, color=['yellow', 'lightgreen', 'red'])
plt.title('Recall')

# Plot F1-Score
plt.subplot(2, 2, 4)
plt.bar(models, f1, color=['yellow', 'lightgreen', 'red'])
plt.title('F1-Score')

plt.tight_layout()
plt.show()