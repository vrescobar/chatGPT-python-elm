# Define a function that takes a list and a value, and returns a new list
# with the value appended to the end.
def append(list, value):
    # Create a new list by concatenating the original list and a single-element
    # list containing the value.
    return list ++ [value]

# Define a function that takes a list and a value, and returns a new list
# with the value prepended to the beginning.
def prepend(list, value):
    # Create a new list by concatenating a single-element list containing
    # the value, and the original list.
    return [value] ++ list

# Define a main function that is called when the program is run.
def main():
    # Create a list of numbers from 1 to 10.
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Print the original list.
    print(numbers)

    # Append the number 11 to the end of the list.
    numbers = append(numbers, 11)

    # Print the modified list.
    print(numbers)

    # Prepend the number 0 to the beginning of the list.
    numbers = prepend(numbers, 0)

    # Print the modified list.
    print(numbers)

# Call the main function when the program is run.
main()
