# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Looptools(AutotoolsPackage):
    """LoopTools is a package for evaluation of scalar and tensor one-loop
    integrals based on the FF package by G.J. van Oldenborgh. It
    features an easy Fortran, C++, and Mathematica interface to the
    scalar one-loop functions of FF and in addition provides
    the 2-, 3-, and 4-point tensor coefficient functions."""

    homepage = "http://www.feynarts.de/looptools/"
    url = "http://www.feynarts.de/looptools/LoopTools-2.15.tar.gz"

    license("LGPL-3.0-or-later")

    version("2.16", sha256="412731a5950f10e2ea3877ceec8655ae18ca856610364e4b6616a8a25d592f2c")
    version("2.15", sha256="a065ffdc4fe6882aa3bb926134ba8ec875d6c0a633c3d4aa5f70db26542713f2")
    version("2.8", sha256="2395518d0eac9b0883a2c249b9a5ba80df443929c520c45e60f5a4284166eb42")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("conf.patch", when="%fj")

    def configure_args(self):
        args = ["FFLAGS=" + self.compiler.f77_pic_flag, "CFLAGS=" + self.compiler.cc_pic_flag]
        return args
