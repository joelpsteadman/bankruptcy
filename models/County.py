class County:
    
    def __init__(self, code):
        self.code = code
        self.used = False
        self.population = 0.0

    def get_bankruptcy_rate(self):
        return float(self.bankruptcies) / self.population