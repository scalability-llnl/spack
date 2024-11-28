# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyReproject(PythonPackage):
    """The reproject package is a Python package to reproject
    astronomical images using various techniques via a uniform
    interface. By reprojection, we mean the re-gridding of images from
    one world coordinate system to another (for example changing the
    pixel resolution, orientation, coordinate system). Currently, we
    have implemented reprojection of celestial images by interpolation
    (like SWARP), as well as by finding the exact overlap between
    pixels on the celestial sphere (like Montage). It can also
    reproject to/from HEALPIX projections by relying on the
    astropy-healpix package."""

    homepage = "https://reproject.readthedocs.io/"
    pypi = "reproject/reproject-0.7.1.tar.gz"

    license("BSD-3-Clause")

    version("0.7.1", sha256="95c0fa49e6b4e36455b91fa09ad1b71b230c990ad91d948af67ea3509a1a4ccb")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-extension-helpers", type="build")
    depends_on("py-numpy@1.13:", type=("build", "run"))
    depends_on("py-astropy@3.2:", type=("build", "run"))
    depends_on("py-scipy@1.1:", type=("build", "run"))
    depends_on("py-astropy-healpix@0.2:", type=("build", "run"))
