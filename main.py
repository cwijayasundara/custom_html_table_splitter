from json_loader import load_json_file
from bs4 import BeautifulSoup

file_name = "docs/complex_table_json.json"

data_in_json = load_json_file(file_name)

html_text = data_in_json["content"]


def extract_html_parts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the header
    header = soup.header

    # Extract the main content
    main_content = soup.main

    # Remove the outer table but keep its content
    outer_table = main_content.table
    inner_content = outer_table.find('td').decode_contents()

    # Parse the inner content
    inner_soup = BeautifulSoup(inner_content, 'html.parser')

    # Extract the first level inner table
    first_level_inner_table = inner_soup.table

    rows = []
    for row in first_level_inner_table.find_all('tr')[1:]:  # Skip the header row
        row_data = []
        for cell in row.find_all('td'):
            if cell.table:
                # If the cell contains a table, extract its contents
                cell_content = cell.table.decode_contents()
            else:
                cell_content = cell.get_text(strip=True)
            row_data.append(cell_content)
        rows.append(row_data)

    return header, rows


header, inner_table_rows = extract_html_parts(html_text)

print("Header:")
print(header.prettify())

print("\nInner Table Rows:")
for row in inner_table_rows:
    print(row)
