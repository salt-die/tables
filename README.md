# Table-Maker
Prints list of lists as a pretty table.


table_maker(my_lists, headers) takes a list of lists, my_lists, and a list, headers, and prints an aligned table with columns labeled by items in headers and each row as a sublist of my_lists. Each sublist of my_lists should have the same length as headers.

Default output looks like:

```
>>>table_maker()
┌────────────┬────────────────┬──────────────┐
│ Name       │ Address        │ Phone Number │
├────────────┼────────────────┼──────────────┤
│ John Smith │ 356 Grove Rd   │ 123-4567     │
│ Mary Sue   │ 311 Penny Lane │ 555-2451     │
│ Hobo       │ N/A            │ N/A          │
└────────────┴────────────────┴──────────────┘
```

Calling table_maker with a list of lists:

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
