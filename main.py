"""Validate and publish the pre-rendered PNG; Python 3.13, standard library only."""

import os
from pathlib import Path
import shutil
import struct
import zlib


def validate_png(path: Path) -> None:
    data = path.read_bytes()
    if len(data) > 1024 * 1024:
        raise ValueError("entry.png exceeds 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    offset, chunks, compressed = 8, [], bytearray()
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("Truncated PNG chunk")
        size, kind = struct.unpack_from(">I4s", data, offset)
        end = offset + 12 + size
        if end > len(data):
            raise ValueError("Truncated PNG payload")
        payload = data[offset + 8 : end - 4]
        crc = struct.unpack_from(">I", data, end - 4)[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc:
            raise ValueError("Invalid PNG checksum")
        if not chunks and kind != b"IHDR":
            raise ValueError("PNG must start with IHDR")
        if kind == b"IHDR":
            if chunks or size != 13:
                raise ValueError("Invalid PNG header")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if (width, height) != (1024, 1024):
                raise ValueError("PNG must be 1024x1024")
            if (depth, color, compression, filtering, interlace) != (8, 2, 0, 0, 0):
                raise ValueError("Expected a non-interlaced 8-bit RGB PNG")
        elif kind == b"IDAT":
            if chunks[-1] not in (b"IHDR", b"IDAT"):
                raise ValueError("Unexpected PNG image-data order")
            compressed.extend(payload)
        elif kind == b"IEND":
            if size or not compressed or end != len(data):
                raise ValueError("Invalid PNG ending")
        else:
            raise ValueError("Unexpected chunk in pre-rendered PNG")
        chunks.append(kind)
        offset = end
    if not chunks or chunks[-1] != b"IEND":
        raise ValueError("Missing PNG ending")
    expected = 1024 * (1 + 1024 * 3)
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(compressed, expected + 1)
    if len(pixels) != expected or not decoder.eof or decoder.unused_data:
        raise ValueError("Invalid PNG pixel stream")
    if any(pixels[row * 3073] > 4 for row in range(1024)):
        raise ValueError("Invalid PNG row filter")


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    validate_png(source)
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    target = output / "entry.png"
    if source.resolve() != target.resolve():
        shutil.copyfile(source, target)


if __name__ == "__main__":
    main()
