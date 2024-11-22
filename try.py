import pandas as pd
import glob
import numpy as np
import itertools
import os

new_version = "1.0.123"
current_kg_versions = pd.read_csv("current_kg_version.csv")
current_kg_versions.loc[0] = "1.0.{new_version}".format(
    new_version=new_version)
current_kg_versions.to_csv("current_kg_version.csv", index=False)
