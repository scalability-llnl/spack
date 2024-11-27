# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorpy(PythonPackage):
    """ColorPy is a Python package to convert physical descriptions of light -
    spectra of light intensity vs. wavelength - into RGB colors that can be
    drawn on a computer screen. It provides a nice set of attractive plots
    that you can make of such spectra, and some other color related
    functions as well.
    """

    homepage = "http://markkness.net/colorpy/ColorPy.html"
    pypi = "colorpy/colorpy-0.1.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.1.1", sha256="e400a7e879adc83c6098dde13cdd093723f3936778c245b1caf88f5f1411170d")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="run")
    depends_on("py-matplotlib", type="run")
