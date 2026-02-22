"""Facade Real-World Example: Computer Subsystem Facade."""

from typing import List


class CPU:
    def freeze(self) -> None:
        pass

    def jump(self, position: int) -> None:
        pass

    def execute(self) -> None:
        pass


class Memory:
    def load(self, position: int, data: str) -> None:
        pass


class HardDrive:
    def read(self, lba: int, size: int) -> str:
        return "data"


class ComputerFacade:
    """Facade for complex computer subsystem."""

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()

    def start_computer(self) -> List[str]:
        """Start computer - abstracts complex boot process."""
        operations = []
        operations.append("starting hard drive...")
        self.hard_drive.read(0, 512)
        operations.append("loading boot sector into memory...")
        self.memory.load(0, self.hard_drive.read(0, 512))
        operations.append("starting CPU...")
        self.cpu.freeze()
        self.cpu.jump(0)
        self.cpu.execute()
        return operations


