import pandas as pd
import os

def load_aci_data():
    base_path = os.path.dirname(__file__)  # <-- directory corrente, cioè utils/
    data_path = os.path.join(base_path, "..", "data", "fringe_benefit_2025.csv")
    data_path = os.path.normpath(data_path)  # pulisce il percorso per Windows/Linux
    fringe_data = pd.read_csv(data_path)
    fringe_data = fringe_data.dropna()
    return fringe_data
