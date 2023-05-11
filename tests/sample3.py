class Sample:
    def __init__(self, rank: int = 0, world_size: int = 1) -> None:
        self.rank = rank
        self.world_size = world_size

    def get_rank(self) -> int:
        x = 1
        return self.rank

    def get_world_size(self) -> int:
        x = 1
        return self.world_size

    def echo1(self) -> None:
        x = 1
        print("echo1")

    def echo2(self) -> None:
        print("echo2")
