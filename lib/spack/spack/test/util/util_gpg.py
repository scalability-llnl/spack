# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.util.gpg


@pytest.fixture()
def has_socket_dir():
    spack.util.gpg.init()
    return bool(spack.util.gpg.SOCKET_DIR)


def test_parse_gpg_output_case_one():
    # Two keys, fingerprint for primary keys, but not subkeys
    output = """sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
"""
    keys = spack.util.gpg._parse_secret_keys_output(output)

    assert len(keys) == 2
    assert keys[0] == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    assert keys[1] == "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"


def test_parse_gpg_output_case_two():
    # One key, fingerprint for primary key as well as subkey
    output = """sec:-:2048:1:AAAAAAAAAA:AAAAAAAA:::-:::escaESCA:::+:::23::0:
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
grp:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
uid:-::::AAAAAAAAA::AAAAAAAAA::Joe (Test) <j.s@s.com>::::::::::0:
ssb:-:2048:1:AAAAAAAAA::::::esa:::+:::23:
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
grp:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
"""
    keys = spack.util.gpg._parse_secret_keys_output(output)

    assert len(keys) == 1
    assert keys[0] == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


def test_parse_gpg_output_case_three():
    # Two keys, fingerprint for primary keys as well as subkeys
    output = """sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
fpr:::::::::ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ:"""

    keys = spack.util.gpg._parse_secret_keys_output(output)

    assert len(keys) == 2
    assert keys[0] == "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    assert keys[1] == "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"


@pytest.mark.requires_executables("gpg2")
def test_really_long_gnupghome_dir(tmpdir, has_socket_dir):
    if not has_socket_dir:
        pytest.skip("This test requires /var/run/user/$(id -u)")

    N = 960
    tdir = str(tmpdir)
    while len(tdir) < N:
        tdir = os.path.join(tdir, "filler")

    tdir = tdir[:N].rstrip(os.sep)
    tdir += "0" * (N - len(tdir))

    with spack.util.gpg.gnupghome_override(tdir):
        spack.util.gpg.create(
            name="Spack testing 1", email="test@spack.io", comment="Spack testing key", expires="0"
        )
        spack.util.gpg.list(True, True)
