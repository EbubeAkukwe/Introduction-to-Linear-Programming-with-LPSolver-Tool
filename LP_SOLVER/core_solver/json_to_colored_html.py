from html import escape

def json_to_colored_html(data):
    def format_value(value):
        if isinstance(value, dict):
            return '{<br>' + ',<br>'.join(
                f'&nbsp;&nbsp;<span style="color:#204a87;">"{escape(str(k))}"</span>: {format_value(v)}'
                for k, v in value.items()
            ) + '<br>}'

        elif isinstance(value, list):
            return '[<br>' + ',<br>'.join(
                '&nbsp;&nbsp;' + format_value(v) for v in value
            ) + '<br>]'

        elif isinstance(value, (int, float)):
            return f'<span style="color:purple;">{value}</span>'

        elif isinstance(value, str):
            if value.lower() == "maximize":
                return f'<span style="color:green;">"{escape(value)}"</span>'
            elif value.lower() == "minimize":
                return f'<span style="color:red;">"{escape(value)}"</span>'
            else:
                return f'"{escape(value)}"'

        else:
            return f'"{escape(str(value))}"'

    return f'<pre>{format_value(data)}</pre>'