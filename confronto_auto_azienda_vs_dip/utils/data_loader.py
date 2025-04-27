import pandas as pd

def load_aci_data():
    fringe_data = pd.read_csv("data/fringe_benefit_2025.csv")
    fringe_data = fringe_data.dropna()
    return fringe_data
