from pathlib import Path


def lines(p: Path, strip: bool = True):
    """Yields lines from file :param p: so that we can process them with or without storing. Opt-out withespace strip"""
    with open(p, 'r') as file:
        for line in file.readlines():
            if strip:
                yield line.strip()
            else:
                yield line

                
class TopN:
    """A structure that keeps track of only the top N biggest items"""
    def __init__(self, cap: int):
        self._cap = cap
        self._stack = []
    
    def add(self, item):
        """For bigger caps, it might be reasonable to insert with a binary search instead of sorting after each insert. (Or use a proper priority queue)"""
        self._stack.append(item)
        self._stack.sort()
        if len(self._stack) > self._cap:
            # Keep only N biggest values
            self._stack = self._stack[-self._cap:]
    
    def sum(self):
        return sum(self._stack)
    
    def __str__(self) -> str:
        return str(self._stack)
