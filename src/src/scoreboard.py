class scoreboard:
    def __init__(self, mem_id = []):
        self.mem_id = mem_id
        self.mac_calc = 0
        self.read_access = {}
        self.write_access = {}
        self.initialize_counters()

    def initialize_counters(self):
        self.mac_calc = 0
        for id in self.mem_id:
            self.read_access[id] = 0
            self.write_access[id] = 0

    def print_results(self):
        print("MAC CALC:",self.mac_calc)
        print("READ ACCESS:",self.read_access)
        print("WRITE ACCESS:",self.write_access)