"""
To run everything. I am adding comments so you guys can see what does what , at least according to
me and then make changes in the main file and any subsequent changes you need to make.
"""
from shortest_path_calculator import gets_original_gives_full_path, only_2_points
from mapping import mapping_on_maps_multiple, mapping_on_maps_singular
Graph = __import__("Graph & Node").Graph
load_graph = __import__("Graph & Node").load_graph

g = load_graph('data/chicago_dataset_2.csv')
end = 'Kinzie'
visitor = ['26th', '18TH', 'Indianapolis', 'Indiana', 'Michigan', 'Peterson', '75th', '96th']
start = '1550 West'
full_path = gets_original_gives_full_path(g, start, end, visitor)  # Gives the full shortest path
# between start and end which goes through the locations mentioned in visitor.
path = only_2_points(g, start, end)  # Gives the full shortest path between start and end , here we
# don't have a visitor parameter.
mapping_on_maps_multiple(g, full_path)  # Two map functions so that on the webbrowser it opens two
# files.
mapping_on_maps_singular(g, path)  # In the actual main file we would need to add Kaartik's plotly
# function and we'd be good I think.
