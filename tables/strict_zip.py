# Note this file is obsolete after Python 3.10 is released. `zip` will have a `strict` kwarg.

def _next_all(*iterables):
    """Yield the next item in each iterable or raise an error if each iterable doesn't raise a `StopIteration`
    """
    if not iterables:
        return

    first, *rest =  iterables
    try:
        yield next(first)
    except StopIteration:
        # First iterable raised StopIteration, so check that all other iterables also raise StopIteration
        for iterable in rest:
            try:
                next(iterable)
            except StopIteration:
                pass
            else:
                raise ValueError("inconsistent lengths")
    else:
        # First iterable did not raise StopIteration implies other iterables should also not raise StopIteration
        for iterable in rest:
            try:
                yield next(iterable)
            except StopIteration:
                raise ValueError("inconsistent lengths")

def strict_zip(*iterables):
    """A `zip` that raises an error if the number of items in each iterable isn't consistent.
    """
    iterables = tuple(map(iter, iterables))

    while zipped := tuple(_next_all(*iterables)):
        yield zipped
