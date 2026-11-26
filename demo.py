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


def _strip_spaces(text: str) -> str:
    out = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if ch != " " and ch != "\t" and ch != "\r" and ch != "\n":
            out += ch
        i += 1
    return out


def _parse_token(token: str) -> Optional[int]:
    if token == "" or token == "None" or token == "none" or token == "null" or token == "NULL":
        return None
    sign = 1
    idx = 0
    if token[0] == "-":
        sign = -1
        idx = 1
    if idx >= len(token):
        raise ValueError("Invalid number token: " + token)
    val = 0
    while idx < len(token):
        ch = token[idx]
        if ch < "0" or ch > "9":
            raise ValueError("Invalid integer character: " + ch)
        val = val * 10 + (ord(ch) - ord("0"))
        idx += 1
    return sign * val


def parse_user_fragments(raw_input: str) -> List[List[Optional[int]]]:
    clean = _strip_spaces(raw_input)
    if len(clean) < 2 or clean[0] != "[" or clean[len(clean) - 1] != "]":
        raise ValueError("Expected format like [[2,1],[3,2,5],[5,4]].")

    inner = clean[1 : len(clean) - 1]
    if inner == "":
        return []

    fragments: List[List[Optional[int]]] = []
    i = 0
    while i < len(inner):
        if inner[i] != "[":
            raise ValueError("Expected '[' at start of fragment.")
        i += 1
        current_frag: List[Optional[int]] = []
        token = ""
        found_close = False
        while i < len(inner):
            ch = inner[i]
            if ch == ",":
                current_frag.append(_parse_token(token))
                token = ""
            elif ch == "]":
                if token != "" or len(current_frag) > 0:
                    current_frag.append(_parse_token(token))
                found_close = True
                i += 1
                break
            else:
                token += ch
            i += 1

        if not found_close:
            raise ValueError("Unclosed fragment bracket ']'.")
        if len(current_frag) < 1 or len(current_frag) > 3:
            raise ValueError("Each fragment must contain 1 to 3 elements.")
        fragments.append(current_frag)

        if i < len(inner):
            if inner[i] != ",":
                raise ValueError("Expected ',' between fragments.")
            i += 1

    return fragments


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

    print("\n============================================================")
    print("4. INTERACTIVE USER INPUT")
    print("============================================================")
    print("Enter fragments as [[root,left,right],...] (press Enter to skip):")
    try:
        user_line = input("> ").strip()
    except EOFError:
        user_line = ""

    if user_line != "":
        try:
            user_frags = parse_user_fragments(user_line)
            res_user = recover_student_index(user_frags)
            if res_user.possible and res_user.root is not None:
                print("\nStatus: RECOVERED")
                print("Merged Root ID:", res_user.root.val)
                print("Inorder Traversal:", _format_int_list(res_user.inorder))
                print("\nRecovered BST Structure:")
                print(format_tree(res_user.root))
            else:
                print("\nStatus: REJECTED")
                print("Reason:", res_user.reason)
        except ValueError as exc:
            print("\nInput Error:", str(exc))


if __name__ == "__main__":
    run_demo()
