from collections import defaultdict


class Graph:
    """
    A class to represent an undirected multigraph. The graph is represented as
    a dictionary of lists. Each key in the dictionary represents a vertex, and
    the corresponding value is a list of tuples. Each tuple represents an edge
    and contains the vertex it is connected to, and the label of the edge.
    """

    def __init__(self):
        self.graph = defaultdict(list)
        self.num_edges = 0
        self.euler_paths = []

    def add_edge(self, current_node, next_node, edge):
        """Add an edge to the graph."""
        self.graph[current_node].append((next_node, edge))
        self.graph[next_node].append((current_node, edge))
        self.num_edges += 1

    def find_euler_paths(self):
        """
        Given a undirected multigraph, find all possible Euler paths. An Euler
        path is a path that visits every edge exactly once. A Euler path exists
        only if there are exactly 0 or 2 odd degree nodes. If there are no odd
        degree nodes, then all nodes are starting nodes. If there are two odd
        degree nodes, then they are the starting and ending nodes.
        """
        # Find all nodes in the graph with an odd degree.
        odd_degree_nodes = [
            vertex for vertex in self.graph if len(self.graph[vertex]) % 2 != 0
        ]

        # An Euler path exists only if there are exactly 0 or 2 odd degree nodes.
        if len(odd_degree_nodes) != 0 and len(odd_degree_nodes) != 2:
            print("Euler path does not exist")
        else:
            # If there are no odd degree nodes, add all nodes as starting nodes.
            start_nodes = (
                odd_degree_nodes if odd_degree_nodes else list(self.graph.keys())
            )

            # Find all Euler paths from each starting node.
            for start in start_nodes:
                self.generate_euler_paths(start)

    def is_bridge(self, current_node, next_node, edge):
        """
        Check if an edge is a bridge in the graph. A bridge is an edge that,
        if removed, would isolate two parts of the graph. To check this, we
        employ a DFS to count the number of reachable nodes from the current
        node, remove the edge, and check if the number of reachable nodes has
        changed. If it has, the edge is a bridge.

        Args:
            current_node: The current node that is connected to one side of the edge.
            next_node: The node that is being explored to, connected to the other side of the edge.
            edge: The edge connecting current_node and next_node.

        Returns:
            True if the edge is a bridge, False otherwise.
        """

        # A set to keep track of visited nodes during DFS.
        visited = set()

        # A function to execute DFS from a starting node and count reachable nodes.
        def dfs(node):
            visited.add(node)
            for next_node, _ in self.graph[node]:
                if next_node not in visited:
                    dfs(next_node)

        # Find the number of reachable nodes from the current node.
        dfs(current_node)
        count_before = len(visited)

        # Remove the edge from the graph
        self.graph[current_node].remove((current_node, edge))
        self.graph[next_node].remove((next_node, edge))

        # Find the number of reachable nodes from the current node with the
        # edge removed.
        visited = set()
        visited.add(current_node)
        dfs(next_node)
        count_after = len(visited)

        # Add back in the edge to the graph.
        self.graph[current_node].append((next_node, edge))
        self.graph[next_node].append((next, edge))

        # If the counts are different, removing the edge has reduced
        # reachability, indicating it is a bridge.
        return count_before > count_after

    def generate_euler_paths(self, start):
        """
        Generate all possible Euler paths from a starting node. This is done
        using backtracking. The algorithm is as follows:
        1. Begin the path with a starting node.
        2. Loop through all connected edges of the current node.
        3. If the edge has already been explored, or is a bridge, don't "walk it".
        4. Otherwise, add it to the path, and mark it as used.
        5. After walking the edge, we are at a new node. Recursively call the
              function on the new node.
        6. If we find ourselves with a path containing all edges, add it to the
                list of Euler paths.
        7. If we have reached a dead end, remove the edge from the path and mark
                it as unused. This is the backtracking step where we "walk back"
                the edge.

        Args:
            start: The starting node.
        """

        def backtrack(path, current_node, used_edges):
            # If the current path contains all edges, add it to the list of Euler paths.
            if len(path) == self.num_edges + 1:
                self.euler_paths.append(path)
                return

            # Loop through the connected edges of the current node.
            for next_node, edge_name in self.graph[current_node]:
                # Keep track of the edge and its reverse. In the current data
                # structure, the reverse edge is the same edge, but with the
                # nodes swapped. For example, vertex A connected to vertex B
                # with edge_name C is the same edge as vertex B connected to vertex
                # A with edge_name C.
                edge = (current_node, next_node, edge_name)
                reverse_edge = (next_node, current_node, edge_name)

                # If the edge has already been explored, or is a bridge, don't
                # "walk it".
                if (
                    edge in used_edges
                    or reverse_edge in used_edges
                    and self.is_bridge(current_node, next_node, edge_name)
                ):
                    continue

                # Otherwise, add it to the path, and mark it as used.
                path.append(f"{next_node} (via {edge_name})")
                used_edges.add(edge)
                used_edges.add(reverse_edge)

                # After walking the edge, we are at a new node. Recursively
                # call the function on the new node.
                backtrack(path.copy(), next_node, used_edges.copy())

                # Once the recursive call returns, remove the edge from the path
                # and mark it as unused. This is the backtracking step where we
                # "walk back" the edge.
                used_edges.remove(edge)
                used_edges.remove(reverse_edge)
                path.pop()

        # Start the backtracking algorithm with the initial path containing
        # only the starting node.
        initial_path = [f"{start}"]
        backtrack(initial_path, start, set())


