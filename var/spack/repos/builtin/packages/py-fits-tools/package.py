# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFitsTools(PythonPackage):
    """Tools for manipulating FITS images using primarily scipy
    & native python routines"""

    homepage = "https://github.com/keflavich/FITS_tools"
    url = "https://github.com/keflavich/FITS_tools/archive/v0.2.tar.gz"

    license("BSD-3-Clause")

    version("1.1.2", sha256="6c7596533ea66f5ca05e4326ae6db643edb03aca4b6b654dce091834155d03e8")
    version("1.1.1", sha256="5b79ef24fadb43458388754381644712c05cd89da4f89c197e3bd80ca158c525")
    version("1.1", sha256="995ebf53dc0ffd8bdb5270c4fa0cf52f639aac05cfb68dc6fd5d58ab40148a8a")
    version("1.0", sha256="b711981eb780f3d27a5dec413397af68493b496e1621f9a37cf68dd265536937")
    version("0.4.1", sha256="3511eb7bbaf73ac68b92b460c71b7a3dbf6c3860fae908638180876eca12f8fd")
    version("0.4", sha256="dbdb558d4c3ada627d42b62aaec5eb8f8f6dd3e323cae853fd447d9ec7805637")
    version(
        "0.2",
        sha256="04c4b6eeb09298bca79b228175fcd209d4ca895ce5675f6684120e75928d2d97",
        preferred=True,
    )
    version("0.1", sha256="d128e49ff4ecc6a9bf9a050f8605bc457e028e10e48bb8d6fda4ca358298ec17")

    depends_on("py-setuptools", type="build")
    depends_on("py-astropy")
    depends_on("py-astropy-helpers")
    depends_on("py-scipy")
    depends_on("py-numpy")
