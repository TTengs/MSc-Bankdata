import csv
import random

# Function to calculate random interest rate
def calculate_interest():
    return round(random.uniform(0.01, 0.05), 2)

# Input and output file paths
input_file = 'springDemo/src/main/resources/data.csv'
output_file = 'data_with_interest.csv'

# Open input and output files
with open(input_file, 'r') as csv_file, open(output_file, 'w', newline='') as output_csv:
    reader = csv.reader(csv_file)
    writer = csv.writer(output_csv)

    # Write headers to the output file
    headers = next(reader)
    headers.append('interest')
    writer.writerow(headers)

    # Process each row
    for row in reader:
        # Calculate random interest
        interest = calculate_interest()
        
        # Append interest to the row
        row.append(interest)
        
        # Write the updated row to the output file
        writer.writerow(row)

print("Interest added successfully!")
