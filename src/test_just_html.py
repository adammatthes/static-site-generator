import unittest
from just_html import *


class TestJustHTML(unittest.TestCase):
    def test_create_element(self):
        header = h1("This is a header")
        self.assertEqual(header, "<h1>This is a header</h1>")
        italic = i("Text is italics")
        self.assertEqual(italic, "<i>Text is italics</i>")
        nested = div(p(f'This is a {b("paragraph")}'))
        self.assertEqual(nested, "<div><p>This is a <b>paragraph</b></p></div>")
        properties = table('',props={'border-width': '1px'})
        self.assertEqual(properties, '<table border-width="1px"></table>')

    def test_no_close(self):
        break_ = br()
        self.assertEqual(break_, '<br>')
        Meta = meta(props={'encoding':'utf-8'})
        self.assertEqual(Meta, '<meta encoding="utf-8">')

    def test_table(self):
        my_table = Table({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        self.assertEqual(my_table, ''.join(
            ["<table><th>A</th><th>B</th><th>C</th>",
            "<tr><td>1</td><td>4</td><td>7</td></tr>",
            "<tr><td>2</td><td>5</td><td>8</td></tr>",
            "<tr><td>3</td><td>6</td><td>9</td></tr></table>"])
            )
