class mem:
    def __init__(self, id=0, sizes={}, data={}, scoreboard=None, parent=None):
        self.id = id
        self.sizes = sizes
        self.data = data
        self.scoreboard = scoreboard
        self.parent = parent

    def read(self, read_data):
        type = read_data[0]
        if read_data in self.data[type]:
            self.scoreboard.read_access[self.id] += 1
        else:
            self.parent.read(read_data)
            self.write(read_data)
            self.scoreboard.read_access[self.id] += 1

    def write(self, write_data):
        type = write_data[0]
        if write_data not in self.data[type]:
            if len(self.data[type]) >= self.sizes[type]:
                self.data[type].pop(0)
                if type == 'o':
                    self.parent.write(write_data)
            self.data[type].append(write_data)
        self.scoreboard.write_access[self.id] += 1