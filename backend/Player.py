class Player:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team

    def __eq__(self, other):
        if isinstance(other, Player):
            return (self.name, self.position, self.team) == (other.name, other.position, other.team)
        return False

    def __hash__(self):
        return hash((self.name, self.position, self.team))

    def __repr__(self):
        return f"Player(name={self.name}, position={self.position}, team={self.team})"
