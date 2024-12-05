# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class AutoconfArchive(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Autoconf Archive is a collection of more than 500 macros for
    GNU Autoconf."""

    homepage = "https://www.gnu.org/software/autoconf-archive/"
    gnu_mirror_path = "autoconf-archive/autoconf-archive-2019.01.06.tar.xz"

    license("GPL-3.0-or-later")

    version(
        "2023.02.20", sha256="71d4048479ae28f1f5794619c3d72df9c01df49b1c628ef85fde37596dc31a33"
    )
    version(
        "2022.02.11", sha256="78a61b611e2eeb55a89e0398e0ce387bcaf57fe2dd53c6fe427130f777ad1e8c"
    )
    version(
        "2019.01.06", sha256="17195c833098da79de5778ee90948f4c5d90ed1a0cf8391b4ab348e2ec511e3f"
    )

    patch(
        "https://github.com/autoconf-archive/autoconf-archive/commit/510672bc200e869fb0ad4634407561be819cf093.patch?full_index=1",
        sha256="139214f5104f699f868dc87a14378e1e694a3c2539efa0de6f878024f3d7c66d",
        when="@2022.02.11",
    )

    # The package does not produce any libraries and does not use libtool:
    patch_libtool = False

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        env.append_path("ACLOCAL_PATH", self.prefix.share.aclocal)
