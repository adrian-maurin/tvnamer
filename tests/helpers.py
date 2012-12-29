#!/usr/bin/env python

"""Helper functions for use in tests
"""

import os
import functools


def assertEquals(a, b):
    assert a == b, "Error, %r not equal to %r" % (a, b)


def assertType(obj, type):
    assert isinstance(obj, type), "Expecting %s, got %r" % (
        type(obj),
        type)


def expected_failure(test):
    """Used as a decorator on a test function. Skips the test if it
    fails, or fails the test if it passes (so the decorator can be
    removed)

    Kind of like the SkipTest nose plugin, but avoids tests being
    skipped quietly if they are fixed "accidentally"

    http://stackoverflow.com/q/9613932/745
    """

    @functools.wraps(test)
    def inner(*args, **kwargs):
        try:
            test(*args, **kwargs)
        except AssertionError:
            from nose.plugins.skip import SkipTest
            raise SkipTest("Expected failure failed, as expected")
        else:
            raise AssertionError('Failure expected')

    return inner


def expected_failure_travisci(test):
    """Like expected_failure, but only expects a failure when the
    env-var TRAVIS is "true"
    """

    @functools.wraps(test)
    def inner(*args, **kwargs):
        if os.getenv("TRAVIS", "false") == "true":
            try:
                test(*args, **kwargs)
            except AssertionError:
                from nose.plugins.skip import SkipTest
                raise SkipTest("Expected failure failed, as expected on Travis-CI")
            else:
                raise AssertionError('Failure expected on Travis-CI')

        else:
            return test(*args, **kwargs)

    return inner
