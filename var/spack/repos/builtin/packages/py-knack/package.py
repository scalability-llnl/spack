# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyKnack(PythonPackage):
    """A Command-Line Interface framework."""

    homepage = "https://github.com/microsoft/knack"
    pypi = "knack/knack-0.7.1.tar.gz"

    license("MIT")

    version("0.7.1", sha256="fcef6040164ebe7d69629e4e089b398c9b980791446496301befcf8381dba0fc")

    depends_on("py-setuptools", type="build")
    depends_on("py-argcomplete", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-jmespath", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
