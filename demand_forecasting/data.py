"""Data loading functions."""

import json

import numpy as np
import pandas as pd

DATA_FOLDER = "demand_forecasting/data"
DATA_FILE_STR = "data.csv"
ALL_DATA_FILE_STR = "all_data.csv"
S_MAT_STR = "S.csv"
COL_IDX_STR = "column_idx.json"


def load_bottom_lvl_data() -> pd.DataFrame:
    """Load csv file of bottom level series."""
    data = pd.read_csv(f"{DATA_FOLDER}/{DATA_FILE_STR}", index_col=0)
    idx = pd.PeriodIndex(pd.date_range(start="2008-01-01", freq="M", periods=len(data)))
    data.index = idx

    return data


def load_all_data() -> pd.DataFrame:
    """Load csv file of all data."""
    data = pd.read_csv(f"{DATA_FOLDER}/{ALL_DATA_FILE_STR}", index_col=0)

    return data


def load_s_mat() -> np.array:
    """Load S matrix data that indicates hieracrhy membership."""
    S = pd.read_csv(f"{DATA_FOLDER}/{S_MAT_STR}", header=None)

    return S.to_numpy()


def load_column_indices() -> dict:
    """Load column name index."""
    with open(f"{DATA_FOLDER}/{COL_IDX_STR}") as f:
        col_idx = json.load(f)
    # return reversed dictionary
    return {v: k for k, v in col_idx.items()}
