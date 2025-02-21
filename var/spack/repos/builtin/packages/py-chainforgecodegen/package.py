# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyChainforgecodegen(PythonPackage):
    """A code generator that fuses subsequent batched matrix multiplications (GEMMs)
    into a single GPU kernel, holding intermediate results in shared memory as long as necessary.
    """

    git = "https://github.com/SeisSol/chainforge.git"

    maintainers("davschneller", "Thomas-Ulrich")
    license("BSD-3-Clause")

    version("master", branch="master")
    depends_on("py-numpy")
    depends_on("py-graphviz", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-lark", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec.prefix)
        env.prepend_path("PYTHONPATH", self.spec.prefix)
