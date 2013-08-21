#!/usr/bin/env python

import pytest

pytest.main("--cov hand --cov-report xml --cov-report term-missing --junitxml=tests.xml")
