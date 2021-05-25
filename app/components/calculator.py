import pickle


def calculate_price(form_components):
    values_dict = {}
    all_children = form_components[0]['props']['children']
    for child in all_children:
        try:
            key = child['props']['children'][1]['props']['id'].replace('input_', '')
            value = child['props']['children'][1]['props']['value']
            values_dict[key] = [value]
        except:
            pass
    import pandas as pd
    df = pd.DataFrame.from_dict(values_dict)
    # Check if all fields are filled up
    if len(df.columns) < 19:
        print(df.columns)
        return -1
    # Check if columns are filled
    buy_or_rent = df['buy_or_rent'].values[0]
    sqm = df['sqm'].values[0]
    df.drop(columns=['buy_or_rent', 'sqm'], inplace=True)
    if buy_or_rent == 'buy':
        # Load buy model
        with open('../data/models/model_buy.model', 'rb') as pickle_file:
            model = pickle.load(pickle_file)
        with open('../data/models/model_buy_columns.pkl', 'rb') as pickle_file:
            model_cols = pickle.load(pickle_file)
    elif buy_or_rent == 'rent':
        with open('../data/models/model_rent.model', 'rb') as pickle_file:
            model = pickle.load(pickle_file)
        with open('../data/models/model_rent_columns.pkl', 'rb') as pickle_file:
            model_cols = pickle.load(pickle_file)

    df = pd.get_dummies(df)
    # Adjust columns
    for col in model_cols:
        if col not in df.columns:
            df[col] = 0
    price = model.predict(df[model_cols])[0]*sqm
    return price
