import unittest

loader = unittest.TestLoader()
tests = loader.discover('src/tests/unit-tests')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
