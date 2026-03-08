class Card:
    def __init__(self, value, is_joker=False):
     
        self.value = value
        self.is_joker = is_joker

    def isEqual(self, other):
    
        if not isinstance(other, Card):
            return False
        
        return self.value == other.value

    def debug(self):

        if self.is_joker:
            return "[ JOKER ]"
        return f"[{self.value}]"