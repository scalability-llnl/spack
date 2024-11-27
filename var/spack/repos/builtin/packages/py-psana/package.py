# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPsana(PythonPackage):
    """LCLS II Developement: PSAna Python."""

    homepage = "https://github.com/slac-lcls/lcls2"
    url = "https://github.com/slac-lcls/lcls2/archive/refs/tags/3.3.37.tar.gz"

    maintainers("valmar")

    version("3.3.37", sha256="127a5ae44c9272039708bd877849a3af354ce881fde093a2fc6fe0550b698b72")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("setup.patch")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-psalg", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-pymongo", type=("build", "run"))
    depends_on("py-amityping", type=("build", "run"))
    depends_on("py-mypy-extensions", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-psmon", type=("build", "run"))
    depends_on("py-lcls-krtc", type=("build", "run"))
    depends_on("py-psmon", type=("build", "run"))
    depends_on("py-ipykernel", type=("build", "run"))
    depends_on("opencv", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-pyabel", type=("build", "run"))
    depends_on("py-prometheus-client", type=("build", "run"))
    depends_on("xtcdata", type=("build", "run", "link"))
    depends_on("psalg", type=("build", "run", "link"))

    build_directory = "psana"

    def setup_build_environment(self, env):
        env.set("INSTDIR", "{0}".format(self.prefix))
        env.set("XTCDATADIR", "{0}".format(self.spec["xtcdata"].prefix))
        env.set("PSALGDIR", "{0}".format(self.spec["psalg"].prefix))
