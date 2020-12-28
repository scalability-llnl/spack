# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgconfig(RPackage):
    """Set configuration options on a per-package basis. Options set by a
     given package only apply to that package,
     other packages are unaffected."""

    homepage = "https://cloud.r-project.org/package=pkgconfig"
    url      = "https://cloud.r-project.org/src/contrib/pkgconfig_2.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pkgconfig"

    version('2.0.2', sha256='25997754d1adbe7a251e3bf9879bb52dced27dd8b84767d558f0f644ca8d69ca')
    version('2.0.1', sha256='ab02b2a4b639ba94dcba882a059fe9cddae5498a4309841f764b62ec46ba5a40')
