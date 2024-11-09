# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import pytest

import archspec.cpu

import spack.concretize
import spack.operating_systems
import spack.platforms
from spack.spec import ArchSpec, Spec


@pytest.fixture(scope="module")
def current_host_platform():
    """Return the platform of the current host as detected by the
    'platform' stdlib package.
    """
    current_platform = None
    if "Linux" in platform.system():
        current_platform = spack.platforms.Linux()
    elif "Darwin" in platform.system():
        current_platform = spack.platforms.Darwin()
    elif "Windows" in platform.system():
        current_platform = spack.platforms.Windows()
    elif "FreeBSD" in platform.system():
        current_platform = spack.platforms.FreeBSD()
    return current_platform


# Valid keywords for os=xxx or target=xxx
VALID_KEYWORDS = ["fe", "be", "frontend", "backend"]

TEST_PLATFORM = spack.platforms.Test()


@pytest.fixture(params=([str(x) for x in TEST_PLATFORM.targets] + VALID_KEYWORDS), scope="module")
def target_str(request):
    """All the possible strings that can be used for targets"""
    return request.param


@pytest.fixture(
    params=([str(x) for x in TEST_PLATFORM.operating_sys] + VALID_KEYWORDS), scope="module"
)
def os_str(request):
    """All the possible strings that can be used for operating systems"""
    return request.param


def test_platform(current_host_platform):
    """Check that current host detection return the correct platform"""
    detected_platform = spack.platforms.real_host()
    assert str(detected_platform) == str(current_host_platform)


def test_user_input_combination(config, target_str, os_str):
    """Test for all the valid user input combinations that both the target and
    the operating system match.
    """
    spec_str = "libelf os={} target={}".format(os_str, target_str)
    spec = Spec(spec_str)
    assert spec.architecture.os == str(TEST_PLATFORM.operating_system(os_str))
    assert spec.architecture.target == TEST_PLATFORM.target(target_str)


def test_default_os_and_target(default_mock_concretization):
    """Test that is we don't specify `os=` or `target=` we get the default values
    after concretization.
    """
    spec = default_mock_concretization("libelf")
    assert spec.architecture.os == str(TEST_PLATFORM.operating_system("default_os"))
    assert spec.architecture.target == TEST_PLATFORM.target("default_target")


def test_operating_system_conversion_to_dict():
    operating_system = spack.operating_systems.OperatingSystem("os", "1.0")
    assert operating_system.to_dict() == {"name": "os", "version": "1.0"}


@pytest.mark.parametrize(
    "item,architecture_str",
    [
        # We can search the architecture string representation
        ("linux", "linux-ubuntu18.04-haswell"),
        ("ubuntu", "linux-ubuntu18.04-haswell"),
        ("haswell", "linux-ubuntu18.04-haswell"),
        # We can also search flags of the target,
        ("avx512", "linux-ubuntu18.04-icelake"),
    ],
)
def test_arch_spec_container_semantic(item, architecture_str):
    architecture = ArchSpec(architecture_str)
    assert item in architecture


@pytest.mark.regression("15306")
@pytest.mark.parametrize(
    "architecture_tuple,constraint_tuple",
    [
        (("linux", "ubuntu18.04", None), ("linux", None, "x86_64")),
        (("linux", "ubuntu18.04", None), ("linux", None, "x86_64:")),
    ],
)
def test_satisfy_strict_constraint_when_not_concrete(architecture_tuple, constraint_tuple):
    architecture = ArchSpec(architecture_tuple)
    constraint = ArchSpec(constraint_tuple)
    assert not architecture.satisfies(constraint)


@pytest.mark.parametrize(
    "root_target_range,dep_target_range,result",
    [
        ("x86_64:nocona", "x86_64:core2", "nocona"),  # pref not in intersection
        ("x86_64:core2", "x86_64:nocona", "nocona"),
        ("x86_64:haswell", "x86_64:mic_knl", "core2"),  # pref in intersection
        ("ivybridge", "nocona:skylake", "ivybridge"),  # one side concrete
        ("haswell:icelake", "broadwell", "broadwell"),
        # multiple ranges in lists with multiple overlaps
        ("x86_64:nocona,haswell:broadwell", "nocona:haswell,skylake:", "nocona"),
        # lists with concrete targets, lists compared to ranges
        ("x86_64,haswell", "core2:broadwell", "haswell"),
    ],
)
@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.skipif(
    str(archspec.cpu.host().family) != "x86_64", reason="tests are for x86_64 uarch ranges"
)
def test_concretize_target_ranges(root_target_range, dep_target_range, result, monkeypatch):
    spec = Spec(
        f"pkg-a %gcc@10 foobar=bar target={root_target_range} ^pkg-b target={dep_target_range}"
    )
    with spack.concretize.disable_compiler_existence_check():
        spec.concretize()
    assert spec.target == spec["pkg-b"].target == result
