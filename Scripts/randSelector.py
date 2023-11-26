import pandas as pd
import os

csv_file = 'E:\\Vscode\\IC\\DataGH\\IAPredictions\\IA_data_all.csv'
csv_out = 'E:\\Vscode\\IC\\DataGH\\IAPredictions\\testedata.csv'

df = pd.read_csv(csv_file)
num = 50

# Check if the DataFrame has at least num rows
if len(df) >= num:
    # Select num random rows from the DataFrame
    random_rows = df.sample(n=num, random_state=42)  # Set a seed for reproducibility (change the seed if needed)

    # Concatenate the first row with the random rows
    output_df = pd.concat([df.iloc[0:1], random_rows])

    # Save the DataFrame to the new CSV file
    output_df.to_csv(csv_out, index=False)

    print(f'{num} random lines saved to {csv_out}')
else:
    print(f'The DataFrame has fewer than {num} rows.')