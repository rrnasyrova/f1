import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

def prediction(name, round_num, driver_points, driver_position, constructor_points, constructor_position, driver_wins, driver_age, constructor_wins):
   
    model = joblib.load('ml/model.pkl')

    main = pd.read_csv("ml/f1_data.csv")
    main.drop('Unnamed: 0', axis=1, inplace=True)

    test = main[(main['season'] == 2023) & (main['round'] == round_num)]
    X_test = test.drop(['driver', 'podium', 'circuit_id', 'country', 'nationality', 'constructor'], axis=1)
    X_test.loc[len(X_test)] = [2023, round_num, driver_points, driver_wins, driver_position, constructor_points, constructor_wins, constructor_position, driver_age]
    y_test = test.podium
    y_test.loc[len(y_test)] = driver_position

    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)
    X_test = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    pred = pd.DataFrame(model.predict(X_test), columns = ['results'])
    pred['podium'] = y_test.reset_index(drop = True)
    pred['actual'] = pred.podium
    pred.sort_values('results', ascending = True, inplace = True)
    pred.reset_index(inplace = True, drop = True)
    pred['predicted'] = pred.index
    pred['predicted'] = pred.predicted.map(lambda x: 1 if x == 0 else x+1)
    
    result = pred.loc[pred['podium'] == driver_position, 'predicted'].iloc[0]

    return int(result)