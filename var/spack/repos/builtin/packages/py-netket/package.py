# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetket(PythonPackage):
    """
    NetKet is an open-source project, delivering cutting-edge methods for the
    study of many-body quantum systems with artificial neural networks and
    machine learning techniques.
    """

    homepage = "https://github.com/netket/netket"
    url = "https://github.com/netket/netket/archive/v2.1.1.tar.gz"

    license("Apache-2.0")

    version("2.1.1", sha256="881ae8605a829364b2116bc4398084766b24e2cd8958d0cb2b85595650e7bfd6")
    version("2.1", sha256="041d2b058c5d2945bf0a4194ad2bf3c426ad9b6ce0dd323a81a7154bc6e45452")
    version("2.0", sha256="c2890361b16ffb5265023a736536c435ccb3ad956d897e5820eac431d72cdb0e")
    version("1.0.5", sha256="26562bf608775f21eb2cb443f2c66c09cadb56e6eac84f4d855d62e7d776a511")
    version("1.0.4", sha256="0b344d526ee34d187281d0c2f7952c91728abbe22553e3dbcd45fcfeb312c3b5")
    version("1.0.3", sha256="b8e54d7ad8b379b740def640d748c6560943aed473755389fc5cf1020b9007de")
    version("1.0.2", sha256="229c906e92a432bbbd0ff0527874f41318f8fc480d12a33c8184f30960ae628b")

    depends_on("cxx", type="build")  # generated

    # build only deps
    depends_on("py-setuptools", type="build")
    depends_on("cmake@3.12:", type="build")

    depends_on("blas")
    depends_on("mpi")
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.16:", type=("build", "run"))
    depends_on("py-scipy@1.2.1:", type=("build", "run"))
    depends_on("py-mpi4py@3.0.1:", type=("build", "run"))
    depends_on("py-numba@0.48.0:", type=("build", "run"))
    depends_on("py-tqdm@4.42.1:", type=("build", "run"))
