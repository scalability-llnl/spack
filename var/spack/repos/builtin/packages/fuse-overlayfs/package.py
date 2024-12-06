# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FuseOverlayfs(AutotoolsPackage):
    """An implementation of overlay+shiftfs in FUSE for rootless containers."""

    homepage = "https://github.com/containers/fuse-overlayfs"
    url = "https://github.com/containers/fuse-overlayfs/archive/v1.1.2.tar.gz"
    maintainers("haampie")

    license("GPL-2.0-or-later")

    version("1.13", sha256="96d10344921d5796bcba7a38580ae14a53c4e60399bb90b238ac5a10b3bb65b2")
    version("1.10", sha256="4351eaed7cf26a5012c14c6e0fc883ef65a7b5dcc95ba129ce485904106c25a9")
    version("1.7.1", sha256="fe2c076aed7b8669e7970301a99c0b197759b611035d8199de4c0add7d2fb2b4")
    version("1.7", sha256="e4d9a794d270e237a38e7ced95af95ad15268e0584eab981ed7c7b3758b95995")
    version("1.6", sha256="5606c5c1e4e0d7063f3f50a72c906f23b7a505784d20dc40fff9e4b2b802d5f4")
    version("1.5.0", sha256="6c81b65b71067b303aaa9871f512c2cabc23e2b793f19c6c854d01a492b5a923")
    version("1.4.0", sha256="7e5666aef4f2047e6a5202d6438b08c2d314dba5b40e431014e7dbb8168d9018")
    version("1.3.0", sha256="91e78a93aac7698c65083deea04952bc86af6abbb0830785ef1dd4a8707ad8bf")
    version("1.2.0", sha256="5df218732244059057686194b0e1fef66fb822d4087db48af88e1bc29bb1afde")
    version("1.1.2", sha256="1c0fa67f806c44d5c51f4bce02fdcb546137a2688a8de76d93d07b79defc9cac")
    version("1.1.1", sha256="9a1c4221a82059fd9686dd8b519d432bae126c08f9d891fb722bcb51ba4933ec")
    version("1.1.0", sha256="060168c2d5a8c6cc768b4542eba9953b7ff4a31f94bfb2e05b3d1051390838b1")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("fuse")
    depends_on("libfuse@3.2.1:", when="^[virtuals=fuse] libfuse")
