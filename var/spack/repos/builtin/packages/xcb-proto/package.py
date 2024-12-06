# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbProto(AutotoolsPackage, XorgPackage):
    """xcb-proto provides the XML-XCB protocol descriptions that libxcb uses to
    generate the majority of its code and API."""

    homepage = "https://xcb.freedesktop.org/"
    xorg_mirror_path = "proto/xcb-proto-1.14.1.tar.xz"

    license("MIT")

    maintainers("wdconinc")

    version("1.17.0", sha256="2c1bacd2110f4799f74de6ebb714b94cf6f80fb112316b1219480fd22562148c")
    version("1.16.0", sha256="a75a1848ad2a89a82d841a51be56ce988ff3c63a8d6bf4383ae3219d8d915119")
    version("1.15.2", sha256="7072beb1f680a2fe3f9e535b797c146d22528990c72f63ddb49d2f350a3653ed")
    version("1.14.1", sha256="f04add9a972ac334ea11d9d7eb4fc7f8883835da3e4859c9afa971efdf57fcc3")
    version("1.14", sha256="186a3ceb26f9b4a015f5a44dcc814c93033a5fc39684f36f1ecc79834416a605")
    version(
        "1.13",
        sha256="0698e8f596e4c0dbad71d3dc754d95eb0edbb42df5464e0f782621216fa33ba7",
        url="https://xcb.freedesktop.org/dist/xcb-proto-1.13.tar.gz",
        deprecated=True,
    )
    version(
        "1.12",
        sha256="cfa49e65dd390233d560ce4476575e4b76e505a0e0bacdfb5ba6f8d0af53fd59",
        url="https://xcb.freedesktop.org/dist/xcb-proto-1.12.tar.gz",
        deprecated=True,
    )
    version(
        "1.11",
        sha256="d12152193bd71aabbdbb97b029717ae6d5d0477ab239614e3d6193cc0385d906",
        url="https://xcb.freedesktop.org/dist/xcb-proto-1.11.tar.gz",
        deprecated=True,
    )

    extends("python")

    patch("xcb-proto-1.12-schema-1.patch", when="@1.12")
