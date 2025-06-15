import multiprocessing as mp


def set_string(array: mp.Array, max_len_str: int, index: int, string: str):
    s_bytes = string.encode("utf-8")[:max_len_str]
    start = index * max_len_str
    array[start : start + len(s_bytes)] = s_bytes
    array[start + len(s_bytes) : start + max_len_str] = b"\0" * (
        max_len_str - len(s_bytes)
    )


def get_string(array: mp.Array, max_len_str: int, index: int) -> str:
    start = index * max_len_str
    raw = bytes(array[start : start + max_len_str])
    return raw.split(b"\0", 1)[0].decode("utf-8")
