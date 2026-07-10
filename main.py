# python libraries
import pandas as pd
from pathlib import Path

# .py files
from clean_data import filter_quality_hitters
from model import create_model_csv

def main():
    create_model_csv()

if __name__ == "__main__":
    main()