import networkx as nx
import numpy as np
import pandas as pd
import json
import smopy
import matplotlib.pyplot as plt
%matplotlib inline
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = mpl.rcParams['savefig.dpi'] = 300

g = nx.read_shp("data/tl_2013_06_prisecroads.shp")
sg = list(nx.connected_component_subgraphs(g.to_undirected()))[0]
#len(sg)
