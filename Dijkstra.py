import sys


def shortestpath(graph, start, end, visited, distances, predecessors):
    """
    Find the shortest path between start and end nodes in a graph
    http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/
    """

    # we've found our end node, now find the path to it, and return
    if start == end:
        path = []
        while end:
            path.append(end)
            end = predecessors.get(end, None)
        return distances[start], path[::-1]

    # detect if it's the first time through, set current distance to zero
    if not visited:
        distances[start] = 0

    # process neighbors as per algorithm, keep track of predecessors
    for neighbor in graph[start]:
        if neighbor not in visited:
            neighbordist = distances.get(neighbor, sys.maxint)
            tentativedist = distances[start] + graph[start][neighbor]
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor] = start

    # neighbors processed, now mark the current node as visited
    visited.append(start)

    # finds the closest unvisited node to the start
    unvisiteds = dict((k, distances.get(k, sys.maxint)) for k in graph if k not in visited)
    closestnode = min(unvisiteds, key=unvisiteds.get)

    # now we can take the closest node and recurse, making it current
    return shortestpath(graph, closestnode, end, visited, distances, predecessors)
