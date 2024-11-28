# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorboardPluginWit(PythonPackage):
    """The What-If Tool makes it easy to efficiently and
    intuitively explore up to two models' performance
    on a dataset. Investigate model performances for
    a range of features in your dataset, optimization
    strategies and even manipulations to individual
    datapoint values. All this and more, in a visual way
    that requires minimal code."""

    homepage = "https://pypi.org/project/tensorboard-plugin-wit/"
    # Could also build from source, but this package requires an older version of bazel
    # than tensorflow supports, so we can't build both from source in the same DAG until
    # Spack supports separate concretization of build deps.
    url = "https://pypi.io/packages/py3/t/tensorboard_plugin_wit/tensorboard_plugin_wit-1.8.0-py3-none-any.whl"

    maintainers("aweits")

    license("Apache-2.0")

    version("1.8.1", sha256="ff26bdd583d155aa951ee3b152b3d0cffae8005dc697f72b44a8e8c2a77a8cbe")
    version("1.8.0", sha256="2a80d1c551d741e99b2f197bb915d8a133e24adb8da1732b840041860f91183a")
    version("1.7.0", sha256="ee775f04821185c90d9a0e9c56970ee43d7c41403beb6629385b39517129685b")

    depends_on("py-setuptools@36.2.0:", type="build")
    depends_on("python@3", type=("build", "run"))
