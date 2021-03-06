# noqa: D100
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_is_fitted
from sklearn.utils.validation import check_array
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import LabelEncoder


class OneNearestNeighbor(BaseEstimator, ClassifierMixin):
    """One Nearest Neighbor model."""

    def __init__(self):  # noqa: D107
        pass

    def fit(self, X, y):
        """Train the model.
        Parameters
        ----------
        X : training np.array of observations
        y : training np.array of labels

        Returns
        -------
        self : fitted model"""
        X, y = check_X_y(X, y)
        X = check_array(X, copy=True, ensure_2d=True)
        self.classes_ = np.unique(y)
        # If more than 50 classes, this is probably a regression and not a classification.
        if len(self.classes_) > 50:  # scientific number
            # sklearn wants us to have this error message start with "Unknwon label type: "
            raise ValueError("Unknown label type: too many classes for classification")
        try:
            y = check_array(
                y, ensure_2d=False, copy=True, dtype="numeric", force_all_finite=False
            )
        except ValueError:
            y = check_array(
                y, ensure_2d=False, copy=True, dtype=np.object, force_all_finite=False
            )

        self.obs_ = X
        self.labels_ = y
        return self

    def predict(self, X):
        """Perform predictions using the model.
        Parameters
        ----------
        X : np.array of observations

        Returns@tommoral my OneNearestNeighbo
        -------
        y_pred : np.array of predictions
        """
        check_is_fitted(self)
        X = check_array(X)
        # y_pred = np.full(shape=len(X), fill_value=self.classes_[0])
        sim_matrix = pairwise_distances(X, self.obs_)
        index_min_sim = np.argmin(sim_matrix, axis=1)
        y_pred = self.labels_[index_min_sim]
        return y_pred

    def score(self, X, y):
        """
        Parameters
        ----------
        X : test np.array of observations
        y : test np.array of labels

        Returns
        -------
        score : accuracy
        """
        X, y = check_X_y(X, y)
        y_pred = self.predict(X)
        return np.mean(y_pred == y)
