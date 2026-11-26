from typing import List, Optional
from index_recovery import format_tree, recover_student_index


def _lists_equal(a: Optional[List[int]], b: List[int]) -> bool:
    if a is None or len(a) != len(b):
        return False
    i = 0
    while i < len(b):
        if a[i] != b[i]:
            return False
        i += 1
    return True


def _format_int_list(values: Optional[List[int]]) -> str:
    if values is None:
        return "None"
    out = "["
    i = 0
    while i < len(values):
        if i > 0:
            out += ", "
        out += str(values[i])
        i += 1
    out += "]"
    return out


def _print_fragments(fragments: List[List[Optional[int]]]) -> None:
    i = 0
    while i < len(fragments):
        frag = fragments[i]
        line = "  ["
        j = 0
        while j < len(frag):
            if j > 0:
                line += ", "
            val = frag[j]
            line += "None" if val is None else str(val)
            j += 1
        line += "]"
        print(line)
        i += 1


def run_demo() -> None:
    print("============================================================")
    print("1. COMPATIBLE FRAGMENT SET (RECOVERABLE BST)")
    print("============================================================")
    compatible_frags: List[List[Optional[int]]] = [
        [40, 20, 60],
        [20, 12, 28],
        [60, 50, 75],
        [12, 8, None],
        [75, None, 88],
    ]
    print("Input fragments:")
    _print_fragments(compatible_frags)

    res_ok = recover_student_index(compatible_frags)
    expected_inorder: List[int] = [8, 12, 20, 28, 40, 50, 60, 75, 88]
    assert res_ok.possible is True
    assert res_ok.root is not None
    assert res_ok.root.val == 40
    assert _lists_equal(res_ok.inorder, expected_inorder)

    print("\nStatus: RECOVERED")
    print("Reason:", res_ok.reason)
    print("Merged Root ID:", res_ok.root.val)
    print("Inorder Traversal:", _format_int_list(res_ok.inorder))
    print("\nRecovered BST Structure:")
    print(format_tree(res_ok.root))

    print("\n============================================================")
    print("2. INCOMPATIBLE FRAGMENT SET (GLOBAL BST ORDERING CONFLICT)")
    print("============================================================")
    conflict_frags: List[List[Optional[int]]] = [
        [40, 20, 60],
        [20, 12, 28],
        [60, 35, 75],
    ]
    print("Input fragments:")
    _print_fragments(conflict_frags)

    res_conflict = recover_student_index(conflict_frags)
    assert res_conflict.possible is False

    print("\nStatus: REJECTED")
    print("Reason:", res_conflict.reason)
    print(
        "Explanation: Fragment [60, 35, 75] is valid on its own, "
        "but grafting it under 60 places 35 inside 40's right subtree, "
        "where all nodes must be strictly greater than 40."
    )

    print("\n============================================================")
    print("3. INCOMPATIBLE FRAGMENT SET (UNUSED / DISCONNECTED FRAGMENT)")
    print("============================================================")
    unused_frags: List[List[Optional[int]]] = [
        [40, 20, 60],
        [20, 12, 28],
        [100, 95, 105],
    ]
    print("Input fragments:")
    _print_fragments(unused_frags)

    res_unused = recover_student_index(unused_frags)
    assert res_unused.possible is False

    print("\nStatus: REJECTED")
    print("Reason:", res_unused.reason)
    print(
        "Explanation: Fragment [100, 95, 105] has root 100, which does not "
        "match any leaf node in the tree rooted at 40, so it cannot be used."
    )


if __name__ == "__main__":
    run_demo()
