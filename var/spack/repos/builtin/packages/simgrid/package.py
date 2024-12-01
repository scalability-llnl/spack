# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Simgrid(CMakePackage):
    """SimGrid is a framework for developing simulators of distributed
    applications targetting distributed platforms, which can in turn be
    used to prototype, evaluate and compare relevant platform configurations,
    system designs, and algorithmic approaches.
    """

    homepage = "https://simgrid.org/"
    url = "https://github.com/simgrid/simgrid/releases/download/v3.27/simgrid-3.27.tar.gz"
    git = "https://framagit.org/simgrid/simgrid.git"

    maintainers("viniciusvgp")

    license("LGPL-2.1-or-later")

    version("3.35", sha256="b4570d3de18d319cbd2e16c5a669f90760307673c0cc9940d4d11cfc537e69a8")
    version("3.34", sha256="161f1c6c0ebb588c587aea6388114307bb31b3c6d5332fa3dc678151f1d0564d")
    version("3.32", sha256="837764eb81562f04e49dd20fbd8518d9eb1f94df00a4e4555e7ec7fa8aa341f0")
    version("3.31", sha256="4b44f77ad40c01cf4e3013957c9cbe39f33dec9304ff0c9c3d9056372ed4c61d")
    version("3.30", sha256="0cad48088c106e72efb42fb423e65d77fc9053cc03d6f3a5ff7ba4c712bb4eb8")
    version("3.29", sha256="83e8afd653555eeb70dc5c0737b88036c7906778ecd3c95806c6bf5535da2ccf")
    version("3.28", sha256="558276e7f8135ce520d98e1bafa029c6c0f5c2d0e221a3a5e42c378fe0c5ef2c")
    version("3.27", sha256="51aeb9de0434066e5fec40e785f5ea9fa934afe7f6bfb4aa627246e765f1d6d7")
    version("3.26", sha256="ac50da1eacc5a53b094a988a8ecde09962c29320f346b45e74dd32ab9d9f3e96")
    version(
        "3.25",
        sha256="0b5dcdde64f1246f3daa7673eb1b5bd87663c0a37a2c5dcd43f976885c6d0b46",
        url="https://github.com/simgrid/simgrid/releases/download/v3.25/SimGrid-3.25.tar.gz",
    )
    version(
        "3.24",
        sha256="c976ed1cbcc7ff136f6d1a8eda7d9ccf090e0e16d5239e6e631047ae9e592921",
        url="https://github.com/simgrid/simgrid/releases/download/v3.24/SimGrid-3.24.tar.gz",
    )
    version(
        "3.23",
        sha256="c3c86673abf0a2685337f1f520a7782d9611cd18d0374f35e1d98652fdbbaf86",
        url="https://github.com/simgrid/simgrid/releases/download/v3.23/SimGrid-3.23.tar.gz",
    )
    version(
        "3.22",
        sha256="4fdff0a8e4c81f8edf6f7eedfa32e19748abe688d156ea9240178c558c8bad33",
        url="https://github.com/simgrid/simgrid/releases/download/v3_22/SimGrid-3.22.tar.gz",
    )
    version(
        "3.21",
        sha256="d2a6e9021016dd39a2b6f8d5d18c8223f6885746c5269550d19ba29c47c0c6a0",
        url="https://github.com/simgrid/simgrid/releases/download/v3_21/SimGrid-3.21.tar.gz",
    )
    version(
        "3.20",
        sha256="4d4757eb45d87cf18d990d589c31d223b0ea8cf6fcd8c94fca4d38162193cef6",
        url="https://github.com/simgrid/simgrid/releases/download/v3.20/SimGrid-3.20.tar.gz",
    )

    # gforge.inria.fr end of life https://gforge.inria.fr/forum/forum.php?forum_id=11543
    version(
        "3.19",
        sha256="64a3b82fdf0a65bb8b7c8e9feb01694360edaf38070097bf28aa181eccb86ea7",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/37452/SimGrid-3.19.tar.gz",
    )
    version(
        "3.18",
        sha256="dc8f6223d89326b6a21c99eabc90598fa153d6b0818a63ff5c3ec8726e2257b2",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/37294/SimGrid-3.18.tar.gz",
    )
    version(
        "3.17",
        sha256="f5e44f41983e83f65261598ab0de1909d3a8a3feb77f28e37d38f04631dbb908",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/37148/SimGrid-3.17.tar.gz",
    )
    version(
        "3.16",
        sha256="51782534fec87eed9da345319ead699b13d7dad4be7ac89984a0446cb385d3fa",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/36900/SimGrid-3.16.tar.gz",
    )
    version(
        "3.15",
        sha256="d1e411cdbfa953c018411b842727339ede6b82efcd5d3f6adc13a24f182fa9e8",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/36621/SimGrid-3.15.tar.gz",
    )
    version(
        "3.14.159",
        sha256="2d93db245c6ec8039ffe332a77531b836ad093d57f18ec3f7920fe98e3719f48",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/36384/SimGrid-3.14.159.tar.gz",
    )
    version(
        "3.13",
        sha256="7bcedd19492f9a32cc431840ad2688d0d6e4121982d6d26e0174b5c92b086121",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/35817/SimGrid-3.13.tar.gz",
    )
    version(
        "3.12",
        sha256="d397ee0273395dc687fbcd2601515e7142559801a3db387454d77e0e18cd7878",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/35215/SimGrid-3.12.tar.gz",
    )
    version(
        "3.11",
        sha256="6efb006e028e37f74a34fc37d585a8cb296720020cabad361d65662533f1600b",
        deprecated=True,
        url="https://gforge.inria.fr/frs/download.php/file/33683/SimGrid-3.11.tar.gz",
    )

    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("doc", default=False, description="Build documentation")
    variant("smpi", default=True, description="SMPI provides MPI")
    variant("examples", default=False, description="Install examples")
    variant("mc", default=False, description="Model checker")
    variant("msg", default=False, description="Enables the old MSG interface")

    # does not build correctly with some old compilers -> rely on packages
    depends_on("boost@:1.69.0", when="@:3.21")
    depends_on("boost+exception")

    conflicts(
        "%gcc@10:",
        when="@:3.23",
        msg="simgrid <= v3.23 cannot be built with gcc >= 10,"
        " please use an older release (e.g., %gcc@:9).",
    )

    def setup_dependent_package(self, module, dep_spec):
        if self.spec.satisfies("+smpi"):
            self.spec.smpicc = join_path(self.prefix.bin, "smpicc")
            self.spec.smpicxx = join_path(self.prefix.bin, "smpicxx")
            self.spec.smpifc = join_path(self.prefix.bin, "smpif90")
            self.spec.smpif77 = join_path(self.prefix.bin, "smpiff")

    def cmake_args(self):
        spec = self.spec
        args = []

        if not spec.satisfies("+doc"):
            args.append("-Denable_documentation=OFF")
        if spec.satisfies("+mc"):
            args.append("-Denable_model-checking=ON")
        if spec.satisfies("+msg"):
            args.append("-Denable_msg=ON")
        return args

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            make("install")
            if spec.satisfies("+examples"):
                install_tree(join_path(self.build_directory, "examples"), prefix.examples)
