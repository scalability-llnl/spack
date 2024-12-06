# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEnvisage(PythonPackage):
    """Envisage is a Python-based framework for building extensible
    applications, that is, applications whose functionality can be extended by
    adding "plug-ins". Envisage provides a standard mechanism for features to
    be added to an application, whether by the original developer or by someone
    else. In fact, when you build an application using Envisage, the entire
    application consists primarily of plug-ins. In this respect, it is similar
    to the Eclipse and Netbeans frameworks for Java applications."""

    homepage = "https://github.com/enthought/envisage"
    pypi = "envisage/envisage-4.9.2.tar.gz"

    license("BSD-3-Clause")

    version("6.0.1", sha256="8864c29aa344f7ac26eeb94788798f2d0cc791dcf95c632da8d79ebc580e114c")
    version("4.9.2", sha256="ed9580ac6ea17b333f1cce5b94656aed584798d56d8bd364f996a06fe1ac32eb")

    depends_on("python@3.6:", when="@5:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@:4", type=("build", "run"))
    depends_on("py-apptools", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-six", when="@:4", type=("build", "run"))
    depends_on("py-traits@6.2:", when="@6:", type=("build", "run"))
    depends_on("py-traits", type=("build", "run"))
