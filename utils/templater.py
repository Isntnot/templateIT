import re
from datetime import datetime, timedelta

import re
from datetime import datetime, timedelta

def moment_to_python_format(fmt: str) -> str:
    """
    Safely translates Moment.js tokens to Python strftime directives 
    using a single-pass regex to prevent token collision.
    """
    mapping = {
        'YYYY': '%Y', 'YY': '%y',
        'MMMM': '%B', 'MMM': '%b', 'MM': '%m',
        'DD': '%d', 'D': '%d',
        'dddd': '%A', 'ddd': '%a',
        'HH': '%H', 'mm': '%M', 'ss': '%S',
        'Do': '%d',  # Fallback for ordinals
        'A': '%p'    # AM/PM
    }
    
    # Sort keys by length descending so longer tokens (like 'dddd') 
    # are matched before shorter ones (like 'A').
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    pattern = '|'.join(re.escape(k) for k in sorted_keys)
    
    def replace_token(match):
        return mapping[match.group(0)]
        
    return re.sub(pattern, replace_token, fmt)

def process_templater(template: str, file_title: str = "Untitled") -> str:
    """
    Evaluates Obsidian Templater expressions using safe regex parsing.
    """
    # 1. Process <% tp.file.title %>
    template = re.sub(r'<%\s*tp\.file\.title\s*%>', file_title, template)

    # 2. Process <% tp.date.now(...) %>
    def evaluate_date_now(match):
        args_raw = match.group(1).strip()
        args = [arg.strip().strip("'\"") for arg in args_raw.split(',') if arg.strip()]
        
        fmt = args[0] if len(args) > 0 else "YYYY-MM-DD"
        py_format = moment_to_python_format(fmt)
        
        target_date = datetime.now()
        if len(args) > 1 and args[1].lstrip('-').isdigit():
            target_date += timedelta(days=int(args[1]))
            
        return target_date.strftime(py_format)

    template = re.sub(r'<%\s*tp\.date\.now\((.*?)\)\s*%>', evaluate_date_now, template)
    template = re.sub(r'<%\s*tp\.date\.now\(\)\s*%>', datetime.now().strftime('%Y-%m-%d'), template)

    return template
if __name__ == "__main__":
    template_string = """---
    title: <% tp.file.title %>
    date: <% tp.date.now("YYYY-MM-DD") %>
    next_week: <% tp.date.now("YYYY-MM-DD", 7) %>
    ---
    # <% tp.file.title %>
    Hello! Today is <% tp.date.now("dddd, MMMM Do YYYY") %>.
    """

    result = process_templater(template_string, file_title="Project Phoenix")
    print(result)

