# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Boostmplcartesianproduct(Package):
    """Cartesian_product is an extension to the Boost.MPL library and as such
    requires a version of the Boost libraries on your system.
    """

    homepage = "http://www.organicvectory.com/index.php?option=com_content&view=article&id=75:boostmplcartesianproduct&catid=42:boost&Itemid=78"
    url = "https://github.com/quinoacomputing/BoostMPLCartesianProduct/tarball/20161205"

    version("20161205", sha256="1fa8e367e4dc545b34016bf57d802858ce38baf40aff20f7c93b329895a18572")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree("boost/mpl", join_path(prefix.include, "boost", "mpl"))
