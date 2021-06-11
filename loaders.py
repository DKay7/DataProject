import pandas as pd
import os

os.chdir(os.path.dirname(__file__))
data = pd.read_csv("data/International_Astronaut_Database.csv")
