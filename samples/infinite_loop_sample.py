def find_element(target, data_list):
    """
    Find the index of a target element in a list.
    Contains an infinite loop and unreachable code.
    """
    index = 0
    
    # Infinite loop - condition never becomes False
    while index < len(data_list):
        if data_list[index] == target:
            return index
        # Missing increment of index
    
    # Unreachable code due to infinite loop
    return -1  # Not found
