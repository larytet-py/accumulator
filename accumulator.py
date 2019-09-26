class Accumulator():
    def __init__(self, name, size):
        self.values = [0.0] * size # value, number of entries for average
        self.hits = [0.0] * size # number of values in a slot
        self.current = 0
        self.size = size
        self.name = name
        self.total = 0
    
    def inc(self):
        self.values[self.current] += 1
        self.hits[self.current] += 1

    def add(self, value):
        self.values[self.current] += value
        self.hits[self.current] += 1

    def tick(self):
        '''
        Move the accumulator to the next slot
        This method is not reentrant
        '''
        total = self.total
        total += 1
        current = total % self.size
        self.values[current] = 0
        self.hits[current] = 0
        self.current = current
        self.total = total

    def get_current(self):
        return self.values[self.current]

    def sprintf(self, columns, str_format, average=False):
        column = 0
        s = ""

        # Start from the oldest slot
        current = self.current
        if self.total < self.size:
            current = 0
        for value in self.values:            
            if not average:
                s  += str_format.format(value)
            else:
                hits = self.hits[current]
                if hits != 0:
                    s  += str_format.format(value/hits)
                else:
                    s  += str_format.format(0)

            column += 1
            if column % columns == 0:
                s  += "\n"
                column = 0

            current = (current + 1) % self.size

        return s

