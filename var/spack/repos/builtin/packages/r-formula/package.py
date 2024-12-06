# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RFormula(RPackage):
    """Extended Model Formulas.

    Infrastructure for extended formulas with multiple parts on the right-hand
    side and/or multiple responses on the left-hand side (see
    <doi:10.18637/jss.v034.i01>)."""

    cran = "Formula"

    version("1.2-5", sha256="86254674600d64e18b65d52f42d7ebfc217c8e1945cb63ac06da22cbf04d355c")
    version("1.2-4", sha256="cb70e373b5ed2fc8450937fb3321d37dfd22dcc6f07cb872a419d51205125caf")
    version("1.2-3", sha256="1411349b20bd09611a9fd0ee6d15f780c758ad2b0e490e908facb49433823872")
    version("1.2-2", sha256="8def4600fb7457d38db8083733477501b54528974aa216e4adf8871bff4aa429")
    version("1.2-1", sha256="5db1ef55119b299c9d291e1c5c08e2d51b696303daf4e7295c38ff5fc428360a")

    depends_on("r@2.0.0:", type=("build", "run"))
