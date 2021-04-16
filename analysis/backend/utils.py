import pandas as pd
import numpy as np


def get_sqlalchemy_table_to_pandas(table, db):
    col_names = db.get_columns('properties')
    col_names = [col.name for col in col_names]
    df = pd.DataFrame(db.select_table(table), columns=col_names)
    return df


def drop_unnecessary_columns(df):
    unnecessary_columns = ['property_id', 'title', 'url', 'extraction_date', 'lift', 'security_system']
    df.drop(columns=unnecessary_columns, inplace=True)
    return df


def map_from_value_to_key(row_value, mapper):
    # Everything must be lowcase!
    if row_value is not None:
        row_value_lowercase = row_value.lower()
        for key, value_list in mapper.items():
            if row_value_lowercase in value_list:
                return key
    return np.NAN


def get_dummies_from_categorical(categorical_features, df):
    for categorical_feature in categorical_features:
        # Get one hot encoding of columns 'vehicleType'
        one_hot = pd.get_dummies(df[categorical_feature], prefix=categorical_feature)
        # Drop column as it is now encoded
        df = df.drop(categorical_feature,axis = 1)
        # Join the encoded df
        df = pd.concat([df, one_hot], axis=1)
    return df


def improve_ols(model, X):
    threshold = 0.05
    pvalues_df = pd.DataFrame(model.pvalues, columns=['p_value']).reset_index().rename(columns={'index': 'feature'})
    features_to_delete_df = pvalues_df[pvalues_df.p_value < threshold].sort_values('p_value')
    features_to_delete = features_to_delete_df.feature.values
    deletable_features = X.select_dtypes(include=np.number).columns.tolist()
    empty_df = pd.DataFrame()

    for feature_to_delete in features_to_delete:
        if feature_to_delete in deletable_features:
            X.drop(columns=[feature_to_delete], inplace=True)
            return X, feature_to_delete
    return empty_df, None