# Helper function to extract the identical paths from the two lists of euler paths.
def find_matching_sequences(list1, list2):
    def extract_via_sequence(sublist):
        # Extract the 'via' sequences, capturing only the edge names
        sequence = [
            item.split("via ")[1].strip("()") for item in sublist if "via" in item
        ]
        return sequence

    # Extract the 'via' sequences from each sublist in both lists
    sequences_list1 = [extract_via_sequence(sublist) for sublist in list1]
    sequences_list2 = [extract_via_sequence(sublist) for sublist in list2]

    # Find sequences that exist in both lists
    common_sequences = set(tuple(seq) for seq in sequences_list1) & set(
        tuple(seq) for seq in sequences_list2
    )

    return common_sequences


# Example usage:
if __name__ == "__main__":
    # Simple Circuit

    # Pull up network
    pull_up_network = Graph()

    # The first two arguements are the nodes that the MOSFET is connected
    # to. The third arguement is the name of the MOSFET. In this case,
    # the MOSFET is named "C" and is connected to nodes "Z" and "VDD".
    pull_up_network.add_edge("Z", "VDD", "C")
    pull_up_network.add_edge("VDD", "AB", "A")
    pull_up_network.add_edge("AB", "Z", "B")

    pull_up_network.find_euler_paths()

    # Pull down network
    pull_down_network = Graph()

    pull_down_network.add_edge("AB", "Z", "C")
    pull_down_network.add_edge("AB", "GND", "A")
    pull_down_network.add_edge("AB", "GND", "B")

    pull_down_network.find_euler_paths()

    poly_orderings = find_matching_sequences(
        pull_up_network.euler_paths, pull_down_network.euler_paths
    )
    print("Poly orderings for simple circuit: \n", poly_orderings)

    # More Complex Circuit

    # Pull up network
    pull_up_network = Graph()

    pull_up_network.add_edge("Z", "AB", "A")
    pull_up_network.add_edge("AB", "BCD", "B")
    pull_up_network.add_edge("BCD", "VDD", "C")
    pull_up_network.add_edge("BCD", "VDD", "D")

    pull_up_network.find_euler_paths()

    # Pull down network
    pull_down_network = Graph()

    pull_down_network.add_edge("Z", "GND", "A")
    pull_down_network.add_edge("Z", "GND", "B")
    pull_down_network.add_edge("Z", "CD", "C")
    pull_down_network.add_edge("GND", "CD", "D")

    pull_down_network.find_euler_paths()

    poly_orderings = find_matching_sequences(
        pull_up_network.euler_paths, pull_down_network.euler_paths
    )
    print("Poly orderings for complex circuit: \n", poly_orderings)
