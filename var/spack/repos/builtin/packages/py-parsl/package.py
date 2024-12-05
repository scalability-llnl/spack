# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParsl(PythonPackage):
    """
    Simple data dependent workflows in Python
    """

    homepage = "https://github.com/Parsl/parsl"
    url = "https://github.com/Parsl/parsl/archive/refs/tags/1.1.0.tar.gz"

    maintainers("hategan")

    license("Apache-2.0")

    version(
        "2023.08.21", sha256="d7d6145ad5ab63baf9c9f9441a0a6ea5be6f896ef8094d47bf64d949a56b1782"
    )
    version("1.2.0", sha256="342c74ee39fa210d74b8adfb455f0a9c20d9f059ec5bd9d60c5bdc9929abcdcc")
    version("1.1.0", sha256="6a623d3550329f028775950d23a2cafcb0f82b199f15940180410604aa5d102c")

    depends_on("c", type="build")  # generated

    variant("monitoring", default=False, description="enable live monitoring")
    # See https://parsl.readthedocs.io/en/stable/userguide/monitoring.html

    depends_on("python@3.8:", type=("build", "run"), when="@2023.08.21:")
    depends_on("python@3.6:", type=("build", "run"), when="@:1.2")
    depends_on("py-setuptools", type="build")
    depends_on("py-pyzmq@17.1.2:", type=("build", "run"))
    depends_on("py-typeguard@2.10:2", type=("build", "run"), when="@2023.08.21:")
    depends_on("py-typeguard@2.10:", type=("build", "run"), when="@:1.2")
    depends_on("py-typing-extensions@4.6:4", type=("build", "run"), when="@2023.08.21:")
    depends_on("py-typing-extensions", type=("build", "run"), when="@:1.2")
    depends_on("py-six", type=("build", "run"), when="@2023.08.21:")
    depends_on("py-globus-sdk", type=("build", "run"))
    depends_on("py-dill", type=("build", "run"))
    depends_on("py-tblib", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-paramiko", type=("build", "run"))
    depends_on("py-psutil@5.5.1:", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"), when="@2023.08.21:")

    with when("+monitoring"):
        depends_on("py-sqlalchemy@1.4:1", type=("build", "run"), when="@2023.08.21:")
        depends_on("py-sqlalchemy@1.3", type=("build", "run"), when="@:1.2")
        conflicts("^py-sqlalchemy@1.3.4", when="@:1.2")
        depends_on("py-sqlalchemy-utils", type=("build", "run"), when="@:1.2")
        depends_on("py-pydot", type=("build", "run"))
        depends_on("py-networkx@2.5.0:2.5", type=("build", "run"), when="@2023.08.21:")
        depends_on("py-networkx", type=("build", "run"), when="@:1.2")
        depends_on("py-flask@1.0.2:", type=("build", "run"))
        depends_on("py-flask-sqlalchemy", type=("build", "run"))
        depends_on("py-pandas@:1", type=("build", "run"), when="@2023.08.21:")
        depends_on("py-pandas", type=("build", "run"), when="@:1.2")
        depends_on("py-plotly", type=("build", "run"))
        depends_on("py-python-daemon", type=("build", "run"))
