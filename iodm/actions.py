class Action(object):

    undo_stack = []
    redo_stack = []

    def _undo(self):
        self.undo()
        self.redo_stack.append(self)

    def _redo(self):
        self.redo()
        self.undo_stack.append(self)

    def undo(self):
        raise NotImplementedError

    def redo(self):
        raise NotImplementedError

    @classmethod
    def clear(cls):
        cls.undo_stack, cls.redo_stack = [], []

    def __call__(self):
        self._redo()

class ActionContext(object):

    def __enter__(self):
        Action.clear()

    def __exit__(self, type, value, traceback):
        if type != None:
            while Action.undo_stack:
                Action.undo_stack.pop()._undo()

        return True