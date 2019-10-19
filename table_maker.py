#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def table_maker(*my_lists, headers=None):
    """
    Takes a list of lists, my_lists, and a list, headers, and returns an
    aligned table with columns labeled by items in headers and with each row as
    a sublist of my_lists.

    Each sublist of my_lists should have the same length as headers.

    Output looks like:
    >>> print(table_maker(['John Smith', '356 Grove Rd', '123-4567'],
                          ['Mary Sue', '311 Penny Lane', '555-2451'],
                          ['A Rolling Stone', 'N/A', 'N/A'],
                          headers=['Name', 'Address', 'Phone Number']))

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
            raise ValueError('Length of rows inconsistent.')

    if headers and len(headers) != number_of_columns:
        raise ValueError('Length of headers inconsistent with length of rows.')

    my_lists = list(my_lists)
    if headers:
        my_lists.insert(0, headers)

    #Stringify
    for my_list in my_lists:
        for i, item in enumerate(my_list):
            my_list[i] = str(item)

    #Pad the length of items in each column
    table = zip(*my_lists)
    for i, column in enumerate(table):
        max_length = len(max(column, key=len))
        for j, item in enumerate(column):
            my_lists[j][i] += ' ' * (max_length - len(item))

    #Construct table
    table = [f'│ {" │ ".join(row)} │' for row in my_lists]
    top, title, bottom = (f'{left}{mid.join("─" * (len(item) + 2) for item in my_lists[0])}{right}'
                          for left, mid, right in ('┌┬┐','├┼┤','└┴┘'))

    table.insert(0, top)
    if headers:
        table.insert(2, title)
    table.append(bottom)
    table = "\n".join(table)

    return table
