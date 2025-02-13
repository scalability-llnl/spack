# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXesmf(PythonPackage):
    """Universal Regridder for Geospatial Data."""

    homepage = "https://github.com/pangeo-data/xESMF"
    pypi = "xesmf/xesmf-0.8.4.tar.gz"

    license("MIT")

    version("0.8.8", sha256="8588f83007ce7011379991f516be3691df6fb30486741f0e1c33aa962056ea33")
    version("0.8.4", sha256="c5a2c4b3e8dbbc9fccd5772a940f9067d68e824215ef87ba222b06718c4eeb56")

    with default_args(type="build"):
        depends_on("py-setuptools@41.2:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-cf-xarray@0.5.1:")

        # esmf +python is only handled correctly in spack for 8.4+
        depends_on("esmf@8.4.0: +python")
        depends_on("py-numba@0.55.2:")
        depends_on("py-numpy@1.16:")
        depends_on("py-shapely")
        depends_on("py-sparse@0.8:")
        depends_on("py-xarray@0.16.2:")
