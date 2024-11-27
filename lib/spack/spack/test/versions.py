# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""These version tests were taken from the RPM source code.
We try to maintain compatibility with RPM's version semantics
where it makes sense.
"""
import os
import pathlib

import pytest

from llnl.util.filesystem import working_dir

import spack.package_base
import spack.spec
import spack.version
from spack.version import (
    EmptyRangeError,
    GitVersion,
    StandardVersion,
    Version,
    VersionList,
    VersionLookupError,
    VersionRange,
    is_git_version,
    ver,
)
from spack.version.git_ref_lookup import SEMVER_REGEX


def assert_ver_lt(a, b):
    """Asserts the results of comparisons when 'a' is less than 'b'."""
    a, b = ver(a), ver(b)
    assert a < b
    assert a <= b
    assert a != b
    assert not a == b
    assert not a > b
    assert not a >= b


def assert_ver_gt(a, b):
    """Asserts the results of comparisons when 'a' is greater than 'b'."""
    a, b = ver(a), ver(b)
    assert a > b
    assert a >= b
    assert a != b
    assert not a == b
    assert not a < b
    assert not a <= b


def assert_ver_eq(a, b):
    """Asserts the results of comparisons when 'a' is equal to 'b'."""
    a, b = ver(a), ver(b)
    assert not a > b
    assert a >= b
    assert not a != b
    assert a == b
    assert not a < b
    assert a <= b


def assert_in(needle, haystack):
    """Asserts that 'needle' is in 'haystack'."""
    assert ver(needle) in ver(haystack)


def assert_not_in(needle, haystack):
    """Asserts that 'needle' is not in 'haystack'."""
    assert ver(needle) not in ver(haystack)


def assert_canonical(canonical_list, version_list):
    """Asserts that a redundant list is reduced to canonical form."""
    assert ver(canonical_list) == ver(version_list)


def assert_overlaps(v1, v2):
    """Asserts that two version ranges overlaps."""
    assert ver(v1).overlaps(ver(v2))


def assert_no_overlap(v1, v2):
    """Asserts that two version ranges do not overlap."""
    assert not ver(v1).overlaps(ver(v2))


def assert_satisfies(v1, v2):
    """Asserts that 'v1' satisfies 'v2'."""
    assert ver(v1).satisfies(ver(v2))


def assert_does_not_satisfy(v1, v2):
    """Asserts that 'v1' does not satisfy 'v2'."""
    assert not ver(v1).satisfies(ver(v2))


def check_intersection(expected, a, b):
    """Asserts that 'a' intersect 'b' == 'expected'."""
    assert ver(expected) == ver(a).intersection(ver(b))


def check_union(expected, a, b):
    """Asserts that 'a' union 'b' == 'expected'."""
    assert ver(expected) == ver(a).union(ver(b))


def test_string_prefix():
    assert_ver_eq("=xsdk-0.2.0", "=xsdk-0.2.0")
    assert_ver_lt("=xsdk-0.2.0", "=xsdk-0.3")
    assert_ver_gt("=xsdk-0.3", "=xsdk-0.2.0")


def test_two_segments():
    assert_ver_eq("=1.0", "=1.0")
    assert_ver_lt("=1.0", "=2.0")
    assert_ver_gt("=2.0", "=1.0")


def test_develop():
    assert_ver_eq("=develop", "=develop")
    assert_ver_eq("=develop.local", "=develop.local")
    assert_ver_lt("=1.0", "=develop")
    assert_ver_gt("=develop", "=1.0")
    assert_ver_eq("=1.develop", "=1.develop")
    assert_ver_lt("=1.1", "=1.develop")
    assert_ver_gt("=1.develop", "=1.0")
    assert_ver_gt("=0.5.develop", "=0.5")
    assert_ver_lt("=0.5", "=0.5.develop")
    assert_ver_lt("=1.develop", "=2.1")
    assert_ver_gt("=2.1", "=1.develop")
    assert_ver_lt("=1.develop.1", "=1.develop.2")
    assert_ver_gt("=1.develop.2", "=1.develop.1")
    assert_ver_lt("=develop.1", "=develop.2")
    assert_ver_gt("=develop.2", "=develop.1")
    # other +infinity versions
    assert_ver_gt("=master", "=9.0")
    assert_ver_gt("=head", "=9.0")
    assert_ver_gt("=trunk", "=9.0")
    assert_ver_gt("=develop", "=9.0")
    # hierarchical develop-like versions
    assert_ver_gt("=develop", "=master")
    assert_ver_gt("=master", "=head")
    assert_ver_gt("=head", "=trunk")
    assert_ver_gt("=9.0", "=system")
    # not develop
    assert_ver_lt("=mydevelopmentnightmare", "=1.1")
    assert_ver_lt("=1.mydevelopmentnightmare", "=1.1")
    assert_ver_gt("=1.1", "=1.mydevelopmentnightmare")


def test_isdevelop():
    assert ver("=develop").isdevelop()
    assert ver("=develop.1").isdevelop()
    assert ver("=develop.local").isdevelop()
    assert ver("=master").isdevelop()
    assert ver("=head").isdevelop()
    assert ver("=trunk").isdevelop()
    assert ver("=1.develop").isdevelop()
    assert ver("=1.develop.2").isdevelop()
    assert not ver("=1.1").isdevelop()
    assert not ver("=1.mydevelopmentnightmare.3").isdevelop()
    assert not ver("=mydevelopmentnightmare.3").isdevelop()


def test_three_segments():
    assert_ver_eq("=2.0.1", "=2.0.1")
    assert_ver_lt("=2.0", "=2.0.1")
    assert_ver_gt("=2.0.1", "=2.0")


def test_alpha():
    # TODO: not sure whether I like this.  2.0.1a is *usually*
    # TODO: less than 2.0.1, but special-casing it makes version
    # TODO: comparison complicated.  See version.py
    assert_ver_eq("=2.0.1a", "=2.0.1a")
    assert_ver_gt("=2.0.1a", "=2.0.1")
    assert_ver_lt("=2.0.1", "=2.0.1a")


def test_patch():
    assert_ver_eq("=5.5p1", "=5.5p1")
    assert_ver_lt("=5.5p1", "=5.5p2")
    assert_ver_gt("=5.5p2", "=5.5p1")
    assert_ver_eq("=5.5p10", "=5.5p10")
    assert_ver_lt("=5.5p1", "=5.5p10")
    assert_ver_gt("=5.5p10", "=5.5p1")


def test_num_alpha_with_no_separator():
    assert_ver_lt("=10xyz", "=10.1xyz")
    assert_ver_gt("=10.1xyz", "=10xyz")
    assert_ver_eq("=xyz10", "=xyz10")
    assert_ver_lt("=xyz10", "=xyz10.1")
    assert_ver_gt("=xyz10.1", "=xyz10")


def test_alpha_with_dots():
    assert_ver_eq("=xyz.4", "=xyz.4")
    assert_ver_lt("=xyz.4", "=8")
    assert_ver_gt("=8", "=xyz.4")
    assert_ver_lt("=xyz.4", "=2")
    assert_ver_gt("=2", "=xyz.4")


def test_nums_and_patch():
    assert_ver_lt("=5.5p2", "=5.6p1")
    assert_ver_gt("=5.6p1", "=5.5p2")
    assert_ver_lt("=5.6p1", "=6.5p1")
    assert_ver_gt("=6.5p1", "=5.6p1")


def test_prereleases():
    # pre-releases are special: they are less than final releases
    assert_ver_lt("=6.0alpha", "=6.0alpha0")
    assert_ver_lt("=6.0alpha0", "=6.0alpha1")
    assert_ver_lt("=6.0alpha1", "=6.0alpha2")
    assert_ver_lt("=6.0alpha2", "=6.0beta")
    assert_ver_lt("=6.0beta", "=6.0beta0")
    assert_ver_lt("=6.0beta0", "=6.0beta1")
    assert_ver_lt("=6.0beta1", "=6.0beta2")
    assert_ver_lt("=6.0beta2", "=6.0rc")
    assert_ver_lt("=6.0rc", "=6.0rc0")
    assert_ver_lt("=6.0rc0", "=6.0rc1")
    assert_ver_lt("=6.0rc1", "=6.0rc2")
    assert_ver_lt("=6.0rc2", "=6.0")


def test_alpha_beta():
    # these are not pre-releases, but ordinary string components.
    assert_ver_gt("=10b2", "=10a1")
    assert_ver_lt("=10a2", "=10b2")


def test_double_alpha():
    assert_ver_eq("=1.0aa", "=1.0aa")
    assert_ver_lt("=1.0a", "=1.0aa")
    assert_ver_gt("=1.0aa", "=1.0a")


def test_padded_numbers():
    assert_ver_eq("=10.0001", "=10.0001")
    assert_ver_eq("=10.0001", "=10.1")
    assert_ver_eq("=10.1", "=10.0001")
    assert_ver_lt("=10.0001", "=10.0039")
    assert_ver_gt("=10.0039", "=10.0001")


def test_close_numbers():
    assert_ver_lt("=4.999.9", "=5.0")
    assert_ver_gt("=5.0", "=4.999.9")


def test_date_stamps():
    assert_ver_eq("=20101121", "=20101121")
    assert_ver_lt("=20101121", "=20101122")
    assert_ver_gt("=20101122", "=20101121")


def test_underscores():
    assert_ver_eq("=2_0", "=2_0")
    assert_ver_eq("=2.0", "=2_0")
    assert_ver_eq("=2_0", "=2.0")
    assert_ver_eq("=2-0", "=2_0")
    assert_ver_eq("=2_0", "=2-0")


def test_rpm_oddities():
    assert_ver_eq("=1b.fc17", "=1b.fc17")
    assert_ver_lt("=1b.fc17", "=1.fc17")
    assert_ver_gt("=1.fc17", "=1b.fc17")
    assert_ver_eq("=1g.fc17", "=1g.fc17")
    assert_ver_gt("=1g.fc17", "=1.fc17")
    assert_ver_lt("=1.fc17", "=1g.fc17")


# Stuff below here is not taken from RPM's tests and is
# unique to spack
def test_version_ranges():
    assert_ver_lt("1.2:1.4", "1.6")
    assert_ver_gt("1.6", "1.2:1.4")
    assert_ver_eq("1.2:1.4", "1.2:1.4")
    assert ver("1.2:1.4") != ver("1.2:1.6")

    assert_ver_lt("1.2:1.4", "1.5:1.6")
    assert_ver_gt("1.5:1.6", "1.2:1.4")


def test_version_range_with_prereleases():
    # 1.2.1: means from the 1.2.1 release onwards
    assert_does_not_satisfy("1.2.1alpha1", "1.2.1:")
    assert_does_not_satisfy("1.2.1beta2", "1.2.1:")
    assert_does_not_satisfy("1.2.1rc3", "1.2.1:")

    # Pre-releases of 1.2.1 are included in the 1.2.0: range
    assert_satisfies("1.2.1alpha1", "1.2.0:")
    assert_satisfies("1.2.1beta1", "1.2.0:")
    assert_satisfies("1.2.1rc3", "1.2.0:")

    # In Spack 1.2 and 1.2.0 are distinct with 1.2 < 1.2.0. So a lowerbound on 1.2 includes
    # pre-releases of 1.2.0 as well.
    assert_satisfies("1.2.0alpha1", "1.2:")
    assert_satisfies("1.2.0beta2", "1.2:")
    assert_satisfies("1.2.0rc3", "1.2:")

    # An upperbound :1.1 does not include 1.2.0 pre-releases
    assert_does_not_satisfy("1.2.0alpha1", ":1.1")
    assert_does_not_satisfy("1.2.0beta2", ":1.1")
    assert_does_not_satisfy("1.2.0rc3", ":1.1")

    assert_satisfies("1.2.0alpha1", ":1.2")
    assert_satisfies("1.2.0beta2", ":1.2")
    assert_satisfies("1.2.0rc3", ":1.2")

    # You can also construct ranges from prereleases
    assert_satisfies("1.2.0alpha2:1.2.0beta1", "1.2.0alpha1:1.2.0beta2")
    assert_satisfies("1.2.0", "1.2.0alpha1:")
    assert_satisfies("=1.2.0", "1.2.0alpha1:")
    assert_does_not_satisfy("=1.2.0", ":1.2.0rc345")


def test_contains():
    assert_in("=1.3", "1.2:1.4")
    assert_in("=1.2.5", "1.2:1.4")
    assert_in("=1.3.5", "1.2:1.4")
    assert_in("=1.3.5-7", "1.2:1.4")
    assert_not_in("=1.1", "1.2:1.4")
    assert_not_in("=1.5", "1.2:1.4")
    assert_not_in("=1.5", "1.5.1:1.6")
    assert_not_in("=1.5", "1.5.1:")

    assert_in("=1.4.2", "1.2:1.4")
    assert_not_in("=1.4.2", "1.2:1.4.0")

    assert_in("=1.2.8", "1.2.7:1.4")
    assert_in("1.2.7:1.4", ":")
    assert_not_in("=1.2.5", "1.2.7:1.4")

    assert_in("=1.4.1", "1.2.7:1.4")
    assert_not_in("=1.4.1", "1.2.7:1.4.0")


def test_in_list():
    assert_in("1.2", ["1.5", "1.2", "1.3"])
    assert_in("1.2.5", ["1.5", "1.2:1.3"])
    assert_in("1.5", ["1.5", "1.2:1.3"])
    assert_not_in("1.4", ["1.5", "1.2:1.3"])

    assert_in("1.2.5:1.2.7", [":"])
    assert_in("1.2.5:1.2.7", ["1.5", "1.2:1.3"])
    assert_not_in("1.2.5:1.5", ["1.5", "1.2:1.3"])
    assert_not_in("1.1:1.2.5", ["1.5", "1.2:1.3"])


def test_ranges_overlap():
    assert_overlaps("1.2", "1.2")
    assert_overlaps("1.2.1", "1.2.1")
    assert_overlaps("1.2.1b", "1.2.1b")

    assert_overlaps("1.2:1.7", "1.6:1.9")
    assert_overlaps(":1.7", "1.6:1.9")
    assert_overlaps(":1.7", ":1.9")
    assert_overlaps(":1.7", "1.6:")
    assert_overlaps("1.2:", "1.6:1.9")
    assert_overlaps("1.2:", ":1.9")
    assert_overlaps("1.2:", "1.6:")
    assert_overlaps(":", ":")
    assert_overlaps(":", "1.6:1.9")
    assert_overlaps("1.6:1.9", ":")


def test_overlap_with_containment():
    assert_in("1.6.5", "1.6")
    assert_in("1.6.5", ":1.6")

    assert_overlaps("1.6.5", ":1.6")
    assert_overlaps(":1.6", "1.6.5")

    assert_not_in(":1.6", "1.6.5")
    assert_in("1.6.5", ":1.6")


def test_lists_overlap():
    assert_overlaps("1.2b:1.7,5", "1.6:1.9,1")
    assert_overlaps("1,2,3,4,5", "3,4,5,6,7")
    assert_overlaps("1,2,3,4,5", "5,6,7")
    assert_overlaps("1,2,3,4,5", "5:7")
    assert_overlaps("1,2,3,4,5", "3, 6:7")
    assert_overlaps("1, 2, 4, 6.5", "3, 6:7")
    assert_overlaps("1, 2, 4, 6.5", ":, 5, 8")
    assert_overlaps("1, 2, 4, 6.5", ":")
    assert_no_overlap("1, 2, 4", "3, 6:7")
    assert_no_overlap("1,2,3,4,5", "6,7")
    assert_no_overlap("1,2,3,4,5", "6:7")


def test_canonicalize_list():
    assert_canonical(["1.2", "1.3", "1.4"], ["1.2", "1.3", "1.3", "1.4"])

    assert_canonical(["1.2", "1.3:1.4"], ["1.2", "1.3", "1.3:1.4"])

    assert_canonical(["1.2", "1.3:1.4"], ["1.2", "1.3:1.4", "1.4"])

    assert_canonical(["1.3:1.4"], ["1.3:1.4", "1.3", "1.3.1", "1.3.9", "1.4"])

    assert_canonical(["1.3:1.4"], ["1.3", "1.3.1", "1.3.9", "1.4", "1.3:1.4"])

    assert_canonical(["1.3:1.5"], ["1.3", "1.3.1", "1.3.9", "1.4:1.5", "1.3:1.4"])

    assert_canonical(["1.3:1.5"], ["1.3, 1.3.1,1.3.9,1.4:1.5,1.3:1.4"])

    assert_canonical(["1.3:1.5"], ["1.3, 1.3.1,1.3.9,1.4 : 1.5 , 1.3 : 1.4"])

    assert_canonical([":"], [":,1.3, 1.3.1,1.3.9,1.4 : 1.5 , 1.3 : 1.4"])


def test_intersection():
    check_intersection("2.5", "1.0:2.5", "2.5:3.0")
    check_intersection("2.5:2.7", "1.0:2.7", "2.5:3.0")
    check_intersection("0:1", ":", "0:1")

    check_intersection(["1.0", "2.5:2.7"], ["1.0:2.7"], ["2.5:3.0", "1.0"])
    check_intersection(["2.5:2.7"], ["1.1:2.7"], ["2.5:3.0", "1.0"])
    check_intersection(["0:1"], [":"], ["0:1"])

    check_intersection(["=ref=1.0", "=1.1"], ["=ref=1.0", "1.1"], ["1:1.0", "=1.1"])


def test_intersect_with_containment():
    check_intersection("1.6.5", "1.6.5", ":1.6")
    check_intersection("1.6.5", ":1.6", "1.6.5")

    check_intersection("1.6:1.6.5", ":1.6.5", "1.6")
    check_intersection("1.6:1.6.5", "1.6", ":1.6.5")

    check_intersection("11.2", "11", "11.2")
    check_intersection("11.2", "11.2", "11")


def test_union_with_containment():
    check_union(":1.6", "1.6.5", ":1.6")
    check_union(":1.6", ":1.6", "1.6.5")

    check_union(":1.6", ":1.6.5", "1.6")
    check_union(":1.6", "1.6", ":1.6.5")

    check_union(":", "1.0:", ":2.0")

    check_union("1:4", "1:3", "2:4")
    check_union("1:4", "2:4", "1:3")

    # Tests successor/predecessor case.
    check_union("1:4", "1:2", "3:4")

    check_union(["1:1.0", "1.1"], ["=ref=1.0", "1.1"], ["1:1.0", "=1.1"])


def test_basic_version_satisfaction():
    assert_satisfies("4.7.3", "4.7.3")

    assert_satisfies("4.7.3", "4.7")
    assert_satisfies("4.7.3v2", "4.7")
    assert_satisfies("4.7v6", "4.7")

    assert_satisfies("4.7.3", "4")
    assert_satisfies("4.7.3v2", "4")
    assert_satisfies("4.7v6", "4")

    assert_does_not_satisfy("4.8.0", "4.9")
    assert_does_not_satisfy("4.8", "4.9")
    assert_does_not_satisfy("4", "4.9")


def test_basic_version_satisfaction_in_lists():
    assert_satisfies(["4.7.3"], ["4.7.3"])

    assert_satisfies(["4.7.3"], ["4.7"])
    assert_satisfies(["4.7.3v2"], ["4.7"])
    assert_satisfies(["4.7v6"], ["4.7"])

    assert_satisfies(["4.7.3"], ["4"])
    assert_satisfies(["4.7.3v2"], ["4"])
    assert_satisfies(["4.7v6"], ["4"])

    assert_does_not_satisfy(["4.8.0"], ["4.9"])
    assert_does_not_satisfy(["4.8"], ["4.9"])
    assert_does_not_satisfy(["4"], ["4.9"])


def test_version_range_satisfaction():
    assert_satisfies("4.7b6", "4.3:4.7")
    assert_satisfies("4.3.0", "4.3:4.7")
    assert_satisfies("4.3.2", "4.3:4.7")

    assert_does_not_satisfy("4.8.0", "4.3:4.7")
    assert_does_not_satisfy("4.3", "4.4:4.7")

    assert_satisfies("4.7b6", "4.3:4.7")
    assert_does_not_satisfy("4.8.0", "4.3:4.7")


def test_version_range_satisfaction_in_lists():
    assert_satisfies(["4.7b6"], ["4.3:4.7"])
    assert_satisfies(["4.3.0"], ["4.3:4.7"])
    assert_satisfies(["4.3.2"], ["4.3:4.7"])

    assert_does_not_satisfy(["4.8.0"], ["4.3:4.7"])
    assert_does_not_satisfy(["4.3"], ["4.4:4.7"])

    assert_satisfies(["4.7b6"], ["4.3:4.7"])
    assert_does_not_satisfy(["4.8.0"], ["4.3:4.7"])


def test_satisfaction_with_lists():
    assert_satisfies("4.7", "4.3, 4.6, 4.7")
    assert_satisfies("4.7.3", "4.3, 4.6, 4.7")
    assert_satisfies("4.6.5", "4.3, 4.6, 4.7")
    assert_satisfies("4.6.5.2", "4.3, 4.6, 4.7")

    assert_does_not_satisfy("4", "4.3, 4.6, 4.7")
    assert_does_not_satisfy("4.8.0", "4.2, 4.3:4.7")

    assert_satisfies("4.8.0", "4.2, 4.3:4.8")
    assert_satisfies("4.8.2", "4.2, 4.3:4.8")


def test_formatted_strings():
    versions = (
        "1.2.3b",
        "1_2_3b",
        "1-2-3b",
        "1.2-3b",
        "1.2_3b",
        "1-2.3b",
        "1-2_3b",
        "1_2.3b",
        "1_2-3b",
    )
    for item in versions:
        v = Version(item)
        assert v.dotted.string == "1.2.3b"
        assert v.dashed.string == "1-2-3b"
        assert v.underscored.string == "1_2_3b"
        assert v.joined.string == "123b"

        assert v.dotted.dashed.string == "1-2-3b"
        assert v.dotted.underscored.string == "1_2_3b"
        assert v.dotted.dotted.string == "1.2.3b"
        assert v.dotted.joined.string == "123b"


def test_dotted_numeric_string():
    assert Version("1a2b3").dotted_numeric_string == "1.0.2.0.3"
    assert Version("1a2b3alpha4").dotted_numeric_string == "1.0.2.0.3.0.4"


def test_up_to():
    v = Version("1.23-4_5b")

    assert v.up_to(1).string == "1"
    assert v.up_to(2).string == "1.23"
    assert v.up_to(3).string == "1.23-4"
    assert v.up_to(4).string == "1.23-4_5"
    assert v.up_to(5).string == "1.23-4_5b"

    assert v.up_to(-1).string == "1.23-4_5"
    assert v.up_to(-2).string == "1.23-4"
    assert v.up_to(-3).string == "1.23"
    assert v.up_to(-4).string == "1"

    assert v.up_to(2).dotted.string == "1.23"
    assert v.up_to(2).dashed.string == "1-23"
    assert v.up_to(2).underscored.string == "1_23"
    assert v.up_to(2).joined.string == "123"

    assert v.dotted.up_to(2).string == "1.23" == v.up_to(2).dotted.string
    assert v.dashed.up_to(2).string == "1-23" == v.up_to(2).dashed.string
    assert v.underscored.up_to(2).string == "1_23"
    assert v.up_to(2).underscored.string == "1_23"

    assert v.up_to(2).up_to(1).string == "1"


def test_repr_and_str():
    def check_repr_and_str(vrs):
        a = Version(vrs)
        assert repr(a) == f'Version("{vrs}")'
        b = eval(repr(a))
        assert a == b
        assert str(a) == vrs
        assert str(a) == str(b)

    check_repr_and_str("1.2.3")
    check_repr_and_str("R2016a")
    check_repr_and_str("R2016a.2-3_4")


@pytest.mark.parametrize(
    "version_str", ["1.2string3", "1.2-3xyz_4-alpha.5", "1.2beta", "1_x_rc-4"]
)
def test_stringify_version(version_str):
    v = Version(version_str)
    v.string = None
    assert str(v) == version_str


def test_len():
    a = Version("1.2.3.4")
    assert len(a) == len(a.version[0])
    assert len(a) == 4
    b = Version("2018.0")
    assert len(b) == 2


def test_get_item():
    a = Version("0.1_2-3")
    assert isinstance(a[1], int)
    # Test slicing
    b = a[0:2]
    assert isinstance(b, StandardVersion)
    assert b == Version("0.1")
    assert repr(b) == 'Version("0.1")'
    assert str(b) == "0.1"
    b = a[0:3]
    assert isinstance(b, StandardVersion)
    assert b == Version("0.1_2")
    assert repr(b) == 'Version("0.1_2")'
    assert str(b) == "0.1_2"
    b = a[1:]
    assert isinstance(b, StandardVersion)
    assert b == Version("1_2-3")
    assert repr(b) == 'Version("1_2-3")'
    assert str(b) == "1_2-3"
    # Raise TypeError on tuples
    with pytest.raises(TypeError):
        b.__getitem__(1, 2)


def test_list_highest():
    vl = VersionList(["=master", "=1.2.3", "=develop", "=3.4.5", "=foobar"])
    assert vl.highest() == Version("develop")
    assert vl.lowest() == Version("foobar")
    assert vl.highest_numeric() == Version("3.4.5")

    vl2 = VersionList(["=master", "=develop"])
    assert vl2.highest_numeric() is None
    assert vl2.preferred() == Version("develop")
    assert vl2.lowest() == Version("master")


@pytest.mark.parametrize("version_str", ["foo 1.2.0", "!", "1!2", "=1.2.0"])
def test_invalid_versions(version_str):
    """Ensure invalid versions are rejected with a ValueError"""
    with pytest.raises(ValueError):
        Version(version_str)


def test_versions_from_git(git, mock_git_version_info, monkeypatch, mock_packages):
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", pathlib.Path(repo_path).as_uri(), raising=False
    )

    for commit in commits:
        spec = spack.spec.Spec("git-test-commit@%s" % commit)
        version: GitVersion = spec.version
        comparator = [str(v) if not isinstance(v, int) else v for v in version.ref_version]

        with working_dir(repo_path):
            git("checkout", commit)

        with open(os.path.join(repo_path, filename), "r") as f:
            expected = f.read()

        assert str(comparator) == expected


@pytest.mark.parametrize(
    "commit_idx,expected_satisfies,expected_not_satisfies",
    [
        # Spec based on earliest commit
        (-1, ("@:0",), ("@1.0",)),
        # Spec based on second commit (same as version 1.0)
        (-2, ("@1.0",), ("@1.1:",)),
        # Spec based on 4th commit (in timestamp order)
        (-4, ("@1.1", "@1.0:1.2"), tuple()),
    ],
)
def test_git_hash_comparisons(
    mock_git_version_info,
    install_mockery,
    mock_packages,
    monkeypatch,
    commit_idx,
    expected_satisfies,
    expected_not_satisfies,
):
    """Check that hashes compare properly to versions"""
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", pathlib.Path(repo_path).as_uri(), raising=False
    )

    spec = spack.spec.Spec(f"git-test-commit@{commits[commit_idx]}").concretized()
    for item in expected_satisfies:
        assert spec.satisfies(item)

    for item in expected_not_satisfies:
        assert not spec.satisfies(item)


def test_git_ref_comparisons(mock_git_version_info, install_mockery, mock_packages, monkeypatch):
    """Check that hashes compare properly to versions"""
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", pathlib.Path(repo_path).as_uri(), raising=False
    )

    # Spec based on tag v1.0
    spec_tag = spack.spec.Spec("git-test-commit@git.v1.0")
    spec_tag.concretize()
    assert spec_tag.satisfies("@1.0")
    assert not spec_tag.satisfies("@1.1:")
    assert str(spec_tag.version) == "git.v1.0=1.0"

    # Spec based on branch 1.x
    spec_branch = spack.spec.Spec("git-test-commit@git.1.x")
    spec_branch.concretize()
    assert spec_branch.satisfies("@1.2")
    assert spec_branch.satisfies("@1.1:1.3")
    assert str(spec_branch.version) == "git.1.x=1.2"


def test_git_branch_with_slash():
    class MockLookup(object):
        def get(self, ref):
            assert ref == "feature/bar"
            return "1.2", 0

    v = spack.version.from_string("git.feature/bar")
    assert isinstance(v, GitVersion)
    v.attach_lookup(MockLookup())

    # Create a version range
    test_number_version = spack.version.from_string("1.2")
    v.satisfies(test_number_version)

    serialized = VersionList([v]).to_dict()
    v_deserialized = VersionList.from_dict(serialized)
    assert v_deserialized[0].ref == "feature/bar"


@pytest.mark.parametrize(
    "string,git",
    [
        ("1.2.9", False),
        ("gitmain", False),
        ("git.foo", True),
        ("git.abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd", True),
        ("abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd", True),
    ],
)
def test_version_git_vs_base(string, git):
    assert is_git_version(string) == git
    assert isinstance(Version(string), GitVersion) == git


def test_version_range_nonempty():
    assert Version("1.2.9") in VersionRange("1.2.0", "1.2")
    assert Version("1.1.1") in ver("1.0:1")


def test_empty_version_range_raises():
    with pytest.raises(EmptyRangeError, match="2:1.0 is an empty range"):
        assert VersionRange("2", "1.0")
    with pytest.raises(EmptyRangeError, match="2:1.0 is an empty range"):
        assert ver("2:1.0")


def test_version_empty_slice():
    """Check an empty slice to confirm get "empty" version instead of
    an IndexError (#25953).
    """
    assert Version("1.")[1:] == Version("")


def test_version_wrong_idx_type():
    """Ensure exception raised if attempt to use non-integer index."""
    v = Version("1.1")
    with pytest.raises(TypeError):
        v["0:"]


@pytest.mark.regression("29170")
def test_version_range_satisfies_means_nonempty_intersection():
    x = VersionRange("3.7.0", "3")
    y = VersionRange("3.6.0", "3.6.0")
    assert not x.satisfies(y)
    assert not y.satisfies(x)


def test_version_list_with_range_and_concrete_version_is_not_concrete():
    v = VersionList([Version("3.1"), VersionRange(Version("3.1.1"), Version("3.1.2"))])
    assert not v.concrete


@pytest.mark.parametrize(
    "vstring, eq_vstring, is_commit",
    (
        ("abc12" * 8 + "=develop", "develop", True),
        ("git." + "abc12" * 8 + "=main", "main", True),
        ("a" * 40 + "=develop", "develop", True),
        ("b" * 40 + "=3.2", "3.2", True),
        ("git.foo=3.2", "3.2", False),
    ),
)
def test_git_ref_can_be_assigned_a_version(vstring, eq_vstring, is_commit):
    v = Version(vstring)
    v_equivalent = Version(eq_vstring)
    assert v.is_commit == is_commit
    assert not v._ref_lookup
    assert v_equivalent == v.ref_version


@pytest.mark.parametrize(
    "lhs_str,rhs_str,expected",
    [
        # StandardVersion
        ("4.7.3", "4.7.3", (True, True, True)),
        ("4.7.3", "4.7", (True, True, False)),
        ("4.7.3", "4", (True, True, False)),
        ("4.7.3", "4.8", (False, False, False)),
        # GitVersion
        (f"git.{'a' * 40}=develop", "develop", (True, True, False)),
        (f"git.{'a' * 40}=develop", f"git.{'a' * 40}=develop", (True, True, True)),
        (f"git.{'a' * 40}=develop", f"git.{'b' * 40}=develop", (False, False, False)),
    ],
)
def test_version_intersects_satisfies_semantic(lhs_str, rhs_str, expected):
    lhs, rhs = ver(lhs_str), ver(rhs_str)
    intersect, lhs_sat_rhs, rhs_sat_lhs = expected

    assert lhs.intersects(rhs) is intersect
    assert lhs.intersects(rhs) is rhs.intersects(lhs)
    assert lhs.satisfies(rhs) is lhs_sat_rhs
    assert rhs.satisfies(lhs) is rhs_sat_lhs


@pytest.mark.parametrize(
    "spec_str,tested_intersects,tested_satisfies",
    [
        (
            "git-test-commit@git.1.x",
            [("@:2", True), ("@:1", True), ("@:0", False), ("@1.3:", False)],
            [("@:2", True), ("@:1", True), ("@:0", False), ("@1.3:", False)],
        ),
        (
            "git-test-commit@git.v2.0",
            [("@:2", True), ("@:1", False), ("@:0", False), ("@1.3:", True)],
            [("@:2", True), ("@:1", False), ("@:0", False), ("@1.3:", True)],
        ),
    ],
)
def test_git_versions_without_explicit_reference(
    spec_str,
    tested_intersects,
    tested_satisfies,
    mock_git_version_info,
    mock_packages,
    monkeypatch,
):
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", pathlib.Path(repo_path).as_uri(), raising=False
    )
    spec = spack.spec.Spec(spec_str)

    for test_str, expected in tested_intersects:
        assert spec.intersects(test_str) is expected, test_str

    for test_str, expected in tested_intersects:
        assert spec.intersects(test_str) is expected, test_str


def test_total_order_versions_and_ranges():
    # The set of version ranges and individual versions are comparable, which is used in
    # VersionList. The comparsion across types is based on default version comparsion
    # of StandardVersion, GitVersion.ref_version, and ClosedOpenRange.lo.

    # StandardVersion / GitVersion (at equal ref version)
    assert_ver_lt("=1.2", "git.ref=1.2")
    assert_ver_gt("git.ref=1.2", "=1.2")

    # StandardVersion / GitVersion (at different ref versions)
    assert_ver_lt("git.ref=1.2", "=1.3")
    assert_ver_gt("=1.3", "git.ref=1.2")
    assert_ver_lt("=1.2", "git.ref=1.3")
    assert_ver_gt("git.ref=1.3", "=1.2")

    # GitVersion / ClosedOpenRange (at equal ref/lo version)
    assert_ver_lt("git.ref=1.2", "1.2")
    assert_ver_gt("1.2", "git.ref=1.2")

    # GitVersion / ClosedOpenRange (at different ref/lo version)
    assert_ver_lt("git.ref=1.2", "1.3")
    assert_ver_gt("1.3", "git.ref=1.2")
    assert_ver_lt("1.2", "git.ref=1.3")
    assert_ver_gt("git.ref=1.3", "1.2")

    # StandardVersion / ClosedOpenRange (at equal lo version)
    assert_ver_lt("=1.2", "1.2")
    assert_ver_gt("1.2", "=1.2")

    # StandardVersion / ClosedOpenRange (at different lo version)
    assert_ver_lt("=1.2", "1.3")
    assert_ver_gt("1.3", "=1.2")
    assert_ver_lt("1.2", "=1.3")
    assert_ver_gt("=1.3", "1.2")


def test_git_version_accessors():
    """Test whether iteration, indexing, slicing, dotted, dashed, and underscored works for
    GitVersion."""
    v = GitVersion("my_branch=1.2-3")
    assert [x for x in v] == [1, 2, 3]
    assert v[0] == 1
    assert v[1] == 2
    assert v[2] == 3
    assert v[0:2] == Version("1.2")
    assert v[0:10] == Version("1.2.3")
    assert str(v.dotted) == "1.2.3"
    assert str(v.dashed) == "1-2-3"
    assert str(v.underscored) == "1_2_3"
    assert v.up_to(1) == Version("1")
    assert v.up_to(2) == Version("1.2")
    assert len(v) == 3
    assert not v.isdevelop()
    assert GitVersion("my_branch=develop").isdevelop()


def test_boolness_of_versions():
    # We do implement __len__, but at the end of the day versions are used as elements in
    # the first place, not as lists of version components. So VersionList(...).concrete
    # should be truthy even when there are no version components.
    assert bool(Version("1.2"))
    assert bool(Version("1.2").up_to(0))

    # bool(GitVersion) shouldn't trigger a ref lookup.
    assert bool(GitVersion("a" * 40))


def test_version_list_normalization():
    # Git versions and ordinary versions can live together in a VersionList
    assert len(VersionList(["=1.2", "ref=1.2"])) == 2

    # But when a range is added, the only disjoint bit is the range.
    assert VersionList(["=1.2", "ref=1.2", "ref=1.3", "1.2:1.3"]) == VersionList(["1.2:1.3"])

    # Also test normalization when using ver.
    assert ver("=1.0,ref=1.0,1.0:2.0") == ver(["1.0:2.0"])
    assert ver("=1.0,1.0:2.0,ref=1.0") == ver(["1.0:2.0"])
    assert ver("1.0:2.0,=1.0,ref=1.0") == ver(["1.0:2.0"])


def test_version_list_connected_union_of_disjoint_ranges():
    # Make sure that we also simplify lists of ranges if their intersection is empty, but their
    # union is connected.
    assert ver("1.0:2.0,2.1,2.2:3,4:6") == ver(["1.0:6"])
    assert ver("1.0:1.2,1.3:2") == ver("1.0:1.5,1.6:2")


@pytest.mark.parametrize("version", ["=1.2", "git.ref=1.2", "1.2"])
def test_version_comparison_with_list_fails(version):
    vlist = VersionList(["=1.3"])

    with pytest.raises(TypeError):
        version < vlist

    with pytest.raises(TypeError):
        vlist < version

    with pytest.raises(TypeError):
        version <= vlist

    with pytest.raises(TypeError):
        vlist <= version

    with pytest.raises(TypeError):
        version >= vlist

    with pytest.raises(TypeError):
        vlist >= version

    with pytest.raises(TypeError):
        version > vlist

    with pytest.raises(TypeError):
        vlist > version


def test_inclusion_upperbound():
    is_specific = spack.spec.Spec("x@=1.2")
    is_range = spack.spec.Spec("x@1.2")
    upperbound = spack.spec.Spec("x@:1.2.0")

    # The exact version is included in the range
    assert is_specific.satisfies(upperbound)

    # But the range 1.2:1.2 is not, since it includes for example 1.2.1
    assert not is_range.satisfies(upperbound)

    # They do intersect of course.
    assert is_specific.intersects(upperbound) and is_range.intersects(upperbound)


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_git_version_repo_attached_after_serialization(
    mock_git_version_info, mock_packages, config, monkeypatch
):
    """Test that a GitVersion instance can be serialized and deserialized
    without losing its repository reference.
    """
    repo_path, _, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", "file://%s" % repo_path, raising=False
    )
    spec = spack.spec.Spec(f"git-test-commit@{commits[-2]}").concretized()

    # Before serialization, the repo is attached
    assert spec.satisfies("@1.0")

    # After serialization, the repo is still attached
    assert spack.spec.Spec.from_dict(spec.to_dict()).satisfies("@1.0")


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_resolved_git_version_is_shown_in_str(
    mock_git_version_info, mock_packages, config, monkeypatch
):
    """Test that a GitVersion from a commit without a user supplied version is printed
    as <hash>=<version>, and not just <hash>."""
    repo_path, _, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", "file://%s" % repo_path, raising=False
    )
    commit = commits[-3]
    spec = spack.spec.Spec(f"git-test-commit@{commit}").concretized()

    assert spec.version.satisfies(ver("1.0"))
    assert str(spec.version) == f"{commit}=1.0-git.1"


def test_unresolvable_git_versions_error(config, mock_packages):
    """Test that VersionLookupError is raised when a git prop is not set on a package."""
    with pytest.raises(VersionLookupError):
        # The package exists, but does not have a git property set. When dereferencing
        # the version, we should get VersionLookupError, not a generic AttributeError.
        spack.spec.Spec(f"git-test-commit@{'a' * 40}").version.ref_version


@pytest.mark.parametrize(
    "tag,expected",
    [
        ("v100.2.3", "100.2.3"),
        ("v1.2.3", "1.2.3"),
        ("v1.2.3-pre.release+build.1", "1.2.3-pre.release+build.1"),
        ("v1.2.3+build.1", "1.2.3+build.1"),
        ("v1.2.3+build_1", None),
        ("v1.2.3-pre.release", "1.2.3-pre.release"),
        ("v1.2.3-pre_release", None),
        ("1.2.3", "1.2.3"),
        ("1.2.3.", None),
    ],
)
def test_semver_regex(tag, expected):
    result = SEMVER_REGEX.search(tag)
    if expected is None:
        assert result is None
    else:
        assert result.group() == expected
