


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if value is None:
            assert children is not None and len(children)
        self.children = children
        self.props = props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

    def __eq__(self, r_val):
        return self.tag == r_val.tag and self.value == r_val.value and self.children == r_val.children and self.props == r_val.props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return ''.join(f' {k}={v}' for k, v in self.props)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        if children is not None or value is None:
            raise ValueError("Leaf Node cannot have children")
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        return f'<{self.tag}{" " + self.props_to_html() if self.props is not None else ""}>{self.value}</{self.tag}>'
           
