

def create_element(tag, inner='', props={}):
    attr = " ".join([f'{k}="{v}"' for k, v in props.items()])
    return f'<{tag}{(" " + attr if props else "")}>{inner}</{tag}>'


def no_close(tag, props={}):
    attr = " ".join([f'{k}="{v}"' for k, v in props.items()])
    return f'<{tag}{(" " + attr if props else "")}>'


tag_names = ['b', 'i', 'a', 'p', 'div', 'fieldset', 'legend', 'table', 'th', 'tr', 'td', 'html', 'body']
tag_names.extend([f'h{x}' for x in range(1, 7)])

for tag in tag_names:
    def wrapper(inner, props={}, _tag=tag):
        return create_element(_tag, inner, props)

    globals()[tag] = wrapper


single_tags = ['br', 'hr', 'input', 'img', 'link', 'meta', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']

for single in single_tags:
    def wrapper(props={}, _tag=single):
        return no_close(_tag, props)

    globals()[single] = wrapper

def Table(data):
    header = ''.join(th(k) for k in data.keys())
    rows = []
    for x in range(len(data.keys())):
        row = []
        for k in data.keys():
            row.append(td(data[k][x]))
        rows.append(tr(''.join(row)))

    return table(f'{header}{"".join(rows)}')
