# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFfc(PythonPackage):
    """The FEniCS Form Compiler FFC is a compiler for finite element
    variational forms, translating high-level mathematical descriptions
    of variational forms into efficient low-level C++ code for finite
    element assembly."""

    homepage = "https://fenicsproject.org/"
    git = "https://bitbucket.org/fenics-project/ffc.git"
    url = "https://bitbucket.org/fenics-project/ffc/downloads/ffc-2019.1.0.post0.tar.gz"
    maintainers("emai-imcs")

    license("LGPL-3.0-or-later")
    version("master", branch="master")
    version(
        "2019.1.0.post0", sha256="306e1179630200a34202975a5369194939b3482eebfc34bc44ad74dab1f109e8"
    )
    version("2018.1.0", sha256="c5a6511693106d1cd2fc013148d0cd01cd1b99fc65dab461ca0b95851a9ea271")
    version(
        "2017.2.0.post0", sha256="1969a5460cb866c478df64874ce213f81cb5c893b89f991a578e258b1a64fee5"
    )
    version("2016.2.0", sha256="097c284780447ea7bb47d4d51956648a1efb2cb9047eb1382944421dde351ecb")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))

    for ver in ["2019.1.0.post0", "2018.1.0", "2017.2.0.post0", "2016.2.0"]:
        if ver in ["2019.1.0.post0", "2017.2.0.post0"]:
            ver = ver[: ver.rfind(".post")]
        wver = "@" + ver
        depends_on("py-fenics-fiat{0}".format(wver), type=("build", "run"), when=wver)
        if Version(ver) < Version("2017.2.0"):
            depends_on("py-fenics-instant{0}".format(wver), type=("build", "run"), when=wver)
        else:
            depends_on("py-fenics-dijitso{0}".format(wver), type=("build", "run"), when=wver)
        depends_on("py-fenics-ufl{0}".format(wver), type=("build", "run"), when=wver)

    depends_on("py-fenics-fiat@2019.1.0", type=("build", "run"), when="@master")
    depends_on("py-fenics-dijitso@master", type=("build", "run"), when="@master")
    depends_on("py-fenics-ufl-legacy@main", type=("build", "run"), when="@master")
