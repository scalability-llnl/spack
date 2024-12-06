# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class NfCoreTools(PythonPackage):
    """A python package with helper tools for the nf-core community."""

    homepage = "https://nf-co.re/tools"
    pypi = "nf-core/nf-core-2.7.1.tar.gz"
    maintainers("marcodelapierre")

    license("MIT")

    version("2.7.2", sha256="585be3908b9b93ee9263b99dd779818d48d51f6e7f44a42aa79e626617e7af48")
    version("2.7.1", sha256="90de62390314ef3141cee700667f017aa65c0346e40704a0f70d0662abcfb0db")
    version("2.6", sha256="47d4df906a60006249284bbf0bb84cdec48303a699c7c0d0a26f404a50e0811a")
    version("2.5.1", sha256="0303f6e3810ba1bc6ac843566ee9dea6b5edbf3527437dec5854b8c437456a4f")

    depends_on("nextflow@21.10.3:", type="run")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-setuptools@40.6:", type="build")

    depends_on("py-click", type=("build", "run"))
    depends_on("py-filetype", type=("build", "run"))
    depends_on("py-galaxy-tool-util", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jsonschema@3.0:", type=("build", "run"))
    depends_on("py-markdown@3.3:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pre-commit", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.3:", type=("build", "run"))
    depends_on("py-pytest@7.0.0:", type=("build", "run"))
    depends_on("py-pytest-workflow@1.6.0:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-questionary@1.8.0:", type=("build", "run"))
    depends_on("py-refgenie", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-requests-cache", type=("build", "run"))
    depends_on("py-rich-click@1.0.0:", type=("build", "run"))
    depends_on("py-rich@10.7.0:", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
