# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VariantValues(Package):
    """Test variant value validation with multiple definitions."""

    homepage = "https://www.example.org"
    url = "https://example.org/files/v3.4/cmake-3.4.3.tar.gz"

    version("1.0", md5="4cb3ff35b2472aae70f542116d616e63")
    version("2.0", md5="b2472aae70f542116d616e634cb3ff35")
    version("3.0", md5="d616e634cb3ff35b2472aae70f542116")

    variant("v", default="foo", values=["foo"], when="@1.0")

    variant("v", default="foo", values=["foo", "bar"], when="@2.0")

    # this overrides the prior definition entirely
    variant("v", default="bar", values=["foo", "bar"], when="@2.0:3.0")
