# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openturns(CMakePackage):
    """OpenTURNS is a scientific C++ and Python library featuring an
    internal data model and algorithms dedicated to the treatment of
    uncertainties. The main goal of this library is to provide all
    functionalities needed to treat uncertainties in studies with
    industrial applications. Targeted users are all engineers who want
    to introduce the probabilistic dimension in their so far
    deterministic studies."""

    homepage = "https://openturns.github.io/www/"
    url = "https://github.com/openturns/openturns/archive/refs/tags/v1.18.tar.gz"
    git = "https://github.com/openturns/openturns.git"
    maintainers("liuyangzhuan")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("1.20", sha256="2be5247f0266d153619b35dfb1eeeb46736c502dad993b40aff8857d6314f293")
    version("1.19", sha256="1d61cb6ce8ec1121db9f1e9fb490aaa056d2ff250db26df05d2e3e30ceb32344")
    version("1.18", sha256="1840d3fd8b38fd5967b1fa04e49d8f760c2c497400430e97623595ca48754ae0")

    variant("python", default=True, description="Build Python bindings")
    variant("libxml2", default=False, description="Use LibXML2 for XML support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@2.8:", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")

    depends_on("lapack")
    depends_on("boost+system+serialization+thread")
    depends_on("intel-tbb")
    depends_on("libxml2", when="+libxml2")

    with when("+python"):
        extends("python")
        depends_on("swig")
        depends_on("py-numpy@1.7:", type=("build", "run"))
        depends_on("py-pandas", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
        depends_on("py-cloudpickle", type=("build", "run"))
        depends_on("py-urllib3", type=("build", "run"))

    def cmake_args(self):
        args = [
            self.define("USE_BISON", True),
            self.define("USE_BOOST", True),
            self.define("USE_FLEX", True),
            self.define("USE_OPENMP", True),
            self.define("USE_TBB", True),
            self.define("LAPACK_LIBRARIES", list(self.spec["lapack"].libs)),
            self.define_from_variant("USE_LIBXML2", "libxml2"),
            # disable optional features explicitly
            self.define("USE_BONMIN", False),
            self.define("USE_CERES", False),
            self.define("USE_CMINPACK", False),
            self.define("USE_CUBA", False),
            self.define("USE_DLIB", False),
            self.define("USE_DOXYGEN", False),
            self.define("USE_HDF5", False),
            self.define("USE_HMAT", False),
            self.define("USE_IPOPT", False),
            self.define("USE_MPC", False),
            self.define("USE_MPFR", False),
            self.define("USE_MUPARSER", False),
            self.define("USE_NANOFLANN", False),
            self.define("USE_NLOPT", False),
            self.define("USE_PAGMO", False),
            self.define("USE_PRIMESIEVE", False),
            self.define("USE_SPECTRA", False),
            self.define("USE_SPHINX", False),
        ]

        if self.spec.satisfies("+python"):
            args.append(self.define("PYTHON_SITE_PACKAGES", python_platlib))

        return args
