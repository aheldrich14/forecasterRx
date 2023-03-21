import demand_forecasting.data as data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import plotly.express as px
import plotly.graph_objects as go

from gluonts.dataset.hierarchical import HierarchicalTimeSeries
from gluonts.mx.model.deepvar_hierarchical import DeepVARHierarchicalEstimator
from gluonts.mx.trainer import Trainer
from gluonts.model.predictor import Predictor
from gluonts.dataset.util import to_pandas

MODEL_FOLDER = "demand_forecasting/models"


def load_predictor():

    predictor = Predictor.deserialize(pathlib.Path(MODEL_FOLDER))

    return predictor


def generate_forecast():
    predictions = []
    S = data.load_s_mat()
    predictor = load_predictor()
    bottom_lvl = data.load_bottom_lvl_data()
    col_idx = data.load_column_indices()

    for i in range(10, 0, -1):
        hts = HierarchicalTimeSeries(
            ts_at_bottom_level=bottom_lvl[:-i],
            S=S,
        )
        forecast = next(predictor.predict(hts.to_dataset()))
        percentiles = [5, 25, 50, 75, 95]
        preds = pd.DataFrame(
            np.percentile(forecast.samples[:, 0, :], q=percentiles, axis=0).T,
            columns=percentiles,
        )
        preds["time"] = 36 - i
        preds["series"] = preds.index.map(col_idx)
        preds[percentiles] = preds[percentiles].clip(lower=0)
        predictions.append(preds)

    return pd.concat(predictions)
