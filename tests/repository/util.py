class ResMock:
    def __init__(self, ack: bool = True, inserted_id: str = '',
                 modified_count: int = 0):
        self.acknowledged = ack
        self.inserted_id = inserted_id
        self.modified_count = modified_count
