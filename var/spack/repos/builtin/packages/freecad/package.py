# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freecad(CMakePackage):
    """FreeCAD is an open-source parametric 3D modeler made primarily
    to design real-life objects of any size. Parametric modeling
    allows you to easily modify your design by going back into your
    model history to change its parameters."""

    homepage = "https://www.freecad.org/"
    url = "https://github.com/FreeCAD/FreeCAD/archive/refs/tags/0.20.2.tar.gz"

    maintainers("aweits")

    license("LGPL-2.0-or-later")

    version("0.20.2", sha256="46922f3a477e742e1a89cd5346692d63aebb2b67af887b3e463e094a4ae055da")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("opencascade")
    depends_on("xerces-c")
    depends_on("vtk")
    depends_on("salome-med")
    depends_on(
        "boost+python+filesystem+date_time+graph+iostreams+program_options+regex+serialization+system+thread"  # noqa: E501
    )
    depends_on("qt@5:")
    depends_on("swig", type="build")
    depends_on("netgen")
    depends_on("pcl")
    depends_on("coin3d")
    depends_on("python")
    depends_on("gmsh+opencascade")
    depends_on("py-pyside2@1.2.4:", type=("build", "run"))
    depends_on("py-matplotlib@3.0.2:", type=("build", "run"))
    depends_on("py-six@1.12.0:", type=("build", "run"))
    depends_on("py-markdown@3.2.2:", type=("build", "run"))
    depends_on("py-pivy", type=("build", "run"))
    depends_on("py-pybind11", type="build")

    def patch(self):
        filter_file(
            "# include <Standard_TooManyUsers.hxx>", "", "src/Mod/Part/App/OCCError.h", string=True
        )
        filter_file('putenv("PYTHONPATH=");', "", "src/Main/MainGui.cpp", string=True)
        filter_file('_putenv("PYTHONPATH=");', "", "src/Main/MainGui.cpp", string=True)

    def cmake_args(self):
        args = []
        # requires qt5 + webkit, which requires python2
        args.append("-DBUILD_WEB=OFF")
        args.append("-DFREECAD_USE_PYBIND11:BOOL=ON")
        args.append("-DFREECAD_USE_PCL:BOOL=ON")
        # TODO:
        #       args.append("-DBUILD_FEM_NETGEN:BOOL=ON")
        #       args.append("-DNETGEN_INCLUDEDIR={}".format(self.spec["netgen"].prefix.include))
        return args
