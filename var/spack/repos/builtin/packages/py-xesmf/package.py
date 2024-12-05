# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXesmf(PythonPackage):
    """Universal Regridder for Geospatial Data."""

    homepage = "https://github.com/pangeo-data/xESMF"
    pypi = "xesmf/xesmf-0.8.4.tar.gz"

    license("MIT")

    version("0.8.4", sha256="c5a2c4b3e8dbbc9fccd5772a940f9067d68e824215ef87ba222b06718c4eeb56")

    with default_args(type="build"):
        depends_on("py-setuptools@41.2:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-cf-xarray@0.5.1:")
        # TODO: add optional dependency
        # https://github.com/esmf-org/esmf/tree/develop/src/addon/esmpy
        # depends_on("py-esmpy@8:")
        depends_on("py-numba@0.55.2:")
        depends_on("py-numpy@1.16:")
        depends_on("py-shapely")
        depends_on("py-sparse@0.8:")
        depends_on("py-xarray@0.16.2:")
