# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcRose(PythonPackage):
    """A Cylc plugin providing support for the Rose rose-suite.conf file."""

    homepage = "https://cylc.github.io/cylc-doc/latest/html/plugins/cylc-rose.html"
    pypi = "cylc-rose/cylc-rose-1.3.0.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0-only")

    version("1.3.0", sha256="017072b69d7a50fa6d309a911d2428743b07c095f308529b36b1b787ebe7ab88")

    depends_on("py-setuptools", type="build")
    depends_on("py-metomi-rose@2.1", type=("build", "run"))
    depends_on("py-cylc-flow@8.2", type=("build", "run"))
    depends_on("py-metomi-isodatetime", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
