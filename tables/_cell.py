class Cell:
    """A single entry in a table.
    """
    __slots__ = '_contents', 'display_width', '_lines', '_needs_rebuild'

    def __init__(self, contents=''):
        self.contents = str(contents)
        self.display_width = self.width

        self._lines = [ ]
        self._needs_rebuild = True

    @property
    def contents(self):
        return '\n'.join(self._contents)

    @contents.setter
    def contents(self, value):
        self._contents = value.splitlines()

    @property
    def height(self):
        return len(self.contents)

    @property
    def width(self):
        return max(map(len, self.contents))

    def __getitem__(self, row):
        if self._needs_rebuild:
            self._build_cell()

        if row < self.height:
            return self._lines[row]

        return ' ' * self.display_width

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

        if attr != '_needs_rebuild':
            self._needs_rebuild = attr != '_lines'

    def _build_cell(self):
        width = self.display_width
        self._lines = [ ]
        for line in self.contents:
            if len(line) > width:
                line[:width - 3] + '...'
                self._lines.append()
            self._lines.append(line[:width] + ' ' * (width - len(line)))

    def __repr__(self):
        return f'{type(self).__name__}(contents={self.contents!r})'
