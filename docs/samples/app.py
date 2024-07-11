from bs4 import BeautifulSoup


# Function to recursively extract text from cells, including nested tables
def extract_cell_text(cell):
    nested_table = cell.find('table')
    if nested_table:
        return extract_table_text(nested_table)
    return cell.get_text(strip=True)


# Function to extract text from a table
def extract_table_text(table):
    rows = table.find_all('tr')
    table_text = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        cell_values = [extract_cell_text(cell) for cell in cells]
        table_text.append(' | '.join(cell_values))
    return ' || '.join(table_text)


# Load the HTML file
file_path = 'inner_table.html'
with open(file_path, 'r') as file:
    content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Find the outer table
outer_table = soup.find('table')

# Extract rows of the outer table
outer_rows = outer_table.find_all('tr', recursive=False)

# Print the header row
header_cells = outer_rows[0].find_all(['th', 'td'])
header_values = [extract_cell_text(cell) for cell in header_cells]
print(header_values)

# Print each row of the outer table including nested tables
for row in outer_rows[1:]:
    cells = row.find_all(['th', 'td'])
    cell_values = [extract_cell_text(cell) for cell in cells]
    print(cell_values)
