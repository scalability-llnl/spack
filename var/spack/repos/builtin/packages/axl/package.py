# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.error import SpackError
from spack.package import *


def async_api_validator(pkg_name, variant_name, values):
    if "none" in values and len(values) != 1:
        raise SpackError("The value 'none' is not usable" " with other async_api values.")
    if "intel_cppr" in values and "cray_dw" in values:
        raise SpackError("The 'intel_cppr' and 'cray_dw' asynchronous" " APIs are incompatible.")


class Axl(CMakePackage):
    """Asynchronous transfer library"""

    homepage = "https://github.com/ecp-veloc/AXL"
    url = "https://github.com/ecp-veloc/AXL/archive/v0.4.0.tar.gz"
    git = "https://github.com/ecp-veloc/axl.git"
    tags = ["ecp"]

    maintainers("CamStan", "gonsie")

    license("MIT")

    version("main", branch="main")
    version("0.9.0", sha256="da2d74092fb230754a63db3cd5ba72a233ee8153dec28cc604fa8465280299ba")
    version("0.8.0", sha256="9fcd4eae143a67ff02622feda2a541b85e9a108749c039faeb473cbbc2330459")
    version("0.7.1", sha256="526a055c072c85cc989beca656717e06b128f148fda8eb19d1d9b43a3325b399")
    version("0.7.0", sha256="840ef61eadc9aa277d128df08db4cdf6cfa46b8fcf47b0eee0972582a61fbc50")
    version("0.6.0", sha256="86edb35f99b63c0ffb9dd644a019a63b062923b4efc95c377e92a1b13e79f537")
    version("0.5.0", sha256="9f3bbb4de563896551bdb68e889ba93ea1984586961ad8c627ed766bff020acf")
    version("0.4.0", sha256="0530142629d77406a00643be32492760c2cf12d1b56c6b6416791c8ff5298db2")
    version("0.3.0", sha256="737d616b669109805f7aed1858baac36c97bf0016e1115b5c56ded05d792613e")
    version(
        "0.2.0",
        sha256="d04a445f102b438fe96a1ff3429790b0c035f0d23c2797bb5601a00b582a71fc",
        deprecated=True,
    )
    version(
        "0.1.1",
        sha256="36edac007938fe47d979679414c5c27938944d32536e2e149f642916c5c08eaa",
        deprecated=True,
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("kvtree")
    depends_on("zlib-api", type="link")

    depends_on("kvtree@main", when="@main")
    depends_on("kvtree@:1.2.0", when="@:0.5.0")
    depends_on("kvtree@1.3.0", when="@0.6.0:0.7.1")
    depends_on("kvtree@1.4.0:", when="@0.8.0:")

    variant(
        "async_api",
        default="daemon",
        description="Set of async transfer APIs to enable",
        values=["cray_dw", "intel_cppr", "daemon", "none"],
        multi=True,
        validator=async_api_validator,
    )

    variant("mpi", default=True, description="Build with MPI support", when="@0.7.1:")
    depends_on("mpi", when="@0.7.1: +mpi")

    variant("pthreads", default=True, description="Enable Pthread support", when="@0.6:")

    variant("bbapi", default=True, description="Enable IBM BBAPI support")

    variant(
        "bbapi_fallback",
        default=False,
        description="Using BBAPI, if source or destination don't support \
            file extents then fallback to pthreads",
    )

    variant("dw", default=False, description="Enable Cray DataWarp support")

    variant("shared", default=True, description="Build with shared libraries")
    depends_on("kvtree+shared", when="@0.5: +shared")
    depends_on("kvtree~shared", when="@0.5: ~shared")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define("WITH_KVTREE_PREFIX", spec["kvtree"].prefix))

        args.append(self.define_from_variant("MPI"))
        if spec.satisfies("+mpi"):
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))

        if spec.satisfies("@:0.3.0"):
            apis = list(spec.variants["async_api"].value)
            if "daemon" in apis:
                args.append("-DAXL_ASYNC_DAEMON=ON")
                apis.remove("daemon")

            for api in apis:
                args.append("-DAXL_ASYNC_API={0}".format(api.upper()))

        if spec.satisfies("@0.4.0:"):
            args.append(self.define_from_variant("ENABLE_BBAPI_FALLBACK", "bbapi_fallback"))

        if spec.satisfies("@0.5.0:"):
            args.append(self.define_from_variant("ENABLE_IBM_BBAPI", "bbapi"))
            args.append(self.define_from_variant("ENABLE_CRAY_DW", "dw"))
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        if spec.satisfies("@0.6.0:"):
            args.append(self.define_from_variant("ENABLE_PTHREADS", "pthreads"))

        return args
