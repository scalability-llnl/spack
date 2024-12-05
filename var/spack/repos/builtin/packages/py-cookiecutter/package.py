# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCookiecutter(PythonPackage):
    """A command-line utility that creates projects from cookiecutters
    (project templates).  E.g. Python package projects, jQuery plugin
    projects."""

    homepage = "https://cookiecutter.readthedocs.io/en/latest/"
    url = "https://github.com/audreyr/cookiecutter/archive/1.6.0.tar.gz"

    license("BSD-3-Clause")

    version("2.6.0", sha256="da014a94d85c1b1be14be214662982c8c90d860834cbf9ddb2391a37ad7d08be")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-24065
        version("1.7.3", sha256="5c16f9e33875f49bb091ef836b71ced63372aadc49799d78315db1d91d17d76d")
        version("1.6.0", sha256="0c9018699b556b83d7c37b27fe0cc17485b90b6e1f47365b3cdddf77f6ca9d36")

    depends_on("py-setuptools", type="build")
    depends_on("py-binaryornot@0.2.0:", type=("build", "run"))
    depends_on("py-binaryornot@0.4.4:", type=("build", "run"), when="@1.7.1:")
    depends_on("py-jinja2@2.7:3", type=("build", "run"))
    depends_on("py-click@5.0:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"), when="@1.7:")
    depends_on("py-click@:7", type=("build", "run"), when="@:2.0")
    depends_on("py-click@:8", type=("build", "run"), when="@2.1:")
    depends_on("py-pyyaml@5.3.1:", type=("build", "run"), when="@2:")
    depends_on("py-python-slugify@4:", type=("build", "run"), when="@1.7.1:")
    depends_on("py-requests@2.18.0:", type=("build", "run"))
    depends_on("py-requests@2.23.0:", type=("build", "run"), when="@1.7.1:")
    depends_on("py-arrow", type=("build", "run"), when="@2.2:")
    depends_on("py-rich", type=("build", "run"), when="@2.3:")

    # Historical dependencies
    depends_on("py-future@0.15.2:", type=("build", "run"), when="@:1.7.0")
    depends_on("py-whichcraft@0.4.0:", type=("build", "run"), when="@:1")
    depends_on("py-poyo@0.1.0:", type=("build", "run"), when="@:1")
    depends_on("py-poyo@0.5.0:", type=("build", "run"), when="@1.7.1:1")
    depends_on("py-jinja2-time@0.1.0:", type=("build", "run"), when="@:2.1")
    depends_on("py-jinja2-time@0.2.0:", type=("build", "run"), when="@1.7.1:2.1")
    depends_on("py-six@1.10:", type=("build", "run"), when="@1.7.2:1")
