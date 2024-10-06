# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArkouda(PythonPackage):
    """This is the python client for Arkouda."""

    homepage = "https://github.com/Bears-R-Us/arkouda"

    url = "https://github.com/Bears-R-Us/arkouda/archive/refs/tags/v2024.06.21.tar.gz"
    git = "https://github.com/Bears-R-Us/arkouda.git"

    test_requires_compiler = True

    # A list of GitHub accounts to notify when the package is updated.
    # TODO: add arkouda devs github account
    maintainers("arezaii")

    # See https://spdx.org/licenses/ for a list.
    license("MIT")

    version("master", branch="master")

    version(
        "2024.06.21", sha256="ab7f753befb3a0b8e27a3d28f3c83332d2c6ae49678877a7456f0fcfe42df51c"
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyarrow", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-tables +lzo +bzip2", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-versioneer", type=("build"))
    depends_on("py-pyfiglet", type=("build", "run"))
    depends_on("py-typeguard", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
