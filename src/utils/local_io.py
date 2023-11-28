"""
    filename: utils/local_io.py
    ~~~~~~~~~~~~~~~~~~~~
    local io tools for file read and write

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""


import aiofiles

async def a_write_file(path: str, content: bytes):
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)
        await f.flush()
        await f.close()  # not necessary if using async with

async def a_read_file(path: str) -> bytes:
    async with aiofiles.open(path, "rb") as f:
        return await f.read()
    
def write_file(path: str, content: bytes):
    with open(path, "wb") as f:
        f.write(content)
        f.flush()
        f.close()  # not necessary if using keyword `with`

def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()