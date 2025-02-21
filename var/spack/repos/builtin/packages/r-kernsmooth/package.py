# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKernsmooth(RPackage):
    """Functions for Kernel Smoothing Supporting Wand & Jones (1995).

    Functions for kernel smoothing (and density estimation) corresponding to
    the book:  Wand, M.P. and Jones, M.C. (1995) "Kernel Smoothing"."""

    cran = "KernSmooth"

    version("2.23-24", sha256="d0b3ec39547ffd92565e91b0c3bb637f3b30e7a46afe416d8790b8c4f528ac5f")
    version("2.23-20", sha256="20eb75051e2473933d41eedc9945b03c632847fd581e2207d452cf317fa5ec39")
    version("2.23-18", sha256="8334800c5ad2305539d2731b929ea34f50fa4269ba87277b699fd5be5b03c490")
    version("2.23-15", sha256="8b72d23ed121a54af188b2cda4441e3ce2646359309885f6455b82c0275210f6")

    depends_on("r@2.5.0:", type=("build", "run"))
