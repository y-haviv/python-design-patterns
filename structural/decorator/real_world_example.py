"""Real-World Decorator Example: Advanced I/O Stream Wrapper System."""

from typing import Optional, List
import json


class Stream:
    """Abstract stream interface."""

    def write(self, data: str) -> None:
        pass

    def read(self) -> str:
        pass


class FileStream(Stream):
    """Concrete file stream."""

    def __init__(self, filename: str):
        self.filename = filename
        self.buffer = ""

    def write(self, data: str) -> None:
        self.buffer += data

    def read(self) -> str:
        return self.buffer


class StreamDecorator(Stream):
    """Abstract stream decorator."""

    def __init__(self, stream: Stream):
        self.stream = stream

    def write(self, data: str) -> None:
        self.stream.write(data)

    def read(self) -> str:
        return self.stream.read()


class CompressionStreamDecorator(StreamDecorator):
    """Decorator that compresses/decompresses data."""

    def write(self, data: str) -> None:
        compressed = "".join(c for c in data if c != " ")
        super().write(f"[COMPRESSED:{len(data)}->{len(compressed)}]" + compressed)

    def read(self) -> str:
        data = super().read()
        if data.startswith("[COMPRESSED:"):
            compressed = data.split("]")[1]
            return compressed
        return data


class EncryptionStreamDecorator(StreamDecorator):
    """Decorator that encrypts/decrypts data."""

    def write(self, data: str) -> None:
        encrypted = "".join(chr((ord(c) + 5) % 256) for c in data)
        super().write(f"[ENCRYPTED]" + encrypted)

    def read(self) -> str:
        data = super().read()
        if data.startswith("[ENCRYPTED]"):
            encrypted = data.split("]")[1]
            decrypted = "".join(chr((ord(c) - 5) % 256) for c in encrypted)
            return decrypted
        return data


class BufferedStreamDecorator(StreamDecorator):
    """Decorator that adds buffering."""

    def __init__(self, stream: Stream, buffer_size: int = 1024):
        super().__init__(stream)
        self.buffer_size = buffer_size
        self.buffer_list: List[str] = []

    def write(self, data: str) -> None:
        self.buffer_list.append(data)
        if sum(len(d) for d in self.buffer_list) >= self.buffer_size:
            self.flush()

    def flush(self) -> None:
        if self.buffer_list:
            combined = "".join(self.buffer_list)
            super().write(combined)
            self.buffer_list.clear()

    def read(self) -> str:
        self.flush()
        return super().read()


