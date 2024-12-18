# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DingLibs(AutotoolsPackage):
    """A meta-package that pulls in libcollection, libdhash, libini_config,
    librefarray libbasicobjects, and libpath_utils."""

    homepage = "https://pagure.io/SSSD/ding-libs"
    url = "https://releases.pagure.org/SSSD/ding-libs/ding-libs-0.6.1.tar.gz"

    version("0.6.1", sha256="a319a327deb81f2dfab9ce4a4926e80e1dac5dcfc89f4c7e548cec2645af27c1")
    version("0.6.0", sha256="764a211f40cbcf2c9a613fc7ce0d77799d5ee469221b8b6739972e76f09e9fad")
    version("0.5.0", sha256="dab937537a05d7a7cbe605fdb9b3809080d67b124ac97eb321255b35f5b172fd")

    depends_on("c", type="build")  # generated
