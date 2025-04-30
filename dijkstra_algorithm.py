import heapq

def dijkstra(graph, start):
    # graph is an adjacency list: { node: [(neighbor, weight), ...] }
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]
    previous = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous

def reconstruct_path(previous, start, end):
    path = []
    current = end
    while current and current != start:
        path.append(current)
        current = previous[current]
    if current == start:
        path.append(start)
        path.reverse()
        return path
    return []
