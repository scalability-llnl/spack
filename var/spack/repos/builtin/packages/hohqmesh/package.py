# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hohqmesh(CMakePackage):
    """High Order mesh generator for Hexahedral and Quadrilateral meshes."""

    homepage = "https://github.com/trixi-framework/HOHQMesh"
    git = "https://github.com/trixi-framework/HOHQMesh.git"
    url = "https://github.com/trixi-framework/HOHQMesh/archive/v1.0.0.tar.gz"

    maintainers("fluidnumerics-joe")

    license("MIT")

    version("main", branch="main")
    version("1.5.3", sha256="5d6de1ff6472d5044997372111754dcf339603351d0c855664115353a085a21e")
    version("1.5.2", sha256="afc749f71657fc70294a00e84891463d23a57dff0c17975445f268fb417da0cc")
    version("1.5.1", sha256="3a3e0246d61d55b58f5bebc6c925f0f6df93398ad8efc52a933feab4dcf00dc1")
    version("1.5.0", sha256="e2a8ff604b93b49dbab101edd6f031e5032535ec96a84ea58906a326be1c8f04")
    version("1.4.2", sha256="656c149b510b6d3e914d1794c27b4802699c9fd209afff8aec3a219a9e7f86ff")
    version("1.4.1", sha256="bbfecdba3899bf124bdac2bf91f1262a8e2f224ba699d55bdf8546073fc62b21")
    version("1.4.0", sha256="f3a8ca4906d86360260b55cf79f66ba7e35f8c3c293ae6d83361d9edf5f70e6d")
    version("1.3.0", sha256="31ea80de15ece886df0dd1b941714d86ec06a9ed02c1415308b4ba23d8314eff")
    version("1.2.1", sha256="b1b13a680c3ef6b8d6a8d05406f68c1ff641c26f69c468ccf2d7bed8d556dd7e")
    version("1.2.0", sha256="39387276a2f145618b1ec3486426f181fc3f3fe1e85519505735a44f0b480967")
    version("1.1.0", sha256="5fdb75157d9dc29bba55e6ae9dc2be71294754204f4f0912795532ae66aada10")
    version("1.0.1", sha256="8435f13c96d714a287f3c24392330047e2131d53fafe251a77eba365bd2b3141")
    version("1.0.0", sha256="3800e63975d0a61945508f13fb76d5e2145c0260440484252b6b81aa0bfe076d")

    depends_on("fortran", type="build")  # generated

    depends_on("ftobjectlibrary")

    parallel = False
