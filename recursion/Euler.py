from utils import plot_all_routes, get_setup

for i in range(5, 6):
    G, E = get_setup(i)
    plot_all_routes(G, E, "./pictures")
