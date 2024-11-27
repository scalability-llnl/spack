# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spatialdata(AutotoolsPackage):
    """SpatialData provides an interface to Proj.4 for converting coordinates

    Spatialdata is a C++ library for

    interpolating values for spatially distributed data,
    converting coordinates among geographic projections using Proj,
    nondimensionalization of quantities,
    specification of units via Pyre (optional).

    This library is used in the finite-element code PyLith
    (https://github.com/geodynamics/pylith). The primary focus is specification
    of parameters that vary in space, such as values for boundary conditions
    and parameters of constitutive models. This provides a specification of
    these parameters independent of the discretization."""

    homepage = "https://geodynamics.org/resources/spatialdata/"
    url = "https://github.com/geodynamics/spatialdata/archive/refs/tags/v3.1.0.tar.gz"
    git = "https://github.com/geodynamics/spatialdata.git"

    license("MIT", checked_by="downloadico")

    version("develop", branch="develop", submodules="true")
    version("3.1.0", sha256="dd6caccbf41a51928183d6a1caf2380aa0ed0f2c8c71ecc9b2cd9e3f23aa418c")

    depends_on("cxx", type="build")  # generated

    # M4 macros shared for the CIG codes
    resource(
        name="autoconf_cig",
        git="https://github.com/geodynamics/autoconf_cig.git",
        commit="e490e14fb13595428d39055304bcf0ee7ab94806",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("swig", type="build")

    depends_on("python")
    depends_on("py-setuptools")
    depends_on("py-cig-pythia")
    depends_on("proj@6:")
    depends_on("py-numpy")

    def autoreconf(self, spec, prefix):
        autoupdate("--include=autoconf_cig", "--include=m4")
        autoreconf(
            "--install",
            "--verbose",
            "--force",
            "--include=autoconf_cig",
            "--include=m4",
            "--include=" + spec["libtool"].prefix + "/share/aclocal/",
        )

    def configure_args(self):
        args = []
        args.append("--enable-swig")
        return args
