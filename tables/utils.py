from functools import wraps

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

def stringify(iterable):
    return [str(item).strip() for item in iterable]

def needs_rebuild(method):
    """Indicates a method will mutate the table.
    """
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        self._needs_rebuild = True
        method(self, *args, **kwargs)

    return wrapped
