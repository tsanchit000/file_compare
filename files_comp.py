import pandas as pd

# Load the CSV files
file1_path = '/Users/sanchittiwari/Downloads/bw_gross_2_july.csv'  # Replace with your actual file path
file2_path = '/Users/sanchittiwari/Downloads/feed_gross_2_july.csv'  # Replace with your actual file path
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Ensure column names are correct and consistent
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Drop duplicates in file 1 based on the combination of 'JRCreateDate', 'SAP GL Code', and 'SOD CODE DESCRIPTION'
unique_combinations = df1.drop_duplicates(subset=['JRCreateDate', 'SAP GL Code', 'SOD CODE DESCRIPTION'])

# Group by 'SAP GL Code' and aggregate descriptions in file 1
grouped = unique_combinations.groupby('SAP GL Code')['SOD CODE DESCRIPTION'].apply(list).reset_index()

# Ensure column names are consistent in file 2
df2.rename(columns={'SAP GL Cod': 'SAP GL Code'}, inplace=True)

# Check if each description for each GL Code in file 1 is present in file 2
results = []

for index, row in grouped.iterrows():
    gl_code = row['SAP GL Code']
    descriptions = row['SOD CODE DESCRIPTION']
    for desc in descriptions:
        if not ((df2['SAP GL Code'] == gl_code) & (df2['SOD CODE DESCRIPTION'] == desc)).any():
            results.append((gl_code, desc))

# Display the results
if results:
    print("GL Codes with description mismatches (not present in the second file):")
    for gl_code, desc in results:
        print(f"GL Code: {gl_code}, Description: {desc}")
else:
    print("All descriptions are present in the second file.")