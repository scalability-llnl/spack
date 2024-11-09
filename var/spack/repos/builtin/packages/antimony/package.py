# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Antimony(CMakePackage):
    """Human readable language for modifying sbml"""

    homepage = "https://antimony.sourceforge.net/"
    url = "antimony"

    maintainers("rblake-llnl")

    license("BSD-3-Clause")

    version("2.8", sha256="7e3e38706c074b72e241ac56ef4ce23e87ef8c718c70f29b2207f1847c43770f")
    version("2.7", sha256="7ad181cac632282ae77ced09388dd92db87ea4683eed8c45f2b43861ae2acad4")
    version("2.6", sha256="afc8dc5ec6bc2cd3085038f80362327456f219171b09a13f775b50550c8b1d87")
    version("2.5", sha256="138d6b45df62198ca71bd3b3c8fd06920f8a78d7de7f6dbc1b89fa7ea7c7d215")
    version("2.4", sha256="1597efa823f9a48f5a40373cbd40386207764807fbc0b79cf20d0f8570a7e54b")
    version("2.2", sha256="795c777dd90c28fd8c3f4f8896702744b7389cff2fcf40e797b4bfafbb6f7251")
    version("2.0", sha256="778146206e5f420d0e3d30dc25eabc9bad2759bfaf6b4b355bb1f72c5bc9593f")

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/antimony/Antimony source/{0}/antimony_src_v{1}.tar.gz".format(
            version, version
        )
        return url

    variant("qt", default=False, description="Build the QT editor.")
    variant("python", default=False, description="Build python bindings.")

    depends_on("sbml~cpp")
    depends_on("swig")
    depends_on("qt", when="+qt")
    depends_on("python", when="+python")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_SBML:BOOL=ON",
            "-DWITH_COMP_SBML:BOOL=ON",
            "-DWITH_LIBSBML_EXPAT:BOOL=OFF",
            "-DWITH_LIBSBML_LIBXML:BOOL=ON",
            "-DWITH_LIBSBML_XERCES:BOOL=OFF",
            "-DLIBSBML_INSTALL_DIR:PATH=" + spec["sbml"].prefix,
            "-DWITH_CELLML:BOOL=OFF",
            "-DWITH_SBW:BOOL=OFF",
            "-DWITH_SWIG:BOOL=ON",
        ]
        args.append(self.define_from_variant("WITH_PYTHON", "python"))
        args.append(self.define_from_variant("WITH_QTANTIMONY", "qt"))
        return args
