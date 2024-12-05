# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServerProxy(PythonPackage):
    """
    Jupyter Server Proxy lets you run arbitrary external processes
    (such as RStudio, Shiny Server, Syncthing, PostgreSQL, Code Server, etc)
    alongside your notebook server and provide authenticated web access to them
    using a path like /rstudio next to others like /lab.
    """

    homepage = "https://github.com/jupyterhub/jupyter-server-proxy"
    pypi = "jupyter-server-proxy/jupyter-server-proxy-3.2.2.tar.gz"

    license("BSD-3-Clause")

    version("3.2.2", sha256="54690ea9467035d187c930c599e76065017baf16e118e6eebae0d3a008c4d946")

    depends_on("py-jupyter-packaging@0.7.9:0.7", type="build")
    depends_on("py-jupyterlab@3.0:3", type="build")
    depends_on("py-setuptools@40.8.0:", type="build")

    depends_on("py-aiohttp", type=("build", "run"))
    depends_on("py-jupyter-server@1.0:", type=("build", "run"))
    depends_on("py-simpervisor@0.4:", type=("build", "run"))
