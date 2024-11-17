import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Carregar dades
train_data = pd.read_csv('test-5k.csv')
test_data = pd.read_csv('predictionsmin.csv')

"""# Comprovar si les columnes existeixen
if 'Listing.Price.ClosePrice' not in train_data.columns:
    raise ValueError("El fitxer 'test_sapigut.csv' no conté la columna 'Listing.Price.ClosePrice'")
if 'preu_predit' not in test_data.columns:
    raise ValueError("El fitxer 'resultat_sapigut.csv' no conté la columna 'preu_predit'")
"""

# Concatenar dades
if len(test_data) != len(train_data):
    raise ValueError("Els fitxers 'test_sapigut.csv' i 'resultat_sapigut.csv' no tenen el mateix nombre de files")
data = pd.concat([test_data.reset_index(drop=True), train_data['Listing.Price.ClosePrice'].reset_index(drop=True)], axis=1).fillna(0)

# Extreure valors predits i reals
predicted = data['preu_predit']
actual = data['Listing.Price.ClosePrice']

# Calcular mètriques
mse = mean_squared_error(actual, predicted)
mae = mean_absolute_error(actual, predicted)

# Crear noves columnes
data['absolute_difference'] = abs(data['Listing.Price.ClosePrice'] - data['preu_predit']).abs()  # Diferència absoluta
# Substituir valors 0 o NaN a 'preu_predit' per un valor molt petit per evitar divisió per zero
data['preu_predit'] = data['preu_predit'].replace(0, 1e-10).fillna(1e-10)
data['real_to_predicted_ratio'] = data['Listing.Price.ClosePrice'] / data['preu_predit']

mean_value = data['Listing.Price.ClosePrice'].mean()
print(mean_value)

# Guardar el resultat en un nou fitxer
output_file_path = 'extended_results5.csv'
data.to_csv(output_file_path, index=False)


# Mostrar resultats
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")