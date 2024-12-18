# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Patch(AutotoolsPackage, GNUMirrorPackage):
    """Patch takes a patch file containing a difference listing produced by
    the diff program and applies those differences to one or more
    original files, producing patched versions.
    """

    homepage = "https://savannah.gnu.org/projects/patch/"
    gnu_mirror_path = "patch/patch-2.7.6.tar.xz"

    tags = ["core-packages"]

    license("GPL-3.0-or-later")

    version("2.7.6", sha256="ac610bda97abe0d9f6b7c963255a11dcb196c25e337c61f94e4778d632f1d8fd")
    version("2.7.5", sha256="fd95153655d6b95567e623843a0e77b81612d502ecf78a489a4aed7867caa299")

    depends_on("c", type="build")  # generated

    build_directory = "spack-build"
