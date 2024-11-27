# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyReacton(PythonPackage):
    """
    A way to write reusable components in a React-like way, to make Python-based UI's using
    the ipywidgets ecosystem (ipywidgets, ipyvolume, bqplot, threejs, leaflet, ipyvuetify, ...).
    """

    homepage = "https://reacton.solara.dev/en/latest/"
    pypi = "reacton/reacton-1.8.2.tar.gz"

    license("MIT")

    maintainers("jeremyfix")

    version("1.8.2", sha256="eaa4eeeffd11688d2b60a49a9895fd299f2ecbe8614f1ad61d144c56edaf7304")

    depends_on("py-hatchling", type="build")

    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-typing-extensions@4.1.1:", type=("build", "run"))
