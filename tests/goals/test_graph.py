import unittest

from goal import Goal


class TestGraphMethods(unittest.TestCase):

    def test_search_name(self):
        # Building goals
        g_a = Goal(name="a")
        g_b = Goal(name="b")
        g_c = Goal(name="c")
        g_d = Goal(name="d")
        g_e = Goal(name="e")
        g_f = Goal(name="f")
        g_g = Goal(name="g")
        g_h = Goal(name="h")


        self.assertEqual('foo'.upper(), 'FOO')

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