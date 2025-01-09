# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeopandas(PythonPackage):
    """GeoPandas is an open source project to make working with geospatial
    data in python easier. GeoPandas extends the datatypes used by pandas
    to allow spatial operations on geometric types. Geometric operations are
    performed by shapely. Geopandas further depends on fiona for file access
    and descartes and matplotlib for plotting."""

    homepage = "https://geopandas.org/"
    pypi = "geopandas/geopandas-0.8.1.tar.gz"
    git = "https://github.com/geopandas/geopandas.git"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.0.1", sha256="b8bf70a5534588205b7a56646e2082fb1de9a03599651b3d80c99ea4c2ca08ab")
    version("1.0.0", sha256="386d42c028047e2b0f09191d7859268304761c4711a247173a88891b6161f711")
    version("0.14.3", sha256="748af035d4a068a4ae00cab384acb61d387685c833b0022e0729aa45216b23ac")
    version("0.11.1", sha256="f0f0c8d0423d30cf81de2056d853145c4362739350a7f8f2d72cc7409ef1eca1")
    version("0.11.0", sha256="562fe7dc19a6e0f61532d654c4752f7bf46e0714990c5844fe3de3f9c99cb873")
    version("0.10.2", sha256="efbf47e70732e25c3727222019c92b39b2e0a66ebe4fe379fbe1aa43a2a871db")
    version("0.10.1", sha256="6429ee4e0cc94f26aff12139445196ef83fe17cadbe816925508a1799f60a681")
    version("0.10.0", sha256="3ba1cb298c8e27112debe1d5b7898f100c91cbdf66c7dbf39726d63616cf0c6b")
    version("0.9.0", sha256="63972ab4dc44c4029f340600dcb83264eb8132dd22b104da0b654bef7f42630a")
    version("0.8.2", sha256="aa9ae82e4e6b52efa244bd4b8bd2363d66693e5592ad1a0f52b6afa8c36348cb")
    version("0.8.1", sha256="e28a729e44ac53c1891b54b1aca60e3bc0bb9e88ad0f2be8e301a03b9510f6e2")
    version("0.5.0", sha256="d075d2ab61a502ab92ec6b72aaf9610a1340ec24ed07264fcbdbe944b9e68954")
    version("0.4.0", sha256="9f5d24d23f33e6d3267a633025e4d9e050b3a1e86d41a96d3ccc5ad95afec3db")
    version("0.3.0", sha256="e63bb32a3e516d8c9bcd149c22335575defdc5896c8bdf15c836608f152a920b")

    depends_on("python@3.5:", type=("build", "run"), when="@0.7:")
    depends_on("python@3.6:", type=("build", "run"), when="@0.9:")
    depends_on("python@3.7:", type=("build", "run"), when="@0.10:")
    depends_on("python@3.8:", type=("build", "run"), when="@0.11:")
    depends_on("python@3.9:", type=("build", "run"), when="@0.14:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61.0.0:", type="build", when="@0.14:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"), when="@0.14.4:")
    # Only for versions 0.x.y - replaced by py-pyogrio
    depends_on("py-fiona", type=("build", "run"), when="@:0.99")
    depends_on("py-fiona@1.8:", type=("build", "run"), when="@0.9:0.99")
    depends_on("py-fiona@1.8.21:", type=("build", "run"), when="@0.14:0.99")
    # Only for versions 1.x.y - replaces py-fiona
    depends_on("py-pyogrio@0.7.2:", type=("build", "run"), when="@1:")
    depends_on("py-packaging", type=("build", "run"), when="@0.11:")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pandas@0.23.0:", type=("build", "run"), when="@0.6:")
    depends_on("py-pandas@0.24.0:", type=("build", "run"), when="@0.9:")
    depends_on("py-pandas@0.25.0:", type=("build", "run"), when="@0.10:")
    depends_on("py-pandas@1.0.0:", type=("build", "run"), when="@0.11:")
    depends_on("py-pandas@1.4.0:", type=("build", "run"), when="@0.14:")
    depends_on("py-pyproj", type=("build", "run"))
    depends_on("py-pyproj@2.2.0:", type=("build", "run"), when="@0.7:")
    depends_on("py-pyproj@2.6.1.post1:", type=("build", "run"), when="@0.11:")
    depends_on("py-pyproj@3.3.0:", type=("build", "run"), when="@0.14:")
    depends_on("py-shapely@:1", type=("build", "run"), when="@:0.99")
    depends_on("py-shapely@1.6:1", type=("build", "run"), when="@0.9:0.10")
    depends_on("py-shapely@1.7:1", type=("build", "run"), when="@0.11:0.99")
    depends_on("py-shapely@1.8.0:", type=("build", "run"), when="@0.14:")
    depends_on("py-shapely@2.0.0:", type=("build", "run"), when="@1:")
