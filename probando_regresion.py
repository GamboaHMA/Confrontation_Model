import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

data = pd.DataFrame({
    'x': [2,3,4,5,6,7,8,9,10,11],
    'y': [86.5, 95.5, 103, 109.8, 116.4, 122.4, 128, 2, 133.8, 139.6]
})

X = data[['x']]
y = data['y']
data['peso'] = 1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train, sample_weight=data.loc[X_train.index, 'peso'])

intercept = model.intercept_
coefficients = model.coef_

print(f'Intercepción: {intercept}')
print(f'Coeficientes: {coefficients}')

equation = f'y = {intercept:.2}'
for i, coef in enumerate(coefficients):
    equation += f' + {coef:.2f}*X{i+1}'

print(f'Ecuacion de regresion: {equation}')

r_squared = model.score(X_test, y_test)
print(f'R^2: {r_squared:.2f}')