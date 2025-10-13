# Import the 'random' module to allow random selection of elements from a list
import random

# Define a function that returns a scheduling hint for VM placement
def choose_host_hint():
    # Use random.choice() to randomly select one element from the list
    # Each element represents a different scheduling hint:
    # - {"different_host": "group1"} tells the scheduler to place the VM on a different host than group1
    # - {"same_host": "group1"} tells the scheduler to place the VM on the same host as group1
    # - None means no scheduling hint is provided (default scheduling behavior)
    return random.choice([
        {"different_host": "group1"},
        {"same_host": "group1"},
        None
    ])
