from sklearn.ensemble import RandomForestRegressor
from utils import *

def compute_wagers(prefinal, final):
    return abs(np.array(prefinal) - np.array(final))

def wagering_data(seasons): #seasons is list of ints
    s_data = load_seasons(seasons)
    if type(seasons) == int:
        s_data = {seasons: s_data}
        
    X = []
    Y = []

#    ipdb.set_trace()
    for s in s_data:
        for g in s_data[s]:
            try:
                prefinal = g['info']['scores']['DJ_round']
                final = g['info']['scores']['final']
                wagers = compute_wagers(prefinal, final)
                scaling_factor = max(prefinal)
                if len(prefinal) == 3 and len(wagers) == 3: #some missing data
                    X.append(np.array(prefinal)/scaling_factor)
                    Y.append(wagers/scaling_factor)
            except:
                print('missing data for game ' + str(g['info']['game_id']))

    X = np.array(X)
    Y = np.array(Y)

    return (X, Y)

def fit_model(X, Y):
    regr = RandomForestRegressor(n_estimators = 100)
    regr.fit(X, Y)
    return regr
