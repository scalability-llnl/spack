# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCrayon(RPackage):
    """Colored terminal output on terminals that support 'ANSI' color and
    highlight codes. It also works in 'Emacs' 'ESS'. 'ANSI' color support is
    automatically detected. Colors and highlighting can be combined and nested.
    New styles can also be created easily. This package was inspired by the
    'chalk' 'JavaScript' project."""

    homepage = "https://github.com/r-lib/crayon#readme"
    url      = "https://cloud.r-project.org/src/contrib/crayon_1.3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/crayon"

    version('1.3.4', sha256='fc6e9bf990e9532c4fcf1a3d2ce22d8cf12d25a95e4779adfa17713ed836fa68')
    version('1.3.2', sha256='9a6b75d63c05fe64baf222f1921330ceb727924bcc5fc2753ff0528d42555e68')
