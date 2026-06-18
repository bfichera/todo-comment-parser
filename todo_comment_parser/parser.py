import re
import os
from warnings import warn


class Parser:

    def __init__(self, text, todo_tag: str = 'TODO'):
        self.text = text
        self.todo_tag = todo_tag
        self.lines = self.text.splitlines()
        self._todo_pars = None

    @classmethod
    def from_file(cls, path: str | os.PathLike, todo_tag: str = 'TODO'):
        try:
            with open(path, 'r') as fh:
                text = fh.read()
        except Exception as e:
            warn(f'Unable to read file: {path}. Reason: {e}')
            return
        return cls(text, todo_tag)

    @property
    def todo_pars(self):
        if self._todo_pars is not None:
            return self._todo_pars
        todo_idxs = []
        for i, line in enumerate(self.lines):
            search = re.search(re.escape(self.todo_tag), line)
            if search is not None:
                todo_idxs.append(i)
        comment_strs = []
        for todo_idx in todo_idxs:
            todo_line = self.lines[todo_idx]
            match = re.match(fr'^\s*(.*){re.escape(self.todo_tag)}', todo_line)
            comment_strs.append(match.group(1))
        if not comment_strs:
            return []
        if not all([c == comment_strs[0] for c in comment_strs]):
            raise ValueError('File contains multiple types of comments')
        comment_str = comment_strs[0]
        todo_pars = []
        state = 'skipping'
        todo_par = ''
        for i, line in enumerate(self.lines):
            if state == 'skipping':
                if i in todo_idxs:
                    state = 'todoline'
            if state == 'todoline':
                todo_par += line
                state = 'reading'
                continue
            if state == 'reading':
                if i in todo_idxs:
                    todo_pars.append(todo_par)
                    todo_par = line
                    state = 'reading'
                    continue
                if line.strip().startswith(comment_str.strip()):
                    todo_par += line
                else:
                    todo_pars.append(todo_par)
                    todo_par = ''
                    state = 'skipping'
                    continue
        if state == 'reading' and todo_par:
            todo_pars.append(todo_par)
        self._todo_pars = todo_pars
        return todo_pars

    def print(self):
        for todo_par in self.todo_pars:
            print(todo_par)
            print('----------')
        return len(self.todo_pars)
