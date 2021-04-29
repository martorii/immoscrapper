from sklearn.metrics import *
from sklearn.model_selection import *


# Genetic algorithm + Logistic Regression
def feature_selection_genetic(estimator, X, Y):
    mcc = make_scorer(matthews_corrcoef)

#     from sklearn.linear_model import LinearRegression
#     estimator = LinearRegression(fit_intercept = True)

    from genetic_selection import GeneticSelectionCV

    report = pd.DataFrame()
    nofeats = []
    chosen_feats = []
    cvscore = []
    rkf = KFold(n_splits = 10)
    for i in range(2, len(X.columns)):

        selector = GeneticSelectionCV(estimator,
                                    cv = rkf,
                                    verbose = 0,
                                    scoring = mcc,
                                    max_features = i,
                                    n_population = 200,
                                    crossover_proba = 0.5,
                                    mutation_proba = 0.2,
                                    n_generations = 10,
                                    crossover_independent_proba=0.5,
                                    mutation_independent_proba=0.05,
                                    #tournament_size = 3,
                                    n_gen_no_change=10,
                                    caching=True,
                                    n_jobs=-1)
        selector = selector.fit(X, Y)
        genfeats = X.columns[selector.support_]
        genfeats = list(genfeats)
        print("Chosen Feats:  ", genfeats)

        cv_score = selector.generation_scores_[-1]
        nofeats.append(len(genfeats))
        chosen_feats.append(genfeats)
        cvscore.append(cv_score)
    report["No of Feats"] = nofeats
    report["Chosen Feats"] = chosen_feats
    report["Scores"] = cvscore
    return report