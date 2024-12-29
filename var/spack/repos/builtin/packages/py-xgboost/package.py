# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyXgboost(PythonPackage):
    """XGBoost is an optimized distributed gradient boosting library designed to be
    highly efficient, flexible and portable."""

    homepage = "https://xgboost.ai/"
    pypi = "xgboost/xgboost-1.3.3.tar.gz"
    import_modules = ["xgboost"]

    license("Apache-2.0")
    maintainers("adamjstewart")

    version("2.1.1", sha256="4b1729837f9f1ba88a32ef1be3f8efb860fee6454a68719b196dc88032c23d97")
    version("2.1.0", sha256="7144980923e76ce741c7b03a14d3bd7514db6de5c7cabe96ba95b229d274f5ca")
    version("1.7.6", sha256="1c527554a400445e0c38186039ba1a00425dcdb4e40b37eed0e74cb39a159c47")
    version("1.6.2", sha256="e1f5c91ba88cf8edb409d7fd2ca150dcd80b6f2115587d87365f0c10b2d4f009")
    version("1.6.1", sha256="24072028656f3428e7b8aabf77340ece057f273e41f7f85d67ccaefb7454bb18")
    version("1.5.2", sha256="404dc09dca887ef5a9bc0268f882c54b33bfc16ac365a859a11e7b24d49da387")
    version("1.3.3", sha256="397051647bb837915f3ff24afc7d49f7fca57630ffd00fb5ef66ae2a0881fb43")

    variant("pandas", default=False, description="Enable Pandas extensions for training.")
    variant(
        "scikit-learn", default=False, description="Enable scikit-learn extensions for training."
    )
    variant("dask", default=False, description="Enables Dask extensions for distributed training.")
    variant("plotting", default=False, description="Enables tree and importance plotting.")
    patch("add-lib64.patch", when="@2:")

    for ver in ["1.3.3", "1.5.2", "1.6.1", "1.6.2", "1.7.6", "2.1.0", "2.1.1"]:
        depends_on("xgboost@" + ver, when="@" + ver)

    with default_args(type="build"):
        depends_on("py-hatchling@1.12.1:", type="build", when="@2:")
        # Required to use --config-settings
        depends_on("py-pip@22.1:", when="@2:")

        # Historical dependencies
        depends_on("py-setuptools", when="@:1")
        # in newer pip versions --install-option does not exist
        depends_on("py-pip@:23.0", when="@:1")

    with default_args(type=("build", "run")):
        depends_on("py-numpy", type=("build", "run"))
        # https://github.com/dmlc/xgboost/issues/10221
        depends_on("py-numpy@:1", when="@:2.0", type=("build", "run"))
        depends_on("py-scipy", type=("build", "run"))

        with when("+pandas"):
            depends_on("py-pandas@1.2:", when="@2:")
            depends_on("py-pandas")

        with when("+scikit-learn"):
            depends_on("py-scikit-learn")

        with when("+dask"):
            depends_on("py-dask")
            depends_on("py-pandas")
            depends_on("py-distributed")

        with when("+plotting"):
            depends_on("py-graphviz")
            depends_on("py-matplotlib")

    def patch(self):
        # Hard-coded to search for system libxgboost in the Python installation prefix
        # https://github.com/dmlc/xgboost/issues/6706
        files = [os.path.join("xgboost", "libpath.py")]
        if self.spec.satisfies("@2:"):
            regex = "sys.base_prefix"
            files.append(os.path.join("packager", "nativelib.py"))
        else:
            regex = "sys.prefix"
            files.append("setup.py")
        filter_file(regex, repr(self.spec["xgboost"].prefix), *files, string=True)

    @when("@2:")
    def config_settings(self, spec, prefix):
        return {"use_system_libxgboost": True}

    @when("@:1")
    def install_options(self, spec, prefix):
        return ["--use-system-libxgboost"]
