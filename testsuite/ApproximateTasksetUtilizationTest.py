import unittest
from model.generators.generator import mergeTaskSets
import itertools

class ApproximateTasksetUtilization(unittest.TestCase):


    def testMerge(self):
        taskset_lhs = [1,2,3]
        taskset_rhs = [4,5,6]
        self.assertEqual(list(itertools.chain(taskset_lhs, taskset_rhs)), [1,2,3,4,5,6])

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
