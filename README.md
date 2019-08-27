# Table-Maker
Prints a list of lists as a pretty table.


`table_maker(*my_lists, headers)` takes a list of lists, my_lists, and a list,
headers, and returns an aligned table with columns labeled by items in headers
and with each row a sublist of my_lists. Each sublist of my_lists should
have the same length. headers is optional, but looks nice.


Example Outputs:

```
>>> print(table_maker(['John Smith', '356 Grove Rd', '123-4567'],\
                      ['Mary Sue', '311 Penny Lane', '555-2451'],\
                      ['A Rolling Stone', 'N/A', 'N/A'],\
                      headers=['Name', 'Address', 'Phone Number']))
┌─────────────────┬────────────────┬──────────────┐
│ Name            │ Address        │ Phone Number │
├─────────────────┼────────────────┼──────────────┤
│ John Smith      │ 356 Grove Rd   │ 123-4567     │
│ Mary Sue        │ 311 Penny Lane │ 555-2451     │
│ A Rolling Stone │ N/A            │ N/A          │
└─────────────────┴────────────────┴──────────────┘
```


```
>>> print(table_maker(['spotted','dog','pants','heavily'],\
                      ['black','cat','meows','loudly'],\
                      ['tall','man','runs','quickly'],\
                      headers=['adjective','noun','verb','adverb']))
┌───────────┬──────┬───────┬─────────┐
│ adjective │ noun │ verb  │ adverb  │
├───────────┼──────┼───────┼─────────┤
│ spotted   │ dog  │ pants │ heavily │
│ black     │ cat  │ meows │ loudly  │
│ tall      │ man  │ runs  │ quickly │
└───────────┴──────┴───────┴─────────┘
```

Or without headers:

```
>>> print(table_maker(["x-coordinate", 234.64, "y-coordinate", -123.54],\
                      ["x-coordinate", 1211.00, "y-coordinate", 10.03],\
                      ["x-coordinate", -176.50, "y-coordinate", -54.00],\
                      ["x-coordinate", 534.35, "y-coordinate", 566.24]))
┌──────────────┬────────┬──────────────┬─────────┐
│ x-coordinate │ 234.64 │ y-coordinate │ -123.54 │
│ x-coordinate │ 1211.0 │ y-coordinate │ 10.03   │
│ x-coordinate │ -176.5 │ y-coordinate │ -54.0   │
│ x-coordinate │ 534.35 │ y-coordinate │ 566.24  │
└──────────────┴────────┴──────────────┴─────────┘
```
