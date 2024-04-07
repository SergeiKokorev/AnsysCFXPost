import re

from PySide6.QtWidgets import QFormLayout


from models.data import *
from tools.const import WIDGETS as wd, MVC_WIDGETS as mvc


def get_data(file: str) -> list:

    try:
        with open(file, 'r', newline='') as f:

            result = []

            domain = re.compile(r'domain:\s*\w*')
            dmn_found = False
            domain_type = re.compile(r'domain\s*type\s*=\s*\w*')
            boundary = re.compile(r'boundary:[\s\w\d]*')
            boundary_type = re.compile(r'boundary\s*type\s*=\s*\w*')
            end = re.compile(r'solver\s+control:')

            lines = f.readlines()

            for line in lines:
                if re.fullmatch(domain, line.strip().lower()):
                    dmn_found = True
                    dmn = Domain(line.split(':')[1].strip())
                    result.append(dmn)
                if dmn_found:
                    if re.fullmatch(domain_type, line.strip().lower()):
                        dmn.type = line.split('=')[1].strip().lower()
                    elif re.fullmatch(boundary, line.strip().lower()):
                        bnd = Boundary(line.split(':')[1].strip())
                        dmn.addItem(bnd)
                    elif re.fullmatch(boundary_type, line.strip().lower()):
                        bnd.type = line.split('=')[1].strip().lower()
                if re.fullmatch(end, line.strip().lower()):
                    break
        return result

    except (FileExistsError, FileNotFoundError, PermissionError):
        return None
    

def generate_dialog(widgets: dict, model: List[Domain], parent=None) -> QFormLayout:
    
    layout = QFormLayout()
    for obj in widgets:
        widget = obj['widget']
        w = None
        if widget in wd.keys():
            w = wd[widget](parent=parent)
        elif widget in mvc.keys():
            w = mvc[widget](parent=parent, model=model)
        if not w:
            continue
        w.setObjectName(obj['name'])
        layout.addRow(obj['title'], w)

    return layout