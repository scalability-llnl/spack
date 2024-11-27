# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    pypi = "dask/dask-1.1.0.tar.gz"

    maintainers("skosukhin")

    license("BSD-3-Clause")

    version("2024.7.1", sha256="dbaef2d50efee841a9d981a218cfeb50392fc9a95e0403b6d680450e4f50d531")
    version("2023.4.1", sha256="9dc72ebb509f58f3fe518c12dd5a488c67123fdd66ccb0b968b34fd11e512153")
    version("2022.10.2", sha256="42cb43f601709575fa46ce09e74bea83fdd464187024f56954e09d9b428ceaab")
    version("2021.6.2", sha256="8588fcd1a42224b7cfcd2ebc8ad616734abb6b1a4517efd52d89c7dd66eb91f8")
    version("2021.4.1", sha256="195e4eeb154222ea7a1c368119b5f321ee4ec9d78531471fe0145a527f744aa8")
    version("2020.12.0", sha256="43e745afd4b464e6c0113131e430a16dce6ac42460b06e24d799093d098f7ab0")

    variant("array", default=True, description="Install requirements for dask.array")
    variant(
        "bag", default=True, when="@:2021.3.0", description="Install requirements for dask.bag"
    )
    variant("dataframe", default=True, description="Install requirements for dask.dataframe")
    variant("distributed", default=True, description="Install requirements for dask.distributed")
    variant("diagnostics", default=False, description="Install requirements for dask.diagnostics")

    variant(
        "delayed",
        default=True,
        when="@:2021.3.0",
        description="Install requirements for dask.delayed (dask.imperative)",
    )

    depends_on("python@3.8:", type=("build", "run"), when="@2022.10.2:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@62.6:", type="build", when="@2023.4.1:")
    depends_on("py-versioneer@0.28+toml", type="build", when="@2023.4.1:")

    # Common requirements
    depends_on("py-packaging@20:", type="build", when="@2022.10.2:")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyyaml@5.3.1:", type=("build", "run"), when="@2022.10.2:")
    depends_on("py-cloudpickle@1.1.1:", type=("build", "run"), when="@2021.3.1:")
    depends_on("py-cloudpickle@1.5.0:", type=("build", "run"), when="@2023.4.1:")
    depends_on("py-fsspec@0.6.0:", type=("build", "run"), when="@2021.3.1:")
    depends_on("py-fsspec@2021.09.0:", type=("build", "run"), when="@2023.4.1:")
    depends_on("py-toolz@0.8.2:", type=("build", "run"), when="@2021.3.1:")
    depends_on("py-toolz@0.10.0:", type=("build", "run"), when="@2023.4.1:")
    depends_on("py-partd@0.3.10:", type=("build", "run"), when="@2021.3.1:")
    depends_on("py-partd@1.2.0:", type=("build", "run"), when="@2023.4.0:")
    depends_on("py-partd@1.4.0:", type=("build", "run"), when="@2024.7.1:")
    depends_on("py-click@7.0:", type=("build", "run"), when="@2022.10.2:")
    depends_on("py-click@8.0:", type=("build", "run"), when="@2023.4.1:")
    depends_on("py-importlib-metadata@4.13.0:", type=("build", "run"), when="@2023.4.0:")

    # Requirements for dask.array
    depends_on("py-numpy@1.15.1:", type=("build", "run"), when="@2020.12.0: +array")
    depends_on("py-numpy@1.16.0:", type=("build", "run"), when="@2021.3.1: +array")
    depends_on("py-numpy@1.18.0:", type=("build", "run"), when="@2022.10.2: +array")
    depends_on("py-numpy@1.21.0:", type=("build", "run"), when="@2023.4.0: +array")
    # https://github.com/dask/dask/issues/11066
    depends_on("py-numpy@:1", when="@:2024.5.0+array", type=("build", "run"))
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on("py-toolz@0.8.2:", type=("build", "run"), when="@:2021.3.0 +array")

    # Requirements for dask.bag
    depends_on("py-cloudpickle@0.2.1:", type=("build", "run"), when="@0.8.2: +bag")
    # The dependency on py-cloudpickle is non-optional starting version 2021.3.1
    depends_on("py-cloudpickle@0.2.2:", type=("build", "run"), when="@2.13.0:2021.3.0 +bag")
    # The dependency on py-fsspec is non-optional starting version 2021.3.1
    depends_on("py-fsspec@0.6.0:", type=("build", "run"), when="@:2021.3.0 +bag")
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on("py-toolz@0.8.2:", type=("build", "run"), when="@:2021.3.0 +bag")
    # The dependency on py-partd is non-optional starting version 2021.3.1
    depends_on("py-partd@0.3.10:", type=("build", "run"), when="@:2021.3.0 +bag")

    # Requirements for dask.dataframe
    depends_on("py-numpy@1.15.1:", type=("build", "run"), when="@2020.12.0: +dataframe")
    depends_on("py-numpy@1.16.0:", type=("build", "run"), when="@2021.3.1: +dataframe")
    depends_on("py-numpy@1.18.0:", type=("build", "run"), when="@2022.10.2: +dataframe")
    depends_on("py-numpy@1.21.0:", type=("build", "run"), when="@2023.4.0: +dataframe")
    # https://github.com/dask/dask/issues/11066
    depends_on("py-numpy@:1", when="@:2024.5.0+dataframe", type=("build", "run"))
    depends_on("py-pandas@0.25.0:", type=("build", "run"), when="@2020.12.0: +dataframe")
    depends_on("py-pandas@1.0:", type=("build", "run"), when="@2022.10.2: +dataframe")
    depends_on("py-pandas@1.3:", type=("build", "run"), when="@2023.4.0: +dataframe")
    depends_on("py-pandas@2.0:", type=("build", "run"), when="@2024.7.1: +dataframe")
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on("py-toolz@0.8.2:", type=("build", "run"), when="@:2021.3.0 +dataframe")
    # The dependency on py-partd is non-optional starting version 2021.3.1
    depends_on("py-partd@0.3.10:", type=("build", "run"), when="@:2021.3.0 +dataframe")
    # The dependency on py-fsspec is non-optional starting version 2021.3.1
    depends_on("py-fsspec@0.6.0:", type=("build", "run"), when="@:2021.3.0 +dataframe")

    # Requirements for dask.distributed
    depends_on(
        "py-distributed@2020.12.0:2021.8.0", type=("build", "run"), when="@:2021.6.1 +distributed"
    )
    depends_on("py-distributed@2021.6.2", type=("build", "run"), when="@2021.6.2 +distributed")
    depends_on("py-distributed@2022.10.2", type=("build", "run"), when="@2022.10.2 +distributed")
    depends_on("py-distributed@2023.4.1", type=("build", "run"), when="@2023.4.1 +distributed")
    depends_on("py-distributed@2024.7.1", type=("build", "run"), when="@2024.7.1 +distributed")

    # Requirements for dask.diagnostics
    depends_on("py-bokeh@1.0.0:1,2.0.1:", type=("build", "run"), when="+diagnostics")
    depends_on("py-bokeh@2.4.2:2", type=("build", "run"), when="@2022.10.2:2023.3 +diagnostics")
    depends_on("py-bokeh@2.4.2:", type=("build", "run"), when="@2023.4.0: +diagnostics")
    depends_on("py-jinja2", type=("build", "run"), when="@2022.10.2: +diagnostics")
    depends_on("py-jinja2@2.10.3:", type=("build", "run"), when="@2023.4.0: +diagnostics")

    # Requirements for dask.delayed
    # The dependency on py-cloudpickle is non-optional starting version 2021.3.1
    depends_on("py-cloudpickle@0.2.2:", type=("build", "run"), when="@:2021.3.0 +delayed")
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on("py-toolz@0.8.2:", type=("build", "run"), when="@:2021.3.0 +delayed")

    @property
    def import_modules(self):
        modules = ["dask", "dask.bytes"]

        if "+array" in self.spec:
            modules.append("dask.array")

        if "+bag" in self.spec:
            modules.append("dask.bag")

        if "+dataframe" in self.spec:
            modules.extend(["dask.dataframe", "dask.dataframe.tseries", "dask.dataframe.io"])

        if "+diagnostics" in self.spec:
            modules.append("dask.diagnostics")

        return modules
