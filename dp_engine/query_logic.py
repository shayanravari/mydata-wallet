import pandas as pd
from pydp.algorithms.laplacian import Count

def count_receipts_over_amount(data_path: str, epsilon: float, threshold: float) -> int:
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        return {"error": "Data not found"}

    relevant_data = (df['amount'] > threshold).astype(int).tolist() # list of 0s and 1s
    dp_count_obj = Count(epsilon=epsilon)
    noisy_count = dp_count_obj.quick_result(relevant_data)
    return noisy_count