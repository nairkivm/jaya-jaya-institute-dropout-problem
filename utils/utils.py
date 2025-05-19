import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..'
        )
    )
)

from utils.constants import Constants

class DataUtils(Constants):
    
    def asses_data(self, df: pd.DataFrame, table_name : str):
        # Initialize the requirements
        requirements = self.requirements
        print(f"Data Assessment for '{table_name}':")
        # Check data shape
        print(" > Data shape: ", df.shape)
        # Check unnecessary columns
        unnecessary_columns = [_col for _col in df.columns if _col not in requirements[table_name].keys()]
        if len(unnecessary_columns) > 0:
            print(" > Columns that should be dropped:")
            for i in range(len(unnecessary_columns)):
                print(f"      {i+1:0>2}. {unnecessary_columns[i]}")
        else:
            print(" > No column should be dropped v")
        # Check missing columns
        missing_columns = [_col for _col in requirements[table_name].keys() if _col not in df.columns]
        if len(missing_columns) > 0:
            print(" > Columns that should have exist:")
            for i in range(len(missing_columns)):
                print(f"      {i+1:0>2}. {missing_columns[i]}")
        else:
            print(" > All requirements columns are exists v")
        # Check available columns
        available_columns = [_col for _col in requirements[table_name].keys() if _col in df.columns]
        # Check mismatch data type columns
        mismatch_columns = {
            _col: _type for _col, _type in df[available_columns].dtypes.to_dict().items()
            if str(_type) != requirements[table_name][_col]
        }
        if len(available_columns) == 0:
            print(" > No column matches the requirements!")
        elif len(mismatch_columns) > 0:
            print(" > Mismatch type columns:")
            i = 0
            for _col, _type in mismatch_columns.items():
                print(f"      {i+1:0>2}. '{_col}' column should be in '{requirements[table_name][_col]}' (original: {str(_type)})!")
                i += 1
        else:
            print(" > All column types match the requirements v")
        # Check missing values
        missing_values_columns = {
            _col: _miss_count for _col, _miss_count in df[available_columns].isna().sum().to_dict().items()
            if _miss_count > 0
        }
        if len(missing_values_columns) > 0:
            print(" > Missing value columns:")
            for _col, _miss_count in missing_values_columns.items():
                print(f"      - {_col:<20} column : {_miss_count/df.shape[0]:.2%} ({_miss_count:<4})")
        else:
            print(" > There is no missing value columns v")
        # Check duplicated data
        duplicated_data_count = df.duplicated(keep=False).sum()
        if duplicated_data_count > 0:
            print(" > Duplicated data count: ", duplicated_data_count)
        else:
            print(" > There is no duplicated data v")
        # Check outlier
        numerical_columns = [_col for _col in available_columns if requirements[table_name][_col] in ['int64', 'float64']]
        if numerical_columns:
            chunk_size = 5
            num_chunks = ceil(len(numerical_columns) / chunk_size)
            
            for chunk_index in range(num_chunks):
                chunk = numerical_columns[chunk_index * chunk_size:(chunk_index + 1) * chunk_size]
                fig, axes = plt.subplots(nrows=len(chunk), ncols=1, figsize=(10, 10 * len(chunk) / chunk_size))
                
                if len(chunk) == 1:
                    axes = [axes]  # Ensure axes is iterable when there's only one subplot
                
                for i, col in enumerate(chunk):
                    df.boxplot(column=[col], ax=axes[i], vert=False)
                    axes[i].set_title(f'Box plot of {col}')
                    axes[i].set_yticklabels([col], rotation=90, va='center')
                
                plt.tight_layout()
                plt.show()
        
            # Generate histograms in batches of 3x3
            hist_chunk_size = 9
            hist_num_chunks = ceil(len(numerical_columns) / hist_chunk_size)
            
            for hist_chunk_index in range(hist_num_chunks):
                hist_chunk = numerical_columns[hist_chunk_index * hist_chunk_size:(hist_chunk_index + 1) * hist_chunk_size]
                fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))
                axes = axes.flatten()  # Flatten the 3x3 grid for easier iteration
                
                for i, col in enumerate(hist_chunk):
                    df[col].hist(ax=axes[i], bins=20, color='skyblue', edgecolor='black')
                    axes[i].set_title(f'Histogram of {col}')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('Frequency')
                
                # Hide unused subplots
                for j in range(len(hist_chunk), len(axes)):
                    fig.delaxes(axes[j])
                
                plt.tight_layout()
                plt.show()
                
        else:
            print(" > There is no available data to examine the outliers")
    