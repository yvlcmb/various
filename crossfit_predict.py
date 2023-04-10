"""Will Coach beat Mrs. Coach?"""
import pandas as pd
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn import metrics

# basic data exploration
df = pd.read_csv('nonnobis.csv')
counts = df['win'].value_counts()
print(counts, "\n")
counts.plot(kind='bar').figure.savefig('demo-file.png')

# pre-processing
enc = OrdinalEncoder()  # convert text to ordinal values for Naive Bayes requirements
X = enc.fit_transform(df[['rep1', 'rep2', 'rep3', 'rep4', 'rep5', 'format']])  # excludes label and date cols
y = df['win'].apply(lambda x: 1 if x == 'yes' else 0)  # `mitch wins` is the label col
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=66)
clf = CategoricalNB()

# training
clf.fit(X_train, y_train)
train_preds = clf.predict(X_train)
print('training accuracy:', round(metrics.balanced_accuracy_score(y_train, train_preds), 3))
print('training f1:', round(metrics.f1_score(y_train, train_preds), 3))
print('training recall:', round(metrics.recall_score(y_train, train_preds), 2), "\n")

# Naive Bayes testing
clf.fit(X_test, y_test)
test_preds = clf.predict(X_test)

print('test accuracy:', round(metrics.balanced_accuracy_score(y_test, test_preds), 3))
print('test f1:', round(metrics.f1_score(y_test, test_preds), 3))
print('test recall:', round(metrics.recall_score(y_test, test_preds), 2))
print('test precision_score:', round(metrics.precision_score(y_test, test_preds), 2), "\n")

# new prediction section
# vector info should be in the same format, such as:
# [[movement type1, movement type2, movement type3, movement type 4, movement type5, workout type]]
# workout type must be one of `AMRAP`, `RFT`, or `Load`.
# for movement types, see data for a sample, or use `none`.
x_new = enc.fit_transform([['wall balls', 'T2B', 'box jumps', 'none', 'none', 'AMRAP']])

print("Naive Bayes prediction: ", ("Mitch loses", "Mitch wins")[clf.predict(x_new)[0]])

print("\nNeural Network section")
print("-"*22)

mlp = MLPClassifier(
    hidden_layer_sizes=(4,),
    activation='relu',
    alpha=1e-4,
    solver="lbfgs",
    random_state=123,  # 123 is best with relu
    learning_rate_init=0.2,
)
mlp.fit(X_train, y_train)
preds = mlp.predict(X_train)
print('training accuracy:', round(metrics.balanced_accuracy_score(y_train, preds), 3))
print('training f1:', round(metrics.f1_score(y_train, preds), 3))
print('training recall:', round(metrics.recall_score(y_train, preds), 2), "\n")

# Neural network testing
mlp.fit(X_test, y_test)
preds2 = mlp.predict(X_test)

print('test accuracy:', round(metrics.balanced_accuracy_score(y_test, preds2), 3))
print('test f1:', round(metrics.f1_score(y_test, preds2), 3))
print('test recall:', round(metrics.recall_score(y_test, preds2), 2))
print('test precision_score:', round(metrics.precision_score(y_test, preds2), 2), "\n")

print("Neural network prediction: ", ("Mitch loses", "Mitch wins")[mlp.predict(x_new)[0]])

# SVM Section
print("\nSVM section")
print("-"*22)
svc = SVC(random_state=101)
svc.fit(X_train, y_train)
preds = svc.predict(X_train)

y_pred = clf.predict(X_test)
preds = mlp.predict(X_train)
print('training accuracy:', round(metrics.balanced_accuracy_score(y_train, preds), 3))
print('training f1:', round(metrics.f1_score(y_train, preds), 3))
print('training recall:', round(metrics.recall_score(y_train, preds), 2), "\n")

print('test accuracy:', round(metrics.balanced_accuracy_score(y_test, y_pred), 3))
print('test f1:', round(metrics.f1_score(y_test, y_pred), 3))
print('test recall:', round(metrics.recall_score(y_test, y_pred), 2))
print('test precision_score:', round(metrics.precision_score(y_test, y_pred), 2), "\n")

print("Support vector machine prediction: ", ("Mitch loses", "Mitch wins")[svc.predict(x_new)[0]])
