from typing import List, Optional, Tuple


class TreeNode:
    def __init__(
        self,
        val: int,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class RecoveryResult:
    def __init__(
        self,
        possible: bool,
        root: Optional[TreeNode] = None,
        inorder: Optional[List[int]] = None,
        reason: str = "",
    ) -> None:
        self.possible = possible
        self.root = root
        self.inorder = inorder
        self.reason = reason


def _parse_fragment(raw: List[Optional[int]]) -> Tuple[int, Optional[int], Optional[int]]:
    if len(raw) == 0 or raw[0] is None:
        raise ValueError("Fragment must have a non-null root ID.")
    root_val = raw[0]
    left_val = raw[1] if len(raw) > 1 else None
    right_val = raw[2] if len(raw) > 2 else None
    return root_val, left_val, right_val


def _validate_local_fragment(
    root_val: int,
    left_val: Optional[int],
    right_val: Optional[int],
) -> Optional[str]:
    if left_val is not None and left_val >= root_val:
        return (
            "Fragment ["
            + str(root_val)
            + ", "
            + str(left_val)
            + ", "
            + str(right_val)
            + "] violates BST order: left child must be strictly less than root."
        )
    if right_val is not None and right_val <= root_val:
        return (
            "Fragment ["
            + str(root_val)
            + ", "
            + str(left_val)
            + ", "
            + str(right_val)
            + "] violates BST order: right child must be strictly greater than root."
        )
    return None


def _satisfies_bounds(val: int, low: Optional[int], high: Optional[int]) -> bool:
    if low is not None and val <= low:
        return False
    if high is not None and val >= high:
        return False
    return True


def _is_valid_bst(
    node: Optional[TreeNode],
    low: Optional[int] = None,
    high: Optional[int] = None,
) -> bool:
    if node is None:
        return True
    if not _satisfies_bounds(node.val, low, high):
        return False
    left_ok = _is_valid_bst(node.left, low, node.val)
    if not left_ok:
        return False
    right_ok = _is_valid_bst(node.right, node.val, high)
    return right_ok


def _collect_inorder(node: Optional[TreeNode], output: List[int]) -> None:
    if node is None:
        return
    _collect_inorder(node.left, output)
    output.append(node.val)
    _collect_inorder(node.right, output)


def inorder_traversal(node: Optional[TreeNode]) -> List[int]:
    result: List[int] = []
    _collect_inorder(node, result)
    return result


def _format_int_list(values: List[int]) -> str:
    parts: List[str] = []
    index = 0
    while index < len(values):
        parts.append(str(values[index]))
        index += 1
    out = "["
    idx = 0
    while idx < len(parts):
        if idx > 0:
            out += ", "
        out += parts[idx]
        idx += 1
    out += "]"
    return out


def _repeat_char(ch: str, count: int) -> str:
    result = ""
    i = 0
    while i < count:
        result += ch
        i += 1
    return result


def _join_lines(lines: List[str]) -> str:
    if len(lines) == 0:
        return ""
    output = lines[0]
    i = 1
    while i < len(lines):
        output += "\n" + lines[i]
        i += 1
    return output


def _build_centered_tree(node: TreeNode) -> Tuple[List[str], int, int, int]:
    label = str(node.val)
    label_len = len(label)

    if node.left is None and node.right is None:
        return [label], label_len, 1, label_len // 2

    if node.right is None:
        left_lines, left_w, left_h, left_mid = _build_centered_tree(node.left)  # type: ignore
        first_line = (
            _repeat_char(" ", left_mid + 1)
            + _repeat_char("_", left_w - left_mid - 1)
            + label
        )
        second_line = (
            _repeat_char(" ", left_mid)
            + "/"
            + _repeat_char(" ", left_w - left_mid - 1 + label_len)
        )

        lines: List[str] = [first_line, second_line]
        pad_right = _repeat_char(" ", label_len)
        i = 0
        while i < len(left_lines):
            lines.append(left_lines[i] + pad_right)
            i += 1

        return lines, left_w + label_len, left_h + 2, left_w + label_len // 2

    if node.left is None:
        right_lines, right_w, right_h, right_mid = _build_centered_tree(node.right)
        first_line = (
            label
            + _repeat_char("_", right_mid)
            + _repeat_char(" ", right_w - right_mid)
        )
        second_line = (
            _repeat_char(" ", label_len + right_mid)
            + "\\"
            + _repeat_char(" ", right_w - right_mid - 1)
        )

        lines = [first_line, second_line]
        pad_left = _repeat_char(" ", label_len)
        i = 0
        while i < len(right_lines):
            lines.append(pad_left + right_lines[i])
            i += 1

        return lines, right_w + label_len, right_h + 2, label_len // 2

    left_lines, left_w, left_h, left_mid = _build_centered_tree(node.left)
    right_lines, right_w, right_h, right_mid = _build_centered_tree(node.right)

    first_line = (
        _repeat_char(" ", left_mid + 1)
        + _repeat_char("_", left_w - left_mid - 1)
        + label
        + _repeat_char("_", right_mid)
        + _repeat_char(" ", right_w - right_mid)
    )
    second_line = (
        _repeat_char(" ", left_mid)
        + "/"
        + _repeat_char(" ", left_w - left_mid - 1 + label_len + right_mid)
        + "\\"
        + _repeat_char(" ", right_w - right_mid - 1)
    )

    if left_h < right_h:
        blank_left = _repeat_char(" ", left_w)
        diff = right_h - left_h
        k = 0
        while k < diff:
            left_lines.append(blank_left)
            k += 1
        total_h = right_h + 2
    elif right_h < left_h:
        blank_right = _repeat_char(" ", right_w)
        diff = left_h - right_h
        k = 0
        while k < diff:
            right_lines.append(blank_right)
            k += 1
        total_h = left_h + 2
    else:
        total_h = left_h + 2

    lines = [first_line, second_line]
    gap = _repeat_char(" ", label_len)
    row = 0
    while row < len(left_lines):
        lines.append(left_lines[row] + gap + right_lines[row])
        row += 1

    return lines, left_w + right_w + label_len, total_h, left_w + label_len // 2


def format_tree(node: Optional[TreeNode]) -> str:
    if node is None:
        return ""
    lines, _, _, _ = _build_centered_tree(node)
    return _join_lines(lines)


def _find_unused_roots(all_roots: List[int], used_roots: List[int]) -> List[int]:
    unused: List[int] = []
    i = 0
    while i < len(all_roots):
        candidate = all_roots[i]
        found = False
        j = 0
        while j < len(used_roots):
            if used_roots[j] == candidate:
                found = True
                break
            j += 1
        if not found:
            unused.append(candidate)
        i += 1
    return unused


def _contains_int(items: List[int], target: int) -> bool:
    idx = 0
    while idx < len(items):
        if items[idx] == target:
            return True
        idx += 1
    return False


def recover_student_index(fragments: List[List[Optional[int]]]) -> RecoveryResult:
    if len(fragments) == 0:
        return RecoveryResult(False, None, None, "IMPOSSIBLE: No fragments provided.")

    parsed: dict[int, Tuple[Optional[int], Optional[int]]] = {}
    root_order: List[int] = []
    referenced_children: List[int] = []

    frag_idx = 0
    while frag_idx < len(fragments):
        raw = fragments[frag_idx]
        try:
            r_val, l_val, r_child = _parse_fragment(raw)
        except ValueError as exc:
            return RecoveryResult(False, None, None, "IMPOSSIBLE: " + str(exc))

        if r_val in parsed:
            return RecoveryResult(
                False,
                None,
                None,
                "IMPOSSIBLE: Duplicate root ID " + str(r_val) + ".",
            )

        local_err = _validate_local_fragment(r_val, l_val, r_child)
        if local_err is not None:
            return RecoveryResult(False, None, None, "IMPOSSIBLE: " + local_err)

        parsed[r_val] = (l_val, r_child)
        root_order.append(r_val)

        if l_val is not None and not _contains_int(referenced_children, l_val):
            referenced_children.append(l_val)
        if r_child is not None and not _contains_int(referenced_children, r_child):
            referenced_children.append(r_child)

        frag_idx += 1

    candidate_roots: List[int] = []
    idx = 0
    while idx < len(root_order):
        r_id = root_order[idx]
        if not _contains_int(referenced_children, r_id):
            candidate_roots.append(r_id)
        idx += 1

    search_order = candidate_roots if len(candidate_roots) > 0 else root_order
    last_failure = "IMPOSSIBLE: Fragments cannot form a single valid BST using every fragment once."

    order_idx = 0
    while order_idx < len(search_order):
        start_root = search_order[order_idx]
        used: List[int] = []
        active_stack: List[int] = []
        cycle_flag = [False]

        def build(val: Optional[int]) -> Optional[TreeNode]:
            if val is None:
                return None
            if _contains_int(active_stack, val):
                cycle_flag[0] = True
                return None
            if val not in parsed:
                return TreeNode(val)
            if _contains_int(used, val):
                cycle_flag[0] = True
                return None

            used.append(val)
            active_stack.append(val)
            l_val, r_child = parsed[val]
            left_node = build(l_val)
            right_node = build(r_child)
            active_stack.pop()
            return TreeNode(val, left_node, right_node)

        root_node = build(start_root)

        if cycle_flag[0]:
            last_failure = (
                "IMPOSSIBLE: Cycle detected while expanding from root " + str(start_root) + "."
            )
            order_idx += 1
            continue

        if len(used) != len(root_order):
            unused = _find_unused_roots(root_order, used)
            last_failure = (
                "IMPOSSIBLE: Disconnected or unused fragment root IDs "
                + _format_int_list(unused)
                + " when starting from root "
                + str(start_root)
                + "."
            )
            order_idx += 1
            continue

        if not _is_valid_bst(root_node, None, None):
            last_failure = (
                "IMPOSSIBLE: Merging fragments starting at root "
                + str(start_root)
                + " violates global BST ordering constraints."
            )
            order_idx += 1
            continue

        return RecoveryResult(
            True,
            root_node,
            inorder_traversal(root_node),
            "Recovered single valid BST using every fragment once.",
        )

    return RecoveryResult(False, None, None, last_failure)
