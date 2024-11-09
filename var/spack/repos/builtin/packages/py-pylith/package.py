# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylith(AutotoolsPackage, PythonExtension):
    """PyLith does dynamic and quasi-static simulations of crustal deformation.
    PyLith is an open-source finite-element code for dynamic and quasi-static
    simulations of crustal deformation, primarily earthquakes and volcanoes."""

    homepage = "https://geodynamics.org/resources/pylith"
    url = "https://github.com/geodynamics/pylith/releases/download/v4.0.0/pylith-4.0.0.tar.gz"

    license("MIT", checked_by="downloadico")

    version("4.0.0", sha256="31e0131683292ee2e62f2c818cc2777f026104ae73d7a8368975dd6560292689")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools")
    depends_on("py-cig-pythia")
    depends_on("spatialdata")
    depends_on("netcdf-c")
    depends_on("petsc@=3.20.2+hdf5")
    depends_on("py-h5py")
