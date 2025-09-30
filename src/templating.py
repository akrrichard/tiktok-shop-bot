from __future__ import annotations
from typing import Dict
from jinja2 import Template

def render_template(text: str, vars: Dict) -> str:
    return Template(text).render(**vars)
