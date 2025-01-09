# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlab(PythonPackage):
    """JupyterLab is the next-generation web-based user interface
    for Project Jupyter."""

    homepage = "https://github.com/jupyterlab/jupyterlab"
    pypi = "jupyterlab/jupyterlab-2.2.7.tar.gz"

    license("BSD-3-Clause")

    version("4.0.1", sha256="4dc3901f7bbfd4704c994b7a893a49955256abf57dba9831f4825e3f3165b8bb")
    version("3.4.8", sha256="1fafb8b657005d91603f3c3adfd6d9e8eaf33fdc601537fef09283332efe67cb")
    version("3.4.2", sha256="38abd3a4f83a8f97e3f15bebbcc0825903c15519809eedfaa41340d260be2160")
    version("3.2.9", sha256="65ddc34e5da1a764606e38c4f70cf9d4ac1c05182813cf0ab2dfea312c701124")
    version("3.2.1", sha256="54466941bcd9b52f23373a32038fbb4e50fd652d4536df6179b53e1ffb8ef431")
    version("3.1.19", sha256="8853a6fa16179ae24b6277541b1619593e0e99da10b380cd72f391b549f59705")
    version("3.1.18", sha256="a43733acc3729557fc4758cff55652e52896e42c64c1f12540656ae7f298b806")
    version("3.1.14", sha256="13174cb6076dd5da6f1b85725ccfcc9518d8f98e86b8b644fc89b1dfaeda63a9")
    version("3.0.18", sha256="0e4bb4b89014607a16658b54f13df2f0af14f3c286109a0e14d5a46cbbe28caf")
    version("3.0.16", sha256="7ad4fbe1f6d38255869410fd151a8b15692a663ca97c0a8146b3f5c40e275c23")
    version("2.2.7", sha256="a72ffd0d919cba03a5ef8422bc92c3332a957ff97b0490494209c83ad93826da")
    version("2.1.0", sha256="8c239aababf5baa0b3d36e375fddeb9fd96f3a9a24a8cda098d6a414f5bbdc81")

    # Optional dependencies needed to install jupyterlab extensions
    depends_on("node-js", type="run")
    depends_on("npm", type="run")

    depends_on("python@3.8:", when="@4:", type=("build", "run"))
    depends_on("py-hatchling@1.5:", when="@4:", type=("build", "run"))
    # under [tool.hatch.build.hooks.jupyter-builder] in pyproject.toml
    depends_on("py-hatch-jupyter-builder@0.3.2:", when="@4:", type=("build", "run"))

    depends_on("py-async-lru@1:", when="@4:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.3:", when="@4: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-resources@1.4:", when="@4: ^python@:3.8", type=("build", "run"))
    depends_on("py-ipykernel", when="@4:", type=("build", "run"))
    depends_on("py-jinja2@3.0.3:", when="@4:", type=("build", "run"))
    depends_on("py-jupyter-core", when="@3:", type=("build", "run"))
    depends_on("py-jupyter-lsp@2:", when="@4:", type=("build", "run"))
    depends_on("py-jupyter-server@2.4:2", when="@4:", type=("build", "run"))
    depends_on("py-jupyterlab-server@2.19:2", when="@4:", type=("build", "run"))
    depends_on("py-notebook-shim@0.2:", when="@4:", type=("build", "run"))
    depends_on("py-packaging", when="@3:", type=("build", "run"))
    depends_on("py-traitlets", when="@4:", type=("build", "run"))
    depends_on("py-tornado@6.2:", when="@4:", type=("build", "run"))
    depends_on("py-tomli", when="@3.4.7: ^python@:3.10", type=("build", "run"))

    with when("@:3"):
        depends_on("py-setuptools", when="@:3", type=("build", "run"))
        depends_on("py-jupyter-packaging@0.9:1", when="@3.4.8", type="build")
        depends_on("py-jupyter-packaging@0.9:0", when="@3.0.15:3.4.2", type="build")
        depends_on("py-pre-commit", when="@3.4:3.4.3", type="build")

        depends_on("py-ipython", when="@3", type=("build", "run"))
        depends_on("py-tornado@6.1:", when="@3:", type=("build", "run"))
        depends_on("py-jupyterlab-server@2.10:2", when="@3.3:", type=("build", "run"))
        depends_on("py-jupyterlab-server@2.3:2", when="@3.0.9:3.2", type=("build", "run"))
        depends_on("py-jupyterlab-server@2.0:2", when="@3.0.0:3.0.8", type=("build", "run"))
        depends_on("py-jupyter-server@1.16:1", when="@3.4:", type=("build", "run"))
        depends_on("py-jupyter-server@1.4:1", when="@3.0.9:3.3", type=("build", "run"))
        depends_on("py-jupyter-server@1.2:1", when="@3.0.3:3.0.8", type=("build", "run"))
        depends_on("py-jupyter-server@1.1:1", when="@3.0.0:3.0.2", type=("build", "run"))
        depends_on("py-nbclassic", when="@3.4.4:", type=("build", "run"))
        depends_on("py-nbclassic@0.2.0:0", when="@3:3.4.3", type=("build", "run"))
        depends_on("py-notebook@:6", when="@3.4.8:", type=("build", "run"))
        # dependency on py-jinja2@2.1 seems to be a migration issue from the switch
        # to setup.cfg in 3.0.15, leave it a 2.10
        depends_on("py-jinja2@2.10:", type=("build", "run"))

    with when("@:2"):
        depends_on("python@:3.9", when="@:2.1", type=("build", "run"))
        depends_on("py-notebook@4.3.1:", type=("build", "run"))
        depends_on("py-tornado@:5,6.0.3:", type=("build", "run"))
        depends_on("py-jupyterlab-server@1.1.5:1", type=("build", "run"))

    def setup_run_environment(self, env):
        env.set("JUPYTERLAB_DIR", self.prefix.share.jupyter.lab)
