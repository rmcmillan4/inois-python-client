# -*- coding: utf-8 -*-

import pytest
from inois.skeleton import fib

__author__ = "chad.mckee"
__copyright__ = "chad.mckee"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
