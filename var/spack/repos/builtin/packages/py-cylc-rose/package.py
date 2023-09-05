# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-cylc-rose
#
# You can edit this file again by typing:
#
#     spack edit py-cylc-rose
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyCylcRose(PythonPackage):
    """A Cylc plugin providing support for the Rose rose-suite.conf file."""

    homepage = "https://cylc.github.io/cylc-doc/latest/html/plugins/cylc-rose.html"
    pypi = "cylc-rose/cylc-rose-1.3.0.tar.gz"

    maintainers("LydDeb")

    version("1.3.0", sha256="017072b69d7a50fa6d309a911d2428743b07c095f308529b36b1b787ebe7ab88")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-metomi-rose@2.1", type=("build", "run"))
    depends_on("py-cylc-flow@8.2", type=("build", "run"))
    depends_on("py-metomi-isodatetime", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
