# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDocker(PythonPackage):
    """A Python library for the Docker Engine API."""

    homepage = "https://github.com/docker/docker-py"
    pypi = "docker/docker-4.2.1.tar.gz"

    license("Apache-2.0")

    version("6.0.1", sha256="896c4282e5c7af5c45e8b683b0b0c33932974fe6e50fc6906a0a83616ab3da97")
    version("5.0.3", sha256="d916a26b62970e7c2f554110ed6af04c7ccff8e9f81ad17d0d40c75637e227fb")
    version("4.2.1", sha256="380a20d38fbfaa872e96ee4d0d23ad9beb0f9ed57ff1c30653cbeb0c9c0964f2")

    variant("ssh", default=False, description="Required to use docker-py over SSH")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@45:", when="@6:", type="build")
    depends_on("py-setuptools-scm+toml@6.2:", when="@6:", type="build")
    depends_on("py-six@1.4.0:", when="@4.2.1", type=("build", "run"))
    depends_on("py-websocket-client@0.32.0:", type=("build", "run"))
    depends_on("py-requests@2.14.2:2.17,2.18.1:", type=("build", "run"))
    depends_on("py-requests@2.26.0:", when="@6:", type=("build", "run"))
    depends_on("py-packaging@14.0:", when="@6:", type=("build", "run"))
    depends_on("py-urllib3@1.26.0:", when="@6:", type=("build", "run"))

    depends_on("py-paramiko@2.4.3:", when="@6:+ssh", type=("build", "run"))
    depends_on("py-paramiko@2.4.2:", when="+ssh", type=("build", "run"))
