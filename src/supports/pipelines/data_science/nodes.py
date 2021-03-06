# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""
# pylint: disable=invalid-name

from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report


def train_model(
    train_x: pd.DataFrame, train_y: pd.DataFrame, parameters: Dict[str, Any]
) -> np.ndarray:
    """Node for training a simple multi-class logistic regression model. The
    number of training iterations as well as the learning rate are taken from
    conf/project/parameters.yml. All of the data as well as the parameters
    will be provided to this function at the time of execution.
    """
    seed = parameters["sklearn_model_seed"]
    criterion = parameters["sklearn_model_criterion"]
    max_leaf_nodes = parameters["sklearn_model_max_leaf_nodes"]
    x_train = train_x.to_numpy()
    y_train = train_y.to_numpy()

    model = DecisionTreeClassifier(criterion, random_state=seed, max_leaf_nodes=max_leaf_nodes)
    model.fit(x_train, y_train)

    # Return a joint multi-class model with weights for all classes
    return model


def predict(model: DecisionTreeClassifier, test_x: pd.DataFrame) -> np.ndarray:
    """Node for making predictions given a pre-trained model and a test set.
    """
    x_test = test_x.to_numpy()
    predictions = model.predict(x_test)

    # Return the index of the class with max probability for all samples
    return predictions


def report_accuracy(predictions: np.ndarray, test_y: pd.DataFrame) -> pd.DataFrame:
    """Node for reporting the accuracy of the predictions performed by the
    previous node. Notice that this function has no outputs, except logging.
    """
    report = classification_report(test_y, predictions, output_dict=True, digits=5)
    avg_logs = pd.DataFrame.from_dict(
        report, orient="index"
    ).T
    return avg_logs


def save_trained_model(model: DecisionTreeClassifier) -> DecisionTreeClassifier:
    return model


def _sigmoid(z):
    """A helper sigmoid function used by the training and the scoring nodes."""
    return 1 / (1 + np.exp(-z))
