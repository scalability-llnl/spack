# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServer(PythonPackage):
    """The Jupyter Server provides the backend (i.e. the core services, APIs,
    and REST endpoints) for Jupyter web applications like Jupyter notebook,
    JupyterLab, and Voila."""

    homepage = "https://github.com/jupyter-server/jupyter_server"
    pypi = "jupyter_server/jupyter_server-1.9.0.tar.gz"

    license("BSD-3-Clause")

    version("2.14.2", sha256="66095021aa9638ced276c248b1d81862e4c50f292d575920bbe960de1c56b12b")
    version("2.6.0", sha256="ae4af349f030ed08dd78cb7ac1a03a92d886000380c9ea6283f3c542a81f4b06")
    version("1.21.0", sha256="d0adca19913a3763359be7f0b8c2ea8bfde356f4b8edd8e3149d7d0fbfaa248b")
    version("1.18.1", sha256="2b72fc595bccae292260aad8157a0ead8da2c703ec6ae1bb7b36dbad0e267ea7")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-29241
        version(
            "1.17.0", sha256="7b3aa524790ab0da64f06dfe0b2af149d0a3f59aad71fdedcf1d8bae6508018c"
        )
        version(
            "1.13.5", sha256="9e3e9717eea3bffab8cfb2ff330011be6c8bbd9cdae5b71cef169fcece2f19d3"
        )
        version(
            "1.11.2", sha256="c1f32e0c1807ab2de37bf70af97a36b4436db0bc8af3124632b1f4441038bf95"
        )
        version(
            "1.11.1", sha256="ab7ab1cc38512f15026cbcbb96300fb46ec8b24aa162263d9edd00e0a749b1e8"
        )
        version(
            "1.11.0", sha256="8ab4f484a4a2698f757cff0769d27b5d991e0232a666d54f4d6ada4e6a61330b"
        )
        version(
            "1.10.2", sha256="d3a3b68ebc6d7bfee1097f1712cf7709ee39c92379da2cc08724515bb85e72bf"
        )
        version("1.9.0", sha256="7d19006380f6217458a9db309b54e3dab87ced6c06329c61823907bef2a6f51b")
        version("1.6.1", sha256="242ddd0b644f10e030f917019b47c381e0f2d2b950164af45cbd791d572198ac")

    variant("typescript", default=False, description="Build the typescript code", when="@1.10.2:1")

    # https://github.com/spack/spack/issues/41899
    patch("no_npm_node.patch", when="@1.10.2:1 ~typescript")

    depends_on("python@3.8:", when="@2:", type=("build", "run"))
    depends_on("py-hatchling@1.11:", when="@2:", type="build")
    # under [tool.hatch.build.hooks.jupyter-builder] in pyproject.toml
    depends_on("py-hatch-jupyter-builder@0.8.1:", when="@2:", type="build")

    with when("@:1"):
        depends_on("py-jupyter-packaging@0.9:0", when="@1.6.2:", type="build")
        depends_on("py-pre-commit", when="@1.16:", type="build")
        depends_on("py-setuptools", type="build")

    depends_on("npm", type="build", when="+typescript")
    depends_on("py-anyio@3.1.0:", when="@2.2.1:", type=("build", "run"))
    depends_on("py-anyio@3.1.0:3", when="@:2.2.0", type=("build", "run"))
    depends_on("py-argon2-cffi@21.1:", when="@2.14:", type=("build", "run"))
    depends_on("py-argon2-cffi", type=("build", "run"))
    depends_on("py-jinja2@3.0.3:", when="@2.14:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jupyter-client@7.4.4:", when="@2:", type=("build", "run"))
    depends_on("py-jupyter-client@6.1.12:", when="@1.16:", type=("build", "run"))
    depends_on("py-jupyter-client@6.1.1:", type=("build", "run"))
    depends_on("py-jupyter-core@4.12:4,5.1:", when="@1.23.5:", type=("build", "run"))
    depends_on("py-jupyter-core@4.7:", when="@1.16:", type=("build", "run"))
    depends_on("py-jupyter-core@4.6:", type=("build", "run"))
    depends_on("py-jupyter-server-terminals@0.4.4:", when="@2.14:", type=("build", "run"))
    depends_on("py-jupyter-server-terminals", when="@2:", type=("build", "run"))
    depends_on("py-nbconvert@6.4.4:", when="@1.16:", type=("build", "run"))
    depends_on("py-nbconvert", type=("build", "run"))
    depends_on("py-nbformat@5.3:", when="@2:", type=("build", "run"))
    depends_on("py-nbformat@5.2:", when="@1.15:", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-packaging@22.0:", when="@2.14:", type=("build", "run"))
    depends_on("py-packaging", when="@1.13.2:", type=("build", "run"))
    depends_on("py-prometheus-client@0.9:", when="@2.14:", type=("build", "run"))
    depends_on("py-prometheus-client", type=("build", "run"))
    # for windows depends_on pywinpty@2.0.1:, when='@2.14:'
    # for windows depends_on pywinpty, when='@1.13.2:'
    # py-pywinpty is not in spack and requires the build system maturin
    depends_on("py-pyzmq@24:", when="@2:", type=("build", "run"))
    depends_on("py-pyzmq@17:", type=("build", "run"))
    depends_on("py-send2trash@1.8.2:", when="@2.7.1:", type=("build", "run"))
    depends_on("py-send2trash", type=("build", "run"))
    depends_on("py-terminado@0.8.3:", type=("build", "run"))
    depends_on("py-tornado@6.2:", when="@2:", type=("build", "run"))
    depends_on("py-tornado@6.1:", type=("build", "run"))
    depends_on("py-traitlets@5.6:", when="@2.0.1:", type=("build", "run"))
    depends_on("py-traitlets@5.1:", when="@1.16:", type=("build", "run"))
    depends_on("py-traitlets@5:", when="@1.13.3:", type=("build", "run"))
    depends_on("py-traitlets@4.2.1:", type=("build", "run"))
    depends_on("py-websocket-client@1.7:", when="@2.14:", type=("build", "run"))
    depends_on("py-websocket-client", type=("build", "run"))
    depends_on("py-jupyter-events@0.9:", when="@2.10.1:", type=("build", "run"))
    depends_on("py-jupyter-events@0.6:", when="@2.6:", type=("build", "run"))
    depends_on("py-overrides@5.0:", when="@2.14:", type=("build", "run"))
    depends_on("py-overrides", when="@2.6:", type=("build", "run"))

    # old
    depends_on("py-ipython-genutils", when="@:1.15", type=("build", "run"))
    depends_on("py-requests-unixsocket", when="@:1.11.1", type=("build", "run"))
