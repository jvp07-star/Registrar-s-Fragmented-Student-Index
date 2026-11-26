import os
from typing import List, Optional
from flask import Flask, jsonify, render_template, request
from demo import parse_user_fragments
from index_recovery import format_tree, recover_student_index

app = Flask(__name__)


def _serialize_fragments(fragments: List[List[Optional[int]]]) -> str:
    out = "["
    i = 0
    while i < len(fragments):
        if i > 0:
            out += ", "
        frag = fragments[i]
        out += "["
        j = 0
        while j < len(frag):
            if j > 0:
                out += ", "
            val = frag[j]
            out += "null" if val is None else str(val)
            j += 1
        out += "]"
        i += 1
    out += "]"
    return out


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/recover")
def recover_api():
    payload = request.get_json(silent=True) or {}
    raw_input = str(payload.get("fragments", "")).strip()

    try:
        fragments = parse_user_fragments(raw_input)
    except ValueError as exc:
        return jsonify(
            {
                "possible": False,
                "reason": "IMPOSSIBLE: " + str(exc),
                "root": None,
                "inorder": [],
                "tree_ascii": "",
                "normalized_input": raw_input,
            }
        ), 400

    result = recover_student_index(fragments)
    root_val = result.root.val if result.root is not None else None
    inorder_vals = result.inorder if result.inorder is not None else []
    tree_text = format_tree(result.root) if result.possible else ""

    return jsonify(
        {
            "possible": result.possible,
            "reason": result.reason,
            "root": root_val,
            "inorder": inorder_vals,
            "tree_ascii": tree_text,
            "normalized_input": _serialize_fragments(fragments),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
