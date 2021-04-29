import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

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


def cramers_corrected_stat(confusion_matrix):
    """ calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher,
        Journal of the Korean Statistical Society 42 (2013): 323-328
    """
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))


def get_cramers_v_correlation_matrix(X):
    X_columns = X.columns
    n_cols = len(X_columns)

    coefficients = np.zeros(shape=(n_cols, n_cols))
    for i in range(n_cols):
        for j in range(n_cols):
            coefficients[i, j] = cramers_corrected_stat(pd.crosstab(X[X_columns[i]], X[X_columns[j]]))
    return coefficients


def plot_cramers_v_correlation_matrix(X):
    corr_matrix = get_cramers_v_correlation_matrix(X)

    cols = X.columns
    fig, ax = plt.subplots(1, 1)
    img = ax.imshow(corr_matrix, alpha=0.8, cmap='OrRd')
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=90)
    ax.set_yticklabels(cols)
    fig.colorbar(img)
    return