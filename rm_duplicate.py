import pandas as pd

def remove_duplicate_rows(csv_file, output_file):
    """
    Removes duplicate rows from a CSV file and saves the cleaned data to a new CSV file.

    Args:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
    """
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='latin1')

    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    final_rows = len(df)
    removed_rows = initial_rows - final_rows

    if removed_rows > 0:
        print(f"Removed {removed_rows} duplicate rows.")
    else:
        print("No duplicate rows found.")

    df.to_csv(output_file, encoding='utf-8', index=False)
    print(f"Cleaned data saved to {output_file}")

# Example usage:
remove_duplicate_rows(r'C:\Users\victo\Desktop\CS\Job\categ\snippet_event.csv', 'cleaned_snippet_event.csv')
