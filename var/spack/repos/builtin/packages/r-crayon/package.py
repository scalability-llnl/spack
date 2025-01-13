# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCrayon(RPackage):
    """Colored Terminal Output.

    Colored terminal output on terminals that support 'ANSI' color and
    highlight codes. It also works in 'Emacs' 'ESS'. 'ANSI' color support is
    automatically detected. Colors and highlighting can be combined and nested.
    New styles can also be created easily. This package was inspired by the
    'chalk' 'JavaScript' project."""

    cran = "crayon"

    license("MIT")

    version("1.5.3", sha256="3e74a0685541efb5ea763b92cfd5c859df71c46b0605967a0b5dbb7326e9da69")
    version("1.5.2", sha256="70a9a505b5b3c0ee6682ad8b965e28b7e24d9f942160d0a2bad18eec22b45a7a")
    version("1.5.1", sha256="c025c73b78a8e88e8e4363c8e1a941da5089a7baea39e59ea5342ab9ebe45df9")
    version("1.4.2", sha256="ee34397f643e76e30588068d4c93bd3c9afd2193deacccacb3bffcadf141b857")
    version("1.4.1", sha256="08b6e42e748d096960b2f32b7ffe690c25742e29fe14c19d1834cd6ff43029c7")
    version("1.3.4", sha256="fc6e9bf990e9532c4fcf1a3d2ce22d8cf12d25a95e4779adfa17713ed836fa68")
    version("1.3.2", sha256="9a6b75d63c05fe64baf222f1921330ceb727924bcc5fc2753ff0528d42555e68")
