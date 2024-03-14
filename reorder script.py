# Read the data from the provided text
with open("\%fakepath%\elo_rankings.txt", "r") as file: #replace fakepath with your destination folder. 
    data = file.readlines()

# Define a function to extract the four digits from the filename
def extract_digits(line):
    return int(line.split(":")[-1])

# Sort the data based on the four digits
sorted_data = sorted(data, key=extract_digits)

# Write the sorted data to a new file
with open("sorted_data.txt", "w") as file: #creates and writes to a file in the script directory. I advise putting the script in its own folder in case stuff gets mixed up.) 
    file.writelines(sorted_data)
