def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    Contains type errors and potential division by zero.
    """
    # Type error: Adding string to int
    count = "Total items: " + len(numbers)
    
    # Potential division by zero
    if len(numbers) == 0:
        average = sum(numbers) / len(numbers)
    else:
        # Logic error in calculation (should divide by len(numbers))
        average = sum(numbers) / 2
    
    return average
