#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def table_maker(*my_lists, headers=None):
    """
    Takes a list of lists, my_lists, and a list, headers, and prints an
    aligned table with columns labeled by items in headers and with each row as
    a sublist of my_lists.

    Each sublist of my_lists should have the same length as headers.

    Output looks like:
    >>> table_maker(['John Smith', '356 Grove Rd', '123-4567'],\
                    ['Mary Sue', '311 Penny Lane', '555-2451'],\
                    ['A Rolling Stone', 'N/A', 'N/A'],\
                    headers=['Name', 'Address', 'Phone Number'])

    ┌─────────────────┬────────────────┬──────────────┐
    │ Name            │ Address        │ Phone Number │
    ├─────────────────┼────────────────┼──────────────┤
    │ John Smith      │ 356 Grove Rd   │ 123-4567     │
    │ Mary Sue        │ 311 Penny Lane │ 555-2451     │
    │ A Rolling Stone │ N/A            │ N/A          │
    └─────────────────┴────────────────┴──────────────┘
    """
    number_of_columns = len(my_lists[0])

    #Check that sizes match up
    for my_list in my_lists[1:]:
        if len(my_list) != number_of_columns:
            print("Number of items in rows inconsistent")
            return

    if headers != None:
        if len(headers) != number_of_columns:
            print("Number of items in rows don't match number of headers.")
            return

    my_lists = list(my_lists)
    if headers != None:
        my_lists.insert(0, headers) #Combine headers and my_lists

    #Stringify
    for my_list in my_lists:
        for i, item in enumerate(my_list):
            my_list[i]=str(item)

    table = zip(*my_lists) #Transpose my_lists to iterate over columns
    for i, column in enumerate(table):
        max_length = max([len(item) for item in column])
        #Pad the length of items in each column
        for j, item in enumerate(column):
            my_lists[j][i] += " " * (max_length - len(item))

    #Construct table
    table = ["│ " + " │ ".join(row) + " │" for row in my_lists]

    box_drawing = [left +\
                   mid.join("─" * (len(item) + 2) for item in my_lists[0]) +\
                   right
                   for left, mid, right in [("┌", "┬", "┐"),\
                                            ("├", "┼", "┤"),\
                                            ("└", "┴", "┘")]]

    table.insert(0, box_drawing[0]) #Top of box
    if headers != None:
        table.insert(2, box_drawing[1]) #Horizontal Line after Headers
    table.append(box_drawing[2])    #Bottom of box
    table = "\n".join(table)        #Convert table as list to string

    print(table)
    #return table
