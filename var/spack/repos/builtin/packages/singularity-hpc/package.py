# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class SingularityHpc(PythonPackage):
    """Local filesystem registry for containers (intended for HPC)
    using Lmod or Environment Modules. Works for users and admins.
    """

    maintainers("marcodelapierre", "vsoch")

    homepage = "https://github.com/singularityhub/singularity-hpc"
    pypi = "singularity-hpc/singularity-hpc-0.1.16.tar.gz"

    license("MPL-2.0")

    version("0.1.16", sha256="00aca234259b962914987ec725181dafc11096fa721d610485615585753d769f")
    version("0.1.12", sha256="760cbcae7b07b319ff6147938578648ce6f0af760701e62bf5f88649ef08f793")

    variant(
        "runtime",
        default="none",
        description="Container runtime installed by Spack for this package",
        values=("none", "singularityce", "singularity", "podman"),
        multi=False,
    )

    variant(
        "modules",
        default="none",
        description="Module system installed by Spack for this package",
        values=("none", "lmod", "environment-modules"),
        multi=False,
    )

    depends_on("python@3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")

    depends_on("py-spython@0.2.0:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-ruamel-yaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))

    depends_on("singularityce@3:", when="runtime=singularityce", type="run")
    depends_on("singularity@3:", when="runtime=singularity", type="run")
    depends_on("podman", when="runtime=podman", type="run")

    depends_on("lmod", when="modules=lmod", type="run")
    depends_on("environment-modules", when="modules=environment-modules", type="run")
