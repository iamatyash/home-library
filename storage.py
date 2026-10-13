class MyMap:
    def __init__(self):
        self._keys = []
        self._vals = []

    @property
    def keys(self):
        return list(self._keys)

    @property
    def values(self):
        return list(self._vals)

    def put(self, key, value):
        if key in self._keys:
            idx = self._keys.index(key)
            self._vals[idx] = value
        else:
            self._keys.append(key)
            self._vals.append(value)

    def get(self, key, default=None):
        if key in self._keys:
            idx = self._keys.index(key)
            return self._vals[idx]
        return default

    def remove(self, key):
        if key in self._keys:
            idx = self._keys.index(key)
            self._keys.pop(idx)
            self._vals.pop(idx)

    def __getitem__(self, key):
        if key in self._keys:
            return self.get(key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return key in self._keys

    def __repr__(self):
        items_str = ", ".join(f"{k!r}: {v!r}" for k, v in zip(self._keys, self._vals))
        return f"MyMap({{{items_str}}})"

    def __str__(self):
        return self.__repr__()
