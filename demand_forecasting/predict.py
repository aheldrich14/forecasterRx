import demand_forecasting.data as data
import numpy as np
import pandas as pd
import pathlib

from gluonts.dataset.hierarchical import HierarchicalTimeSeries
from gluonts.model.predictor import Predictor

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
            np.percentile(
                forecast.samples[:, 0, :],
                q=percentiles,
                axis=0,
            ).T,
            columns=percentiles,
        )
        preds["time"] = 36 - i
        preds["series"] = preds.index.map(col_idx)
        preds[percentiles] = preds[percentiles].clip(lower=0)
        predictions.append(preds)

    return pd.concat(predictions)


def get_hierarchy_str(region, reason):
    if region is None:
        if reason is None:
            series = "Total"
        else:
            series = reason
    else:
        if reason is None:
            series = region
        else:
            series = f"{region} - {reason.lower()}"
    return series


def calc_total_usage(
    prediction_df,
    region,
    reason,
    percentile,
):
    series = get_hierarchy_str(region, reason)
    filtered_preds = prediction_df[prediction_df["series"] == series]
    usage = filtered_preds[percentile].cumsum().round().astype(int)
    return usage
