# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

import spack.spec
from spack.oci.image import Digest, ImageReference, default_tag, tag


@pytest.mark.parametrize(
    "image_ref, expected",
    [
        (
            f"example.com:1234/a/b/c:tag@sha256:{'a'*64}",
            ("example.com:1234", "a/b/c", "tag", Digest.from_sha256("a" * 64)),
        ),
        ("example.com:1234/a/b/c:tag", ("example.com:1234", "a/b/c", "tag", None)),
        ("example.com:1234/a/b/c", ("example.com:1234", "a/b/c", "latest", None)),
        (
            f"example.com:1234/a/b/c@sha256:{'a'*64}",
            ("example.com:1234", "a/b/c", "latest", Digest.from_sha256("a" * 64)),
        ),
        # ipv4
        ("1.2.3.4:1234/a/b/c:tag", ("1.2.3.4:1234", "a/b/c", "tag", None)),
        # ipv6
        ("[2001:db8::1]:1234/a/b/c:tag", ("[2001:db8::1]:1234", "a/b/c", "tag", None)),
        # Follow docker rules for parsing
        ("ubuntu:22.04", ("index.docker.io", "library/ubuntu", "22.04", None)),
        ("myname/myimage:abc", ("index.docker.io", "myname/myimage", "abc", None)),
        ("myname:1234/myimage:abc", ("myname:1234", "myimage", "abc", None)),
        ("localhost/myimage:abc", ("localhost", "myimage", "abc", None)),
        ("localhost:1234/myimage:abc", ("localhost:1234", "myimage", "abc", None)),
        (
            "example.com/UPPERCASE/lowercase:AbC",
            ("example.com", "uppercase/lowercase", "AbC", None),
        ),
    ],
)
def test_name_parsing(image_ref, expected):
    x = ImageReference.from_string(image_ref)
    assert (x.domain, x.name, x.tag, x.digest) == expected


@pytest.mark.parametrize(
    "image_ref",
    [
        # wrong order of tag and sha
        f"example.com:1234/a/b/c@sha256:{'a'*64}:tag",
        # double tag
        "example.com:1234/a/b/c:tag:tag",
        # empty tag
        "example.com:1234/a/b/c:",
        # empty digest
        "example.com:1234/a/b/c@sha256:",
        # unsupport digest algorithm
        f"example.com:1234/a/b/c@sha512:{'a'*128}",
        # invalid digest length
        f"example.com:1234/a/b/c@sha256:{'a'*63}",
        # whitespace
        "example.com:1234/a/b/c :tag",
        "example.com:1234/a/b/c: tag",
        "example.com:1234/a/b/c:tag ",
        " example.com:1234/a/b/c:tag",
        # broken ipv4
        "1.2..3:1234/a/b/c:tag",
    ],
)
def test_parsing_failure(image_ref):
    with pytest.raises(ValueError):
        ImageReference.from_string(image_ref)


def test_digest():
    valid_digest = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

    # Test string roundtrip
    assert str(Digest.from_string(f"sha256:{valid_digest}")) == f"sha256:{valid_digest}"

    # Invalid digest length
    with pytest.raises(ValueError):
        Digest.from_string("sha256:abcdef")

    # Missing algorithm
    with pytest.raises(ValueError):
        Digest.from_string(valid_digest)


@pytest.mark.parametrize(
    "spec",
    [
        # Standard case
        "short-name@=1.2.3",
        # Unsupported characters in git version
        f"git-version@{1:040x}=develop",
        # Too long of a name
        f"{'too-long':x<256}@=1.2.3",
    ],
)
def test_default_tag(spec: str):
    """Make sure that computed image tags are valid."""
    assert re.fullmatch(tag, default_tag(spack.spec.Spec(spec)))
