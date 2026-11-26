# Registrar Student Index Recovery

An interactive web utility for reconstructing a unified Binary Search Tree (BST) student index from fragmented 1–3 node subtrees while validating structural connectivity and BST ordering invariants.

## Overview

In distributed or partially corrupted registrar databases, a student ID index may be split into small local node triples. **Registrar Student Index Recovery** takes a list of 1–3 node BST fragments, links matching parent-child references into a single rooted tree, and verifies that the resulting structure satisfies strict BST properties without disconnected components or cycles.

## Key Features

- **BST Fragment Merging:** Reconstructs a complete Binary Search Tree from `[root, left, right]` node definitions.
- **Conflict & Anomaly Detection:** Identifies BST ordering violations, cyclic references, multiple roots, and disconnected or unused fragments.
- **Built-in Test Presets:**
  - **Illustrative Sample:** Valid multi-level fragment set that merges cleanly into a balanced student index.
  - **Conflict Sample:** Demonstrates detection of ordering or structural conflicts across fragments.
  - **Unused Fragment Sample:** Highlights disconnected subtrees that do not attach to the primary root.
- **Diagnostic Outputs:**
  - **Merged Root ID:** Displays the root student identifier of the recovered index.
  - **Inorder Traversal:** Outputs the sorted sequence of student IDs to confirm valid BST ordering.
  - **Centered BST View:** Renders a visual tree layout of the reconstructed student index.

## Input Format

Fragments are provided as a JSON- or Python-style list of 3-element arrays:

```text
[root, left, right]
```

- `root`: Integer student ID of the fragment's parent node.
- `left`: Integer student ID of the left child, or `null` / `None` if empty.
- `right`: Integer student ID of the right child, or `null` / `None` if empty.

### Example Input

```json
[
  [40, 20, 60],
  [20, 12, 28],
  [60, 50, 75],
  [12, 8, null],
  [75, null, 88]
]
```

### Expected Output for Example

- **Merged Root ID:** `40`
- **Inorder Traversal:** `[8, 12, 20, 28, 40, 50, 60, 75, 88]`
- **Centered BST View:** Visual hierarchy rooted at `40` with left subtree `(20 -> 12 -> 8, 28)` and right subtree `(60 -> 50, 75 -> 88)`.

## Usage

1. Open the **Registrar Student Index Recovery** web interface.
2. Enter your list of `[root, left, right]` BST fragments in the input field (using `null` or `None` for missing children), or select one of the built-in sample buttons (**Illustrative Sample**, **Conflict Sample**, or **Unused Fragment Sample**).
3. Click **Recover Index** to validate the fragments and inspect the **Merged Root ID**, **Inorder Traversal**, and **Centered BST View**.

## Validation Rules

For a fragment set to recover into a valid student index, it must satisfy:

1. **Single Root Connectivity:** Exactly one node has no parent across all fragments, and all other nodes are reachable from this root.
2. **No Unused Fragments:** Every supplied fragment participates in the final merged tree.
3. **Strict BST Ordering:** For every node `N`, all values in its left subtree are strictly less than `N`, and all values in its right subtree are strictly greater than `N`.
4. **Acyclic Structure:** No node appears more than once or creates a cycle.
