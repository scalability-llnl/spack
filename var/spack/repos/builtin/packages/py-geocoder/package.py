# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeocoder(PythonPackage):
    """Geocoder is a simple and consistent geocoding library."""

    homepage = "https://github.com/DenisCarriere/geocoder"
    pypi = "geocoder/geocoder-1.38.1.tar.gz"

    license("MIT")

    version("1.38.1", sha256="c9925374c961577d0aee403b09e6f8ea1971d913f011f00ca70c76beaf7a77e7")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-requests")
        depends_on("py-ratelim")
        depends_on("py-click")
        depends_on("py-six")
        depends_on("py-future")
