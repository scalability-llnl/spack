# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNnls(RPackage):
    """The Lawson-Hanson algorithm for non-negative least squares (NNLS).

    An R interface to the Lawson-Hanson implementation of an algorithm for
    non-negative least squares (NNLS). Also allows the combination of
    non-negative and non-positive constraints."""

    cran = "nnls"

    license("GPL-2.0-or-later")

    version("1.5", sha256="cd70feb286f86f6dead75da693a8f67c9bd3b91eb738e6e6ac659e3b8c7a3452")
    version("1.4", sha256="0e5d77abae12bc50639d34354f96a8e079408c9d7138a360743b73bd7bce6c1f")
