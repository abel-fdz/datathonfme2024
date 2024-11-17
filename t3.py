import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Carregar dades
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Filtrar valors no numèrics a 'Postal Code'
train_data = train_data[pd.to_numeric(train_data['Location.Address.PostalCode'], errors='coerce').notna()]
# Convertim a numèric i els que donin error es converteixen en NaN
test_data['Location.Address.PostalCode'] = pd.to_numeric(test_data['Location.Address.PostalCode'], errors='coerce')
# Substituïm els NaN per 9000
test_data['Location.Address.PostalCode'] = test_data['Location.Address.PostalCode'].fillna(9000)

# Eliminar columnes no escencials
columnes = [
    'Characteristics.LotFeatures', 'ImageData.c1c6.summary.bathroom', 
    'ImageData.c1c6.summary.exterior', "ImageData.style.exterior.summary.label",
    "ImageData.c1c6.summary.interior", "ImageData.c1c6.summary.kitchen", 
    "ImageData.features_reso.results", "ImageData.q1q6.summary.bathroom",
    "ImageData.q1q6.summary.exterior", "ImageData.q1q6.summary.interior", 
    "ImageData.q1q6.summary.kitchen", "ImageData.room_type_reso.results", 
    "Listing.Dates.CloseDate", "Location.Address.CensusBlock", 
    "Location.Address.CensusTract", "Location.Address.PostalCodePlus4", 
    "Location.Address.StreetDirectionPrefix", "Location.Address.StreetName", 
    "Location.Address.StreetNumber", "Location.Address.StreetSuffix", 
    "Location.Address.UnitNumber", "Location.Address.UnparsedAddress", 
    "Location.Area.SubdivisionName", "Location.GIS.Latitude", 
    "Location.GIS.Longitude", "Location.School.HighSchoolDistrict", 
    "Structure.Basement", "Structure.BelowGradeFinishedArea",
    "Structure.BelowGradeUnfinishedArea", "Structure.ParkingFeatures", 
    "Structure.Cooling", "UnitTypes.UnitTypeType", 
    "Location.Address.StreetDirectionSuffix"
]

# Eliminar columnes no necessàries
train_data = train_data.drop(columns=columnes + ["Listing.ListingId"], errors='ignore')
test_data = test_data.drop(columns=columnes, errors='ignore')

# Eliminar columnes buides
train_data = train_data.dropna(axis=1, how='all')
test_data = test_data.dropna(axis=1, how='all')

# Seleccionar columnes rellevants
numeric_features = [
    "Characteristics.LotSizeSquareFeet", "ImageData.c1c6.summary.property", 
    "ImageData.q1q6.summary.property", "Location.Address.PostalCode", 
    "Structure.BathroomsFull", "Structure.BathroomsHalf",
    "Structure.FireplacesTotal", "Structure.GarageSpaces", 
    "Structure.LivingArea", "Structure.Rooms.RoomsTotal", "Structure.YearBuilt"
]

categorical_features = [
    "ImageData.style.stories.summary.label", "Location.Address.City", 
    "Location.Address.CountyOrParish", "Property.PropertyType", 
    "Structure.Cooling", "Structure.Heating", 
    "Structure.NewConstructionYN", "Tax.Zoning"
]

# Processar dades
numeric_features = [col for col in numeric_features if col in train_data.columns]
categorical_features = [col for col in categorical_features if col in train_data.columns]

train_categoric = pd.get_dummies(train_data[categorical_features], drop_first=True)
test_categoric = pd.get_dummies(test_data[categorical_features], drop_first=True)

common_columns = train_categoric.columns.intersection(test_categoric.columns)
train_categoric = train_categoric[common_columns]
test_categoric = test_categoric[common_columns]

# En lloc de .fillna(0), utilitzem .fillna() amb el mètode 'mean' per cada columna
X_train = pd.concat([train_data[numeric_features], train_categoric], axis=1)
X_test = pd.concat([test_data[numeric_features], test_categoric], axis=1)

# Calcular la mitjana de les columnes numèriques del training set
column_means = X_train[numeric_features].mean()

# Aplicar la mitjana als valors nuls
X_train[numeric_features] = X_train[numeric_features].fillna(column_means)
X_test[numeric_features] = X_test[numeric_features].fillna(column_means)

# Les columnes categòriques (one-hot encoded) mantenen el 0 com a valor per defecte
X_train[train_categoric.columns] = X_train[train_categoric.columns].fillna(0)
X_test[test_categoric.columns] = X_test[test_categoric.columns].fillna(0)

y_train = train_data['Listing.Price.ClosePrice']

# Entrenar el model
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Prediccions
predictions = model.predict(X_test)

# Crear dataframe de resultats
results_df = pd.DataFrame({
    'Listing.ListingId': test_data['Listing.ListingId'],
    'Listing.Price.ClosePrice': predictions
})

# Guardar a CSV
results_df.to_csv('resultat1.csv', index=False)