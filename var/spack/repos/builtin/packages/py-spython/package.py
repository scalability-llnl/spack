# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySpython(PythonPackage):
    """The Python API for working with Singularity containers."""

    homepage = "https://github.com/singularityhub/singularity-cli"
    pypi = "spython/spython-0.2.14.tar.gz"

    license("MPL-2.0")

    version("0.3.1", sha256="143557849d636697ddd80e0ba95920efe4668351f5becce6bdc73a7651aa128d")
    version("0.2.14", sha256="49e22fbbdebe456b27ca17d30061489db8e0f95e62be3623267a23b85e3ce0f0")

    variant(
        "runtime",
        default="none",
        description="Container runtime installed by Spack for this package",
        values=("none", "singularityce", "singularity"),
        multi=False,
    )

    depends_on("singularityce@3.5.2:", when="runtime=singularityce", type="run")
    depends_on("singularity@3.5.2:", when="runtime=singularity", type="run")

    depends_on("py-setuptools", type="build")
    depends_on("py-semver@2.8.1:", when="@:0.2", type=("build", "run"))
