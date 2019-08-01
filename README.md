# Table-Maker
Prints a list of lists as a pretty table.


`table_maker(my_lists, headers)` takes a list of lists, my_lists, and a list, 
headers, and prints an aligned table with columns labeled by items in headers 
and with each row a sublist of my_lists. Each sublist of my_lists should 
have the same length as headers.


Calling table_maker with no parameters:

```
>>>table_maker()
┌─────────────────┬────────────────┬──────────────┐
│ Name            │ Address        │ Phone Number │
├─────────────────┼────────────────┼──────────────┤
│ John Smith      │ 356 Grove Rd   │ 123-4567     │
│ Mary Sue        │ 311 Penny Lane │ 555-2451     │
│ A Rolling Stone │ N/A            │ N/A          │
└─────────────────┴────────────────┴──────────────┘
```

Calling table_maker with suitable parameters:

```
>>> table_maker([['spotted','dog','pants','heavily'],['black','cat','meows','loudly'],\
['tall','man','runs','quickly']],['adjective','noun','verb','adverb'])
┌───────────┬──────┬───────┬─────────┐
│ adjective │ noun │ verb  │ adverb  │
├───────────┼──────┼───────┼─────────┤
│ spotted   │ dog  │ pants │ heavily │
│ black     │ cat  │ meows │ loudly  │
│ tall      │ man  │ runs  │ quickly │
└───────────┴──────┴───────┴─────────┘
```
