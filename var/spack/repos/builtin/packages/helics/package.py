# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Helics(CMakePackage):
    """HELICS is a general-purpose, modular, highly-scalable co-simulation
    framework that runs cross-platform (Linux, Windows, and Mac OS X) and
    supports both event driven and time series simulation."""

    homepage = "https://github.com/GMLC-TDC/HELICS"
    url = "https://github.com/GMLC-TDC/HELICS/releases/download/v2.4.1/Helics-v2.4.1-source.tar.gz"
    git = "https://github.com/GMLC-TDC/HELICS.git"

    maintainers("nightlark")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=True)
    version("main", branch="main", submodules=True)
    version("master", branch="main", submodules=True)
    version("3.5.3", sha256="f9ace240510b18caf642f55d08f9009a9babb203fbc032ec7d7d8aa6fd5e1553")
    version("3.5.2", sha256="c2604694698a1e33c4a68f3d1c5ab0a228ef2bfca1b0d3bae94801dbd3b11048")
    version("3.5.1", sha256="546fc6e6a85de6ba841e4bd547b811cc81a67a22be5e212ccb54be139d740555")
    version("3.5.0", sha256="0c02ebaecf3d4ead7911e13325b26706f1e4b316ca51ec609e969e18ec584b78")
    version("3.4.0", sha256="88877a3767de9aed9f1cddea7b6455a2be060a00b959bb7e94994d1fd20878f8")
    version("3.3.2", sha256="b04013969fc02dc36c697c328e6f50a0ac8dbdaf3d3e69870cd6e6ebeb374286")
    version("3.3.1", sha256="0f6357e6781157515230d14033afc8769a02971a1870909e5697415e1db2e03f")
    version("3.3.0", sha256="0c2fe0eb2bfc527901a50bbdaa742a7c4b9424dc8fa326ca614157613dcd1457")
    version("3.2.1", sha256="9df8a7a687c7cf8ea6f157e748e57e8bf5cefa9a49a24e7c590fe9191291da95")
    version("3.2.0", sha256="b9cec50b9e767113b2e04a5623437885f76196cc9a58287e21f5c0f62c32cca1")
    version("3.1.2", sha256="eed5daff8ce131c86e972383a1e67933ddac97be5345d41b41ef71663eb097bb")
    version("3.1.1", sha256="65791ddede5f06aff58daa7cf0b9d244baa6c4e08e119ca010ddcc6137a479d9")
    version("3.1.0", sha256="b6f97c8ce3c4c18dce8e868a366782b726077165204d631a5c580682f872ffd7")
    version("3.0.1", sha256="512afc18e25311477ec82804de74c47a674aa213d2173c276b6caf555b8421dd")
    version("3.0.0", sha256="928687e95d048f3f9f9d67cec4ac20866a98cbc00090a2d62abaa11c2a20958c")
    version("2.8.1", sha256="9485091fb1bf5d0dd3b21a2641dd78051bbf5374cd823425e458053abafdfa1f")
    version("2.8.0", sha256="f2b218494407573c75561b7d4d656bc60f7592e970dd87d98c969066d76d89c1")
    version("2.7.1", sha256="872d415959e9d97069b06327410af00e7daae8dbeb9f050b26632eca924ea23c")
    version("2.7.0", sha256="ad005c0948ef4284417d429112772d0b63ebfbc62c9093c02ac10f4a333d70f4")
    version("2.6.1", sha256="4b9a733a568ae8e6492f93abcd43f1aa9c53b233edcbeb0ab188dcc0d73ac928")
    version("2.6.0", sha256="450cbfc0c37b77ea051d3edc12bbc0f7cf4c1a17091ae10df5214b6176eebb42")
    version("2.5.2", sha256="81928f7e30233a07ae2bfe6c5489fdd958364c0549b2a3e6fdc6163d4b390311")
    version("2.5.1", sha256="3fc3507f7c074ff8b6a17fe54676334158fb2ff7cc8e7f4df011938f28fdbbca")
    version("2.5.0", sha256="6f4f9308ebb59d82d71cf068e0d9d66b6edfa7792d61d54f0a61bf20dd2a7428")
    version("2.4.2", sha256="957856f06ed6d622f05dfe53df7768bba8fe2336d841252f5fac8345070fa5cb")
    version("2.4.1", sha256="ac077e9efe466881ea366721cb31fb37ea0e72a881a717323ba4f3cdda338be4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("apps", default=True, description="Install the HELICS apps executables")
    variant("apps_lib", default=True, description="Install the HELICS apps library")
    variant("benchmarks", default=False, description="Install the HELICS benchmarks")
    variant("c_shared", default=True, description="Install the C shared library")
    variant("cxx_shared", default=True, description="Install the CXX shared library")
    variant("zmq", default=True, description="Enable ZeroMQ core types")
    variant("tcp", default=True, description="Enable TCP core types")
    variant("udp", default=True, description="Enable UDP core type")
    variant("ipc", default=True, description="Enable IPC core type")
    variant("inproc", default=True, description="Enable in-process core type")
    variant("mpi", default=False, description="Enable MPI core type")
    variant("boost", default=True, description="Compile with Boost libraries")
    variant("asio", default=True, description="Compile with ASIO libraries")
    variant("swig", default=False, description="Build language bindings with SWIG")
    variant(
        "webserver",
        default=True,
        description="Enable the integrated webserver in the HELICS broker server",
    )
    variant(
        "encryption",
        default=True,
        when="@3.2.0:",
        description="Enable support for encrypted communication",
    )
    variant(
        "python",
        default=False,
        when="@:2",
        description="Enable building Python interface (split into separate repo in v3)",
    )

    # Build dependency
    depends_on("git", type="build", when="@master:")
    depends_on("cmake@3.4:", type="build", when="@:2")
    depends_on("cmake@3.10:", type="build", when="@3.0.0:3.2.1")
    depends_on("cmake@3.11:", type="build", when="@3.3.0:")
    depends_on("boost@1.70:", type="build", when="+boost")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type="build", when="+boost")
    depends_on("swig@3.0:", type="build", when="+swig")

    depends_on("libzmq@4.3:", when="+zmq")
    depends_on("mpi@2", when="+mpi")
    depends_on("openssl@1.1.1:", when="+encryption")

    # SWIG generated Python interface only works with HELICS <=2.x
    depends_on("python@3:", when="@:2 +python")

    # Compiler restrictions based on C++ standard supported
    conflicts("%gcc@:6", when="@3.0.0:", msg="HELICS 3+ cannot be built with GCC older than 7.0")
    conflicts(
        "%clang@:4", when="@3.0.0:", msg="HELICS 3+ cannot be built with Clang older than 5.0"
    )
    conflicts("%intel@:18", when="@3.0.0:", msg="HELICS 3+ cannot be built with ICC older than 19")

    # OpenMPI doesn't work with HELICS <=2.4.1
    conflicts("^openmpi", when="@:2.4.1 +mpi")

    # Boost is required for ipc and webserver options
    conflicts("+ipc", when="~boost")
    conflicts("+webserver", when="~boost")

    # ASIO (vendored in HELICS repo) is required for tcp and udp options
    conflicts("+tcp", when="~asio")
    conflicts("+udp", when="~asio")

    extends("python", when="+python")

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant
        args = ["-DHELICS_BUILD_EXAMPLES=OFF", "-DHELICS_BUILD_TESTS=OFF"]

        # HELICS core type CMake options
        # Options were renamed in v3
        pre = "HELICS_" if spec.satisfies("@3:") else ""
        args.append(from_variant("{0}ENABLE_ZMQ_CORE".format(pre), "zmq"))
        args.append(from_variant("{0}ENABLE_TCP_CORE".format(pre), "tcp"))
        args.append(from_variant("{0}ENABLE_UDP_CORE".format(pre), "udp"))
        args.append(from_variant("{0}ENABLE_IPC_CORE".format(pre), "ipc"))
        args.append(from_variant("{0}ENABLE_INPROC_CORE".format(pre), "inproc"))
        args.append(from_variant("{0}ENABLE_MPI_CORE".format(pre), "mpi"))

        # HELICS shared library options
        args.append(
            "-DHELICS_DISABLE_C_SHARED_LIB={0}".format(
                "OFF" if spec.satisfies("+c_shared") else "ON"
            )
        )
        args.append(from_variant("HELICS_BUILD_CXX_SHARED_LIB", "cxx_shared"))

        # HELICS executable app options
        args.append(from_variant("HELICS_BUILD_APP_EXECUTABLES", "apps"))
        args.append(from_variant("HELICS_BUILD_APP_LIBRARY", "apps_lib"))
        args.append(
            "-DHELICS_DISABLE_WEBSERVER={0}".format(
                "OFF" if spec.satisfies("+webserver") else "ON"
            )
        )
        args.append(from_variant("HELICS_BUILD_BENCHMARKS", "benchmarks"))

        # Extra HELICS library dependencies
        args.append(
            "-DHELICS_DISABLE_BOOST={0}".format("OFF" if spec.satisfies("+boost") else "ON")
        )
        args.append("-DHELICS_DISABLE_ASIO={0}".format("OFF" if spec.satisfies("+asio") else "ON"))

        # Encryption
        args.append(from_variant("HELICS_ENABLE_ENCRYPTION", "encryption"))

        # SWIG
        args.append(from_variant("HELICS_ENABLE_SWIG", "swig"))

        # Python
        if spec.satisfies("@:2"):
            # Python interface was removed from the main HELICS build in v3
            args.append(from_variant("BUILD_PYTHON_INTERFACE", "python"))

        # GCC >=13
        if spec.satisfies("%gcc@13:"):
            # C++20 required when building with GCC>=13
            args.append("-DCMAKE_CXX_STANDARD=20")

        return args

    def setup_run_environment(self, env):
        spec = self.spec
        if spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.prefix.python)
