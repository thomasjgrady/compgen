from typing import Callable, List, Optional, Tuple, TypeVar


T = TypeVar("T")

def find_sublist_range(
    l: List[T],
    sublist: List[T]
) -> Optional[Tuple[int, int]]:
    
    n = len(l)
    nsub = len(sublist)
    assert nsub <= n
    
    for i in range(n - nsub + 1):
        if l[i:i+nsub] == sublist:
            return (i, i+nsub)
    
    return None

def find_contiguous_ranges(
    xs: List[T],
    f: Callable[[T], bool]
) -> List[Tuple[int, int]]:
    
    if len(xs) == 0:
        return []
    
    idxs = [i for i, x in enumerate(xs) if f(x)]
    if len(idxs) == 0:
        return []
    
    if len(idxs) == 1:
        return [(idxs[0], idxs[0]+1)]
    
    start = idxs[0]
    curr = start+1
    out = []

    for j, i in enumerate(idxs[1:]):
        if i == curr:
            curr += 1
            if j == len(idxs)-2:
                out.append((start, curr))
        else:
            out.append((start, curr))
            start = i
            curr = i+1

    return out