# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GpiSpace(CMakePackage):
    """
    GPI-Space is a task-based workflow management system for parallel
    applications. It allows the developers to build domain-specific workflows
    using their own parallelization patterns, data management policies and I/O
    routines, while relying on the runtime system for the workflow management.
    The GPI-Space ecosystem "auto-manages" the application with dynamic
    scheduling, built-in distributed memory transfers and distributed tasks
    execution.
    """

    homepage = "https://www.gpi-space.de"
    url = "https://github.com/cc-hpc-itwm/gpispace/archive/refs/tags/v21.09.tar.gz"
    git = "https://github.com/cc-hpc-itwm/gpispace.git"

    maintainers("mzeyen1985", "tiberot", "rumach", "mrahn", "acastanedam")

    license("GPL-3.0-or-later")

    version("latest", branch="main")
    version("23.06", sha256="b4ee51f309c80c12a7842c0909041903608c6144535bc6faac3bbb8ff40e9213")
    version("22.12", sha256="1c0ab9a1ada9dbbc0f80fb04ddbbb24ff900231f709cb99aa63f0d135a3ad398")
    version("22.09", sha256="f938847205181081ed24896bba16302ac35bbf478b4ceecae5bb21d5a38c8556")
    version("22.06", sha256="d89d8a7b574430c4f151a3768073fa44d32e5cc7606fbe0f58aeedf6f5fefc0b")
    version("22.03", sha256="b01500b9480452aee865a0ef98cf40864f847b7e22ea572f9a6f0f5ac2ae9a1a")
    version("21.12.1", sha256="6c49aca95a32e66fa1e34bef542c2f380e91f86c9c2b3b0d98921901bab7abce")
    version("21.12", sha256="51794e2b593b8d1dc7d6310e17744842919bf44205b2cb7a79de2f2bbac3352a")
    version("21.09", sha256="7f3861c2bfec15a4da46378ea38b304e1462ed315cd315b81ab2c2a8ba50dd3e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "monitor",
        default=True,
        description="""
                    Enables the gspc-monitor application for execution monitoring.
                    """,
    )
    variant(
        "iml",
        default=True,
        description="""
                    Enables IML support
                    """,
    )
    variant(
        "network",
        default="ethernet",
        values=("infiniband", "ethernet"),
        description="GPI-2 fabric to enable",
        when="+iml",
    )

    depends_on("cmake@3.15.0:", type="build")
    depends_on("cmake@3.16.0:", type="build", when="@23.06:")
    depends_on("chrpath@0.13:", type=("build", "run"))
    depends_on("pkgconfig", type="build")
    depends_on(
        "boost@1.62.0:1.63.0"
        "+atomic +chrono +coroutine +context +date_time +filesystem +iostreams"
        " +program_options +random +regex +serialization +test +timer cxxstd=14"
    )
    depends_on("hwloc@1.10: +libudev ~libxml2 libs=static")
    depends_on("libssh2@1.7:")
    depends_on("openssl@0.9:")
    with when("+iml"):
        depends_on("gpi-2@1.3.2:1.3.3 fabrics=infiniband", when="@:22.09 network=infiniband")
        depends_on("gpi-2@1.3.2:1.3.3 fabrics=ethernet", when="@:22.09 network=ethernet")
        depends_on("gpi-2@1.5.0: fabrics=infiniband", when="@22.12: network=infiniband")
        depends_on("gpi-2@1.5.0: fabrics=ethernet", when="@22.12: network=ethernet")
    depends_on("qt@5.9:5.15", when="+monitor")

    def cmake_args(self):
        args = [
            self.define("FHG_ASSERT_MODE", False),
            self.define("INSTALL_DO_NOT_BUNDLE", True),
            self.define("BUILD_TESTING", False),
            self.define_from_variant("GSPC_WITH_MONITOR_APP", "monitor"),
            self.define_from_variant("GSPC_WITH_IML", "iml"),
        ]

        return args
