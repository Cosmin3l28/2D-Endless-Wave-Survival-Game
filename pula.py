import csv
from support import import_csv_layout

# File path
file_path = 'C:/Users/cosmi/Desktop/new_game/graphics/map_layer3.csv'

# Create an empty 40x40 matrix
imported_map = [['-1' for _ in range(41)] for _ in range(40)]

# Modify rows except the first and last 4
for i in range(0, 40):
    for j in range(0, 41):
        if i >= 2 and i <= 38:
            if j == 0 or j == 40:
                imported_map[i][j] = '322'

    # Write the modified map to a new CSV file
    new_file_path = 'C:/Users/cosmi/Desktop/new_game/graphics/modified_map_layer3.csv'
    with open(new_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(imported_map)
