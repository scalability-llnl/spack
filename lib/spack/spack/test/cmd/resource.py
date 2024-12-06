# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

from spack.main import SpackCommand

resource = SpackCommand("resource")

#: these are hashes used in mock packages
mock_hashes = (
    [
        "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
        "1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd",
        "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
        "c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8",
        "24eceabef5fe8f575ff4b438313dc3e7b30f6a2d1c78841fbbe3b9293a589277",
        "689b8f9b32cb1d2f9271d29ea3fca2e1de5df665e121fca14e1364b711450deb",
        "208fcfb50e5a965d5757d151b675ca4af4ce2dfd56401721b6168fae60ab798f",
        "bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c",
        "7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730",
    ]
    if sys.platform != "win32"
    else [
        "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
        "1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd",
        "d0df7988457ec999c148a4a2af25ce831bfaad13954ba18a4446374cb0aef55e",
        "aeb16c4dec1087e39f2330542d59d9b456dd26d791338ae6d80b6ffd10c89dfa",
        "mid21234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
        "ff34cb21271d16dbf928374f610bb5dd593d293d311036ddae86c4846ff79070",
        "bf874c7dd3a83cf370fdc17e496e341de06cd596b5c66dbf3c9bb7f6c139e3ee",
        "3c5b65abcd6a3b2c714dbf7c31ff65fe3748a1adc371f030c283007ca5534f11",
    ]
)


def test_resource_list(mock_packages, capfd):
    with capfd.disabled():
        out = resource("list")

    for h in mock_hashes:
        assert h in out

    assert "url:" in out
    assert "applies to:" in out
    assert "patched by:" in out
    assert "path:" in out

    assert (
        os.path.join("repos", "builtin.mock", "packages", "patch-a-dependency", "libelf.patch")
        in out
    )
    assert "applies to: builtin.mock.libelf" in out
    assert "patched by: builtin.mock.patch-a-dependency" in out


def test_resource_list_only_hashes(mock_packages, capfd):
    with capfd.disabled():
        out = resource("list", "--only-hashes")

    for h in mock_hashes:
        assert h in out


def test_resource_show(mock_packages, capfd):
    test_hash = (
        "c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8"
        if sys.platform != "win32"
        else "3c5b65abcd6a3b2c714dbf7c31ff65fe3748a1adc371f030c283007ca5534f11"
    )
    with capfd.disabled():
        out = resource("show", test_hash)

    assert out.startswith(test_hash)
    assert (
        os.path.join("repos", "builtin.mock", "packages", "patch-a-dependency", "libelf.patch")
        in out
    )
    assert "applies to: builtin.mock.libelf" in out
    assert "patched by: builtin.mock.patch-a-dependency" in out

    assert len(out.strip().split("\n")) == 4
