# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFabric3(PythonPackage):
    """Fabric is a simple, Pythonic tool for
    remote execution and deployment (py2.7/py3.4+ compatible fork).
    """

    homepage = "https://github.com/mathiasertl/fabric/"
    pypi = "fabric3/Fabric3-1.14.post1.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.14.post1", sha256="647e485ec83f30b587862f92374d6affc217f3d79819d1d7f512e42e7ae51e81"
    )

    depends_on("py-setuptools", type="build")

    depends_on("py-paramiko@2.0:2", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
