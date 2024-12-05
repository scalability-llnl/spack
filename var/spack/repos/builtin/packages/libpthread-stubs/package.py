# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpthreadStubs(AutotoolsPackage, XorgPackage):
    """The libpthread-stubs package provides weak aliases for pthread
    functions not provided in libc or otherwise available by default."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/pthread-stubs"
    xorg_mirror_path = "xcb/libpthread-stubs-0.4.tar.gz"

    maintainers("wdconinc")

    version("0.5", sha256="593196cc746173d1e25cb54a93a87fd749952df68699aab7e02c085530e87747")
    version(
        "0.4",
        sha256="50d5686b79019ccea08bcbd7b02fe5a40634abcfd4146b6e75c6420cc170e9d9",
        url="https://xcb.freedesktop.org/dist/libpthread-stubs-0.4.tar.gz",
    )
    version(
        "0.3",
        sha256="3031f466cf0b06de6b3ccbf2019d15c4fcf75229b7d226a711bc1885b3a82cde",
        url="https://xcb.freedesktop.org/dist/libpthread-stubs-0.3.tar.gz",
    )
