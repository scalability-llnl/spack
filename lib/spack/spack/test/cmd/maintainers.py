# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

import spack.main
import spack.repo

maintainers = spack.main.SpackCommand("maintainers")

MAINTAINED_PACKAGES = ["maintainers-1", "maintainers-2", "maintainers-3", "py-extension1"]


def split(output):
    """Split command line output into an array."""
    output = output.strip()
    return re.split(r"\s+", output) if output else []


def test_maintained(mock_packages):
    out = split(maintainers("--maintained"))
    assert out == MAINTAINED_PACKAGES


def test_unmaintained(mock_packages):
    out = split(maintainers("--unmaintained"))
    assert out == sorted(set(spack.repo.all_package_names()) - set(MAINTAINED_PACKAGES))


def test_all(mock_packages, capfd):
    with capfd.disabled():
        out = split(maintainers("--all"))
    assert out == [
        "maintainers-1:",
        "user1,",
        "user2",
        "maintainers-2:",
        "user2,",
        "user3",
        "maintainers-3:",
        "user0,",
        "user1,",
        "user2,",
        "user3",
        "py-extension1:",
        "user1,",
        "user2",
    ]

    with capfd.disabled():
        out = split(maintainers("--all", "maintainers-1"))
    assert out == ["maintainers-1:", "user1,", "user2"]


def test_all_by_user(mock_packages, capfd):
    with capfd.disabled():
        out = split(maintainers("--all", "--by-user"))
    assert out == [
        "user0:",
        "maintainers-3",
        "user1:",
        "maintainers-1,",
        "maintainers-3,",
        "py-extension1",
        "user2:",
        "maintainers-1,",
        "maintainers-2,",
        "maintainers-3,",
        "py-extension1",
        "user3:",
        "maintainers-2,",
        "maintainers-3",
    ]

    with capfd.disabled():
        out = split(maintainers("--all", "--by-user", "user1", "user2"))
    assert out == [
        "user1:",
        "maintainers-1,",
        "maintainers-3,",
        "py-extension1",
        "user2:",
        "maintainers-1,",
        "maintainers-2,",
        "maintainers-3,",
        "py-extension1",
    ]


def test_no_args(mock_packages):
    with pytest.raises(spack.main.SpackCommandError):
        maintainers()


def test_no_args_by_user(mock_packages):
    with pytest.raises(spack.main.SpackCommandError):
        maintainers("--by-user")


def test_mutex_args_fail(mock_packages):
    with pytest.raises(SystemExit):
        maintainers("--maintained", "--unmaintained")


def test_maintainers_list_packages(mock_packages, capfd):
    with capfd.disabled():
        out = split(maintainers("maintainers-1"))
    assert out == ["user1", "user2"]

    with capfd.disabled():
        out = split(maintainers("maintainers-1", "maintainers-2"))
    assert out == ["user1", "user2", "user3"]

    with capfd.disabled():
        out = split(maintainers("maintainers-2"))
    assert out == ["user2", "user3"]


def test_maintainers_list_fails(mock_packages, capfd):
    out = maintainers("pkg-a", fail_on_error=False)
    assert not out
    assert maintainers.returncode == 1


def test_maintainers_list_by_user(mock_packages, capfd):
    with capfd.disabled():
        out = split(maintainers("--by-user", "user1"))
    assert out == ["maintainers-1", "maintainers-3", "py-extension1"]

    with capfd.disabled():
        out = split(maintainers("--by-user", "user1", "user2"))
    assert out == ["maintainers-1", "maintainers-2", "maintainers-3", "py-extension1"]

    with capfd.disabled():
        out = split(maintainers("--by-user", "user2"))
    assert out == ["maintainers-1", "maintainers-2", "maintainers-3", "py-extension1"]

    with capfd.disabled():
        out = split(maintainers("--by-user", "user3"))
    assert out == ["maintainers-2", "maintainers-3"]
