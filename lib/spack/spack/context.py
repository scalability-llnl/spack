# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module provides classes used in user and build environment"""

from enum import Enum


class Context(Enum):
    """Enum used to indicate the context in which an environment has to be setup: build,
    run or test."""

    BUILD = 1
    RUN = 2
    TEST = 3

    def __str__(self):
        return ("build", "run", "test")[self.value - 1]

    @classmethod
    def from_string(cls, s: str):
        if s == "build":
            return Context.BUILD
        elif s == "run":
            return Context.RUN
        elif s == "test":
            return Context.TEST
        raise ValueError(f"context should be one of 'build', 'run', 'test', got {s}")
