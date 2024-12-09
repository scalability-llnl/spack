# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluiddyn(PythonPackage):
    """Framework for studying fluid dynamics."""

    pypi = "fluiddyn/fluiddyn-0.6.5.tar.gz"

    maintainers("paugier")

    license("CECILL-B", checked_by="paugier")

    version("0.6.5", sha256="ad0df4c05855bd2ae702731983d310bfbb13802874ce83e2da6454bb7100b5df")
    version("0.6.4", sha256="576eb0fa50012552b3a68dd17e81ce4f08ddf1e276812b02316016bb1c3a1342")
    version("0.6.3", sha256="3c4c57ac8e48c55498aeafaf8b26daecefc03e6ac6e2c03a591e0f7fec13bb69")
    version("0.6.2", sha256="40f772cfdf111797ae1c6cf7b67272207f2bc7c4f599085634cc1d74eb748ee5")
    version("0.6.1", sha256="af75ed3adfaaa0f0d82822619ced2f9e0611ad15351c9cdbc1d802d67249c3de")
    version("0.6.0", sha256="47ad53b3723487d3711ec4ea16bca2d7c270b5c5c5a0255f7684558d7397850e")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pdm-backend", type="build")

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-matplotlib")
        depends_on("py-h5py")
        depends_on("py-h5netcdf")
        depends_on("py-distro")
        depends_on("py-simpleeval@0.9.13:")
        depends_on("py-psutil@5.2.1:")
        depends_on("py-ipython")
        depends_on("py-scipy")

    with default_args(type="test"):
        depends_on("py-pytest")
        depends_on("py-pytest-allclose")
        depends_on("py-pytest-mock")
