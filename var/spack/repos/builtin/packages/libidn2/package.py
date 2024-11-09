# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libidn2(AutotoolsPackage, GNUMirrorPackage):
    """Libidn2 is a free software implementation of IDNA2008, Punycode and
    TR46. Its purpose is to encode and decode internationalized domain
    names."""

    homepage = "https://gitlab.com/libidn/libidn2"
    # URL must remain http:// so Spack can bootstrap curl
    gnu_mirror_path = "libidn/libidn2-2.0.5.tar.gz"

    license("GPL-2.0-or-later OR LGPL-3.0-or-later")

    version("2.3.7", sha256="4c21a791b610b9519b9d0e12b8097bf2f359b12f8dd92647611a929e6bfd7d64")
    version("2.3.4", sha256="93caba72b4e051d1f8d4f5a076ab63c99b77faee019b72b9783b267986dbb45f")
    version("2.3.3", sha256="f3ac987522c00d33d44b323cae424e2cffcb4c63c6aa6cd1376edacbf1c36eb0")
    version("2.3.2", sha256="76940cd4e778e8093579a9d195b25fff5e936e9dc6242068528b437a76764f91")
    version("2.3.1", sha256="8af684943836b8b53965d5f5b6714ef13c26c91eaa36ce7d242e3d21f5d40f2d")
    version("2.3.0", sha256="e1cb1db3d2e249a6a3eb6f0946777c2e892d5c5dc7bd91c74394fc3a01cab8b5")
    version("2.1.1a", sha256="57666bcf6ecf54230d7bac95c392379561954b57a673903aed4d3336b3048b72")
    version("2.1.1", sha256="95416080329298a13269e13175041b530cec3d98b54cafae9424b8dfd22078b1")
    version("2.1.0", sha256="032398dbaa9537af43f51a8d94e967e3718848547b1b2a4eb3138b20cad11d32")
    version("2.0.5", sha256="53f69170886f1fa6fa5b332439c7a77a7d22626a82ef17e2c1224858bb4ca2b8")

    depends_on("c", type="build")  # generated

    depends_on("libunistring")

    # in-source build fails
    build_directory = "spack-build"
