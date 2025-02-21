# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginKubernetes(PythonPackage):
    """A Snakemake executor plugin for submission of jobs to Kubernetes."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-kubernetes"
    pypi = "snakemake_executor_plugin_kubernetes/snakemake_executor_plugin_kubernetes-0.1.4.tar.gz"

    license("MIT")

    version("0.2.2", sha256="08f7ea92cc288f0830f7bfc38112c9e4a03d623d84f8f80b0105cc179458fc4c")
    version("0.2.1", sha256="476c423cb33b71bff2ed11d2ec0aace8bb76e1b9667b408880bcbe2c7fdbe6ef")
    version("0.2.0", sha256="83981ad405515880b1b311129fd442c1e17902ee0a673ca14bab5b8ba31d7fbf")
    version("0.1.5", sha256="7984ef057c25ce1ff46ceac5839dfad01e2938faa649e59fa439e8154e8025eb")
    version("0.1.4", sha256="c3aeac87939ec5d038efdc3ba7dbbef5eeb3171c1b718b8af850b6287b9c54ff")

    depends_on("py-kubernetes@27.2:30", type=("build", "run"), when="@0.2.1:")
    depends_on("py-kubernetes@27.2:29", type=("build", "run"), when="@0.1.5:0.2.0")
    depends_on("py-kubernetes@27.2:27", type=("build", "run"), when="@:0.1.4")

    depends_on("py-snakemake-interface-common@1.17.3:1", type=("build", "run"), when="@0.2.0:")
    depends_on("py-snakemake-interface-common@1.14.1:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@0.1.5:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.0.2:8", type=("build", "run"), when="@:0.1.4"
    )

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
