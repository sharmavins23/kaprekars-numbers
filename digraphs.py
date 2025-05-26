import graphviz
from itertools import product
import shutil
import os
import time


def kaprekars_routine(n: int, k: int) -> int:
    """
    Perform one iteration of Kaprekar's routine on a number n with k digits.

    Args:
        n (int): The input number.
        k (int): The number of digits in the number.

    Returns:
        int: The next number in Kaprekar's routine.
    """
    # Convert the number to a string and pad with zeros to ensure consistent digit count
    digits = sorted(str(n).zfill(k))

    # Form the smallest and largest numbers
    smallest = int("".join(digits))
    largest = int("".join(digits[::-1]))

    # Return the result of subtracting the smallest from the largest
    return largest - smallest


def create_kaprekar_digraph(k: int) -> None:
    """
    Creates and saves a digraph visualization of Kaprekar's routine for k-digit numbers.
    Iterates through every number between 0 and 10^k - 1 (inclusive).
    Also saves the directed graph as a text file.

    Args:
        k (int): Number of digits in the numbers to analyze
    """

    # Create a new directed graph with layout engine and spacing attributes
    dot = graphviz.Digraph(
        comment=f'Kaprekar\'s Routine for {k}-digit numbers',
        engine='neato'
    )

    # Adjust graph attributes to reduce overlap
    dot.graph_attr.update({
        'overlap': 'false',  # Prevent node overlap
        'sep': '1',          # Increase separation between nodes
        'nodesep': '1',      # Minimum space between nodes
        'ranksep': '2',      # Minimum space between ranks (if hierarchical)
    })

    # Prepare a list to store edges for the text file
    edges = []

    # Iterate through every number from 0 to 10^k - 1
    for n in range(10**k):
        result = kaprekars_routine(n, k)  # Apply Kaprekar's routine
        dot.node(str(n))  # Create a node for the current number
        dot.node(str(result))  # Create a node for the result
        dot.edge(str(n), str(result))  # Create an edge from n to result
        edges.append(f"{n} -> {result}")  # Add edge to the list

    # Create img directory if it doesn't exist
    os.makedirs('img/digraphs', exist_ok=True)

    # Save the graph as a PNG file
    dot.render(f'img/digraphs/digraph_{k}', format='png', cleanup=True)

    # Save the edges as a text file
    with open(f'img/digraphs/digraph_{k}.txt', 'w') as f:
        f.write("\n".join(edges))

    print(f"Directed graph for {k}-digit numbers saved as PNG and TXT.")


if __name__ == "__main__":
    # Define the directory to clean
    output_dir = 'img/digraphs/'

    # Delete everything in the directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    print(f"Deleted contents of {output_dir}.")

    # Recreate the directory
    os.makedirs(output_dir, exist_ok=True)

    # Create digraphs for all numbers from 2 to k digits
    for k in range(2, 4):
        startTime = time.time()
        create_kaprekar_digraph(k)
        endTime = time.time()
        print(
            f"Created digraph for {k}-digit numbers in {endTime - startTime:.2f} seconds.")
