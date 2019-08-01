def table_maker(my_lists=[['John Smith','356 Grove Rd','123-4567'],\
                          ['Mary Sue', '311 Penny Lane', '555-2451'],\
                          ['Hobo', 'N/A', 'N/A']],\
                headers=['Name','Address','Phone Number']):
    """
    Takes a list of lists, my_lists, and a list, headers, and prints an
    aligned table with columns labeled by items in headers and each row as a
    sublist of my_lists.

    Each sublist of my_lists should have the same length as headers.
    
    Default output looks like:
    ┌────────────┬────────────────┬──────────────┐
    │ Name       │ Address        │ Phone Number │
    ├────────────┼────────────────┼──────────────┤
    │ John Smith │ 356 Grove Rd   │ 123-4567     │
    │ Mary Sue   │ 311 Penny Lane │ 555-2451     │
    │ Hobo       │ N/A            │ N/A          │
    └────────────┴────────────────┴──────────────┘
    
    """

    number_of_items = len(headers)

    #Check that sizes match up
    for my_list in my_lists:
        if len(my_list) != number_of_items:
            return "Number of items in rows don't match number of headers."

    my_lists.insert(0, headers) #Combine headers and my_lists
    table = zip(*my_lists) #Transpose my_lists to iterate over columns

    lengths = []
    row_length = 0
    for i, column in enumerate(table):
        max_length = max([len(item) for item in column])
        row_length += max_length
        lengths.append(max_length)

        #Pad the length of items in each column
        for j, item in enumerate(column):
            my_lists[j][i] += " " * (max_length - len(item))

    #Construct table
    table = "\n".join("│ " + " │ ".join(line) + " │" for line in my_lists) + "\n"
    def box_drawing(i):
        a, b, c = [("┌","┬","┐"),("├","┼","┤"),("└","┴","┘")][i]
        return a + b.join("─" * (length + 2) for length in lengths) + c
    row_length += number_of_items * 3 + 2
    table = box_drawing(0) + "\n" +\
            table[:row_length] +\
            box_drawing(1) + "\n" +\
            table[row_length:] +\
            box_drawing(2)

    print(table)
    #return table #Alternatively use this line to save the table as a string
