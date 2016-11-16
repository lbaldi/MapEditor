import Dijkstra


def find_shortest_path(graph, start_node, end_node):

    path = Dijkstra.shortestpath(
        graph,
        start_node,
        end_node,
        visited=[],
        distances={},
        predecessors={}
    )

    if path:
        return path[1]
