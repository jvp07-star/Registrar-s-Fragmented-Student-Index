import unittest
from index_recovery import recover_student_index


class TestStudentIndexRecovery(unittest.TestCase):
    def test_illustrative_example(self):
        frags = [[2, 1], [3, 2, 5], [5, 4]]
        res = recover_student_index(frags)
        self.assertTrue(res.possible)
        self.assertEqual(res.root.val, 3)
        self.assertEqual(res.inorder, [1, 2, 3, 4, 5])

    def test_multi_branch_grafting(self):
        frags = [
            [50, 25, 75],
            [25, 10, 35],
            [75, 60, 90],
            [10, 5],
            [90, None, 99],
        ]
        res = recover_student_index(frags)
        self.assertTrue(res.possible)
        self.assertEqual(res.root.val, 50)
        self.assertEqual(res.inorder, [5, 10, 25, 35, 50, 60, 75, 90, 99])

    def test_global_bst_conflict(self):
        # 42 is in the right subtree of 30, so grafting [42, 20, None] puts 20 < 30 on the right side.
        frags = [[30, 15, 42], [42, 20, None]]
        res = recover_student_index(frags)
        self.assertFalse(res.possible)
        self.assertIn("IMPOSSIBLE", res.reason)

    def test_unused_disconnected_fragment(self):
        frags = [[20, 10, 30], [10, 5], [80, 70, 90]]
        res = recover_student_index(frags)
        self.assertFalse(res.possible)
        self.assertIn("80", res.reason)

    def test_cycle_rejected(self):
        frags = [[10, 5], [5, None, 10]]
        res = recover_student_index(frags)
        self.assertFalse(res.possible)
        self.assertIn("IMPOSSIBLE", res.reason)


if __name__ == "__main__":
    unittest.main()
