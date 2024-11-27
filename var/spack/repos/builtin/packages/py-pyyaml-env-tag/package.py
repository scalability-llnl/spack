# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyyamlEnvTag(PythonPackage):
    """A custom YAML tag for referencing environment variables in YAML files."""

    homepage = "https://github.com/waylan/pyyaml-env-tag"
    pypi = "pyyaml_env_tag/pyyaml_env_tag-0.1.tar.gz"

    license("MIT")

    version("0.1", sha256="70092675bda14fdec33b31ba77e7543de9ddc88f2e5b99160396572d11525bdb")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-flit-core@2:3", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
