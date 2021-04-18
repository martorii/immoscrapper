import pandas as pd
import numpy as np


def get_sqlalchemy_table_to_pandas(table, db):
    col_names = db.get_columns('properties')
    col_names = [col.name for col in col_names]
    df = pd.DataFrame(db.select_table(table), columns=col_names)
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
