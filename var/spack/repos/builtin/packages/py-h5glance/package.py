# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyH5glance(PythonPackage):
    """H5Glance lets you explore HDF5 files in the terminal or
    an HTML interface.
    """

    homepage = "https://github.com/European-XFEL/h5glance"
    pypi = "h5glance/h5glance-0.4.tar.gz"

    license("BSD-3-Clause")

    version("0.6", sha256="203369ab614273aaad3419f151e234609bb8390b201b65f678d7e17c57633e35")
    version("0.5", sha256="bc34ee42429f0440b329083e3f67fbf3d7016a4aed9e8b30911e5905217bc8d9")
    version("0.4", sha256="03babaee0d481991062842796126bc9e6b11e2e6e7daba57c26f2b58bf3bbd32")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-flit", type="build")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-htmlgen", type=("build", "run"))
