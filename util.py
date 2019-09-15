import json
import functools
from difflib import SequenceMatcher


def pretty_print_dictionary(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        output = func(self, *args, **kwargs)
        print(json.dumps(output, indent=4))
    return wrapper


class StringWrapper(object):
    DEFAULT_THRESHOLD = 0.5

    def __init__(self, value, case_sensitive=False, default_similarity_threshold=DEFAULT_THRESHOLD):
        self.default_similarity_threshold = default_similarity_threshold
        self.case_sensitive = case_sensitive
        self._value = value

    def _sensitivity_matching(self, string):
        return string if self.case_sensitive else string.lower()

    @property
    def value(self):
        return self._sensitivity_matching(self._value)

    def contains(self, pattern, reverse=False):
        pattern = self._sensitivity_matching(string=pattern)
        return (pattern in self.value) if not reverse else (self.value in pattern)

    def similarity_ratio(self, pattern):
        pattern = self._sensitivity_matching(string=pattern)
        return SequenceMatcher(None, self.value, pattern).ratio()

    def similar_enough(self, pattern, threshold=None):
        min_ratio = threshold if threshold else self.default_similarity_threshold
        return self.similarity_ratio(pattern) > min_ratio

    def boolean_search(self, pattern, exact=False, threshold=None, reverse=False):
        return self.contains(pattern, reverse=reverse) if exact else self.similar_enough(pattern, threshold=threshold)
