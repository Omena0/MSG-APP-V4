class plugin():
    def _default(self,*arg): pass
    def __init__(self):
        self.on_msg = self._default
        self.on_join = self._default
        self.on_leave = self._default
        self.on_init = self._default
        self.on_login = self._default
