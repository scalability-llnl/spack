# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Data structures that represent Spack's edge types."""

from typing import Iterable, List, Tuple, Union

#: Type hint for the low-level dependency input (enum.Flag is too slow)
DepFlag = int

#: Type hint for the high-level dependency input
DepTypes = Union[str, List[str], Tuple[str, ...]]

#: Individual dependency types
DepType = str  # Python 3.8: Literal["build", "link", "run", "test"]

# Flag values. NOTE: these values are not arbitrary, since hash computation imposes
# the order (link, run, build, test) when depending on the same package multiple times,
# and we rely on default integer comparison to sort dependency types.
# New dependency types should be appended.
LINK = 0b0001
RUN = 0b0010
BUILD = 0b0100
TEST = 0b1000

#: The types of dependency relationships that Spack understands.
ALL_TYPES: Tuple[DepType, ...] = ("build", "link", "run", "test")

#: Default dependency type if none is specified
DEFAULT_TYPES: Tuple[DepType, ...] = ("build", "link")

#: A flag with all dependency types set
ALL: DepFlag = BUILD | LINK | RUN | TEST

#: Default dependency type if none is specified
DEFAULT: DepFlag = BUILD | LINK

#: A flag with no dependency types set
NONE: DepFlag = 0

#: An iterator of all flag components
ALL_FLAGS: Tuple[DepFlag, DepFlag, DepFlag, DepFlag] = (BUILD, LINK, RUN, TEST)


def compatible(flag1: DepFlag, flag2: DepFlag) -> bool:
    """Returns True if two depflags can be dependencies from a Spec to deps of the same name.

    The only allowable separated dependencies are a build-only dependency, combined with a
    non-build dependency. This separates our two process spaces, build time and run time.

    These dependency combinations are allowed:
        single dep on name: [b], [l], [r], [bl], [br], [blr]
        two deps on name: [b, l], [b, r], [b, lr]

    but none of these make any sense:
        two build deps: [b, b], [b, br], [b, bl], [b, blr]
        any two deps that both have an l or an r, i.e. [l, l], [r, r], [l, r], [bl, l], [bl, r]"""
    # Cannot have overlapping build types to two different dependencies
    if flag1 & flag2:
        return False

    # Cannot have two different link/run dependencies for the same name
    link_run = LINK | RUN
    if flag1 & link_run and flag2 & link_run:
        return False

    return True


def flag_from_string(s: str) -> DepFlag:
    if s == "build":
        return BUILD
    elif s == "link":
        return LINK
    elif s == "run":
        return RUN
    elif s == "test":
        return TEST
    else:
        raise ValueError(f"Invalid dependency type: {s}")


def flag_from_strings(deptype: Iterable[str]) -> DepFlag:
    """Transform an iterable of deptype strings into a flag."""
    flag = 0
    for deptype_str in deptype:
        flag |= flag_from_string(deptype_str)
    return flag


def canonicalize(deptype: DepTypes) -> DepFlag:
    """Convert deptype user input to a DepFlag, or raise ValueError.

    Args:
        deptype: string representing dependency type, or a list/tuple of such strings.
            Can also be the builtin function ``all`` or the string 'all', which result in
            a tuple of all dependency types known to Spack.
    """
    if deptype in ("all", all):
        return ALL

    if isinstance(deptype, str):
        return flag_from_string(deptype)

    if isinstance(deptype, (tuple, list, set)):
        return flag_from_strings(deptype)

    raise ValueError(f"Invalid dependency type: {deptype!r}")


def flag_to_tuple(x: DepFlag) -> Tuple[DepType, ...]:
    deptype: List[DepType] = []
    if x & BUILD:
        deptype.append("build")
    if x & LINK:
        deptype.append("link")
    if x & RUN:
        deptype.append("run")
    if x & TEST:
        deptype.append("test")
    return tuple(deptype)


def flag_to_string(x: DepFlag) -> DepType:
    if x == BUILD:
        return "build"
    elif x == LINK:
        return "link"
    elif x == RUN:
        return "run"
    elif x == TEST:
        return "test"
    else:
        raise ValueError(f"Invalid dependency type flag: {x}")


def flag_to_chars(depflag: DepFlag) -> str:
    """Create a string representing deptypes for many dependencies.

    The string will be some subset of 'blrt', like 'bl ', 'b t', or
    ' lr ' where each letter in 'blrt' stands for 'build', 'link',
    'run', and 'test' (the dependency types).

    For a single dependency, this just indicates that the dependency has
    the indicated deptypes. For a list of dependnecies, this shows
    whether ANY dpeendency in the list has the deptypes (so the deptypes
    are merged)."""
    return "".join(
        t_str[0] if t_flag & depflag else " " for t_str, t_flag in zip(ALL_TYPES, ALL_FLAGS)
    )
