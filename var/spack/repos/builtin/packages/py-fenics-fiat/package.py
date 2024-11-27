# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFiat(PythonPackage):
    """The FInite element Automatic Tabulator FIAT supports generation of
    arbitrary order instances of the Lagrange elements on lines, triangles, and
    tetrahedra. It is also capable of generating arbitrary order instances of
    Jacobi-type quadrature rules on the same element shapes. Further, H(div)
    and H(curl) conforming finite element spaces such as the families of
    Raviart-Thomas, Brezzi-Douglas-Marini and Nedelec are supported on
    triangles and tetrahedra. Upcoming versions will also support Hermite and
    nonconforming elements"""

    homepage = "https://fenicsproject.org/"
    url = "https://github.com/FEniCS/fiat/archive/2019.1.0.tar.gz"
    git = "https://github.com/FEniCS/fiat.git"
    maintainers("js947", "chrisrichardson")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("2019.1.0", sha256="2a6d175a825ed725843918ef28846edbcf710a879c2fe8caaeda77b1ce9b9a1c")
    version("2018.1.0", sha256="7468709c7aacf7dfb22c09fb5250448eb24084b9dd088ec2632a96d56c0f3830")
    version("2017.2.0", sha256="e4d3ffc86a0a717b3f17b9bb2d922214c342be27e5bdfbe50f110030bfff9729")
    version(
        "2017.1.0.post1", sha256="1784fe1cb9479ca7cd85f63b0afa6e07634feec8d8e82fa8be4c480649cb9621"
    )
    version("2017.1.0", sha256="d4288401ad16c4598720f9db0810a522f7f0eadad35d8211bac7120bce5fde94")
    version("2016.2.0", tag="fiat-2016.2.0", commit="e021c825cab938ae8809b738410cda26e392db05")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-sympy", type=("build", "run"), when="@2019.1.0")
    # avoid compilation error of dolfin (ffc fails with latest sympy)
    depends_on("py-sympy@1.0", type=("build", "run"), when="@:2018.1.0")
