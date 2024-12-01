# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgconfig(RPackage):
    """Private Configuration for 'R' Packages.

    Set configuration options on a per-package basis. Options set by a given
    package only apply to that package, other packages are unaffected."""

    cran = "pkgconfig"

    license("MIT")

    version("2.0.3", sha256="330fef440ffeb842a7dcfffc8303743f1feae83e8d6131078b5a44ff11bc3850")
    version("2.0.2", sha256="25997754d1adbe7a251e3bf9879bb52dced27dd8b84767d558f0f644ca8d69ca")
    version("2.0.1", sha256="ab02b2a4b639ba94dcba882a059fe9cddae5498a4309841f764b62ec46ba5a40")
