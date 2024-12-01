# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.platforms.cray
from spack.package import *


class Libfabric(AutotoolsPackage, CudaPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
    fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url = "https://github.com/ofiwg/libfabric/releases/download/v1.8.0/libfabric-1.8.0.tar.bz2"
    git = "https://github.com/ofiwg/libfabric.git"
    maintainers("rajachan")

    executables = ["^fi_info$"]

    license("GPL-2.0-or-later")

    version("main", branch="main")
    version("1.22.0", sha256="485e6cafa66c9e4f6aa688d2c9526e274c47fda3a783cf1dd8f7c69a07e2d5fe")
    version("1.21.1", sha256="54befa6697352f3179c79c4a79225ae71694f29eefad5d0d5a14b5444ff986dd")
    version("1.21.0", sha256="0c1b7b830d9147f661e5d7f359250b85b5a9885c330464cd3b5e5d35b86551c7")
    version("1.20.2", sha256="75b89252a0b8b3eae8e60f7098af1598445a99a99e8fc1ff458e2fd5d4ef8cde")
    version("1.20.1", sha256="fd88d65c3139865d42a6eded24e121aadabd6373239cef42b76f28630d6eed76")
    version("1.20.0", sha256="7fbbaeb0e15c7c4553c0ac5f54e4ef7aecaff8a669d4ba96fa04b0fc780b9ddc")
    version("1.19.1", sha256="b8839e56d80470a917453a7d8ad9cb717f6683fee28cf93de5f3a056ed4f04c8")
    version("1.19.0", sha256="f14c764be9103e80c46223bde66e530e5954cb28b3835b57c8e728479603ef9e")
    version("1.18.2", sha256="64d7837853ca84d2a413fdd96534b6a81e6e777cc13866e28cf86cd0ccf1b93e")
    version("1.18.1", sha256="4615ae1e22009e59c72ae03c20adbdbd4a3dce95aeefbc86cc2bf1acc81c9e38")
    version("1.18.0", sha256="912fb7c7b3cf2a91140520962b004a1c5d2f39184adbbd98ae5919b0178afd43")
    version("1.17.1", sha256="8b372ddb3f46784c53fdad50a701a6eb0e661239aee45a42169afbedf3644035")
    version("1.17.0", sha256="579c0f5ef636c0c72f4d3d6bd4da91a5aed9ac3ac4ea387404c45dbbdee4745d")
    version("1.16.1", sha256="53f992d33f9afe94b8a4ea3d105504887f4311cf4b68cea99a24a85fcc39193f")
    version("1.16.0", sha256="ac104b9d6e3ce8bda6116329e3f440b621d85602257b3015116ca590f65267d2")
    version("1.15.2", sha256="8d050b88bee62e8512a88f5aa25f532f46bef587bc3f91022ecdb9b3b2676c7e")
    version("1.15.1", sha256="cafa3005a9dc86064de179b0af4798ad30b46b2f862fe0268db03d13943e10cd")
    version("1.15.0", sha256="70982c58eadeeb5b1ddb28413fd645e40b206618b56fbb2b18ab1e7f607c9bea")
    version("1.14.1", sha256="6cfabb94bca8e419d9015212506f5a367d077c5b11e94b9f57997ec6ca3d8aed")
    version("1.14.0", sha256="fc261388848f3cff555bd653f5cb901f6b9485ad285e5c53328b13f0e69f749a")
    version("1.13.2", sha256="25d783b0722a8df8fe61c1de75fafca684c5fe520303180f26f0ad6409cfc0b9")
    version("1.13.1", sha256="8e6eed38c4a39aa4cbf7d5d3734f0eecbfc030182f1f9b3be470702f2586d30e")
    version("1.12.1", sha256="db3c8e0a495e6e9da6a7436adab905468aedfbd4579ee3da5232a5c111ba642c")
    version("1.12.0", sha256="ca98785fe25e68a26c61e272be64a1efeea37e61b0dcebd34ccfd381bda7d9cc")
    version("1.11.2", sha256="ff2ba821b55a54855d327e6f6fb8a14312c9c9ca7c873525b6a246d8f974d7da")
    version("1.11.1", sha256="a72a7dac6322bed09ef1af33bcade3024ca5847a1e9c8fa369da6ab879111fe7")
    version("1.11.0", sha256="9938abf628e7ea8dcf60a94a4b62d499fbc0dbc6733478b6db2e6a373c80d58f")
    version("1.10.1", sha256="889fa8c99eed1ff2a5fd6faf6d5222f2cf38476b24f3b764f2cbb5900fee8284")
    version("1.10.0", sha256="c1ef6e9cd6dafec3f003d2f78f0f3a25f055a7a791e98b5a0db1e4c5036e40f6")
    version("1.9.1", sha256="c305c6035c992523e08c7591a6a3707225ba3e72de40443eaed837a10df6771a")
    version("1.9.0", sha256="559bfb7376c38253c936d0b104591c3394880376d676894895706c4f5f88597c")
    version("1.8.1", sha256="3c560b997f9eafd89f961dd8e8a29a81aad3e39aee888e3f3822da419047dc88")
    version("1.8.0", sha256="c4763383a96af4af52cd81b3b094227f5cf8e91662f861670965994539b7ee37")
    version("1.7.1", sha256="f4e9cc48319763cff4943de96bf527b737c9f1d6ac3088b8b5c75d07bd719569")
    version("1.7.0", sha256="b3dd9cc0fa36fe8c3b9997ba279ec831a905704816c25fe3c4c09fc7eeceaac4")
    version("1.6.2", sha256="ec63f61f5e529964ef65fd101627d8782c0efc2b88b3d5fc7f0bfd2c1e95ab2c")
    version("1.6.1", sha256="33215a91450e2234ebdc7c467f041b6757f76f5ba926425e89d80c27b3fd7da2")
    version("1.6.0", sha256="b3ce7bd655052ea4da7bf01a3177d96d94e5f41b3fd6011ac43f50fcb2dc7581")
    version("1.5.3", sha256="f62a40da06f8951db267a59a4ee7363b6ee60a7abbc55cd5db6c8b067d93fa0c")
    version("1.5.0", sha256="88a8ad6772f11d83e5b6f7152a908ffcb237af273a74a1bd1cb4202f577f1f23")
    version("1.4.2", sha256="5d027d7e4e34cb62508803e51d6bd2f477932ad68948996429df2bfff37ca2a5")

    depends_on("c", type="build")  # generated

    fabrics = (
        conditional("cxi", when=spack.platforms.cray.slingshot_network()),
        "efa",
        "gni",
        "mlx",
        "mrail",
        "opx",
        "psm",
        "psm2",
        "psm3",
        "rxm",
        "rxd",
        "shm",
        "sockets",
        "tcp",
        "ucx",
        "udp",
        "usnic",
        "verbs",
        "xpmem",
    )

    # CXI is a closed source package and only exists when an external.
    conflicts("fabrics=cxi")

    variant(
        "fabrics",
        default="sockets,tcp,udp",
        description="A list of enabled fabrics",
        values=fabrics,
        multi=True,
    )

    # NOTE: the 'kdreg' variant enables use of the special /dev/kdreg file to
    #   assist in memory registration caching in the GNI provider.  This
    #   device file can only be opened once per process, however, and thus it
    #   frequently conflicts with MPI.
    variant("kdreg", default=False, description="Enable kdreg on supported Cray platforms")

    variant("debug", default=False, description="Enable debugging")

    variant("uring", default=False, when="@1.17.0:", description="Enable uring support")

    # For version 1.9.0:
    # headers: fix forward-declaration of enum fi_collective_op with C++
    patch(
        "https://github.com/ofiwg/libfabric/commit/2e95b0efd85fa8a3d814128e34ec57ffd357460e.patch?full_index=1",
        sha256="456693e28bb1fc41a0bbb94b97ae054e7d28f81ca94795d7f294243da58c6376",
        when="@1.9.0",
    )

    # Fix for the inline assembly problem for the Nvidia compilers
    # https://github.com/ofiwg/libfabric/pull/7665
    patch("nvhpc-symver.patch", when="@1.6.0:1.14.0 %nvhpc")

    depends_on("rdma-core", when="fabrics=verbs")
    depends_on("rdma-core", when="@1.10.0: fabrics=efa")
    depends_on("opa-psm2", when="fabrics=psm2")
    depends_on("psm", when="fabrics=psm")
    depends_on("ucx", when="fabrics=mlx")
    depends_on("ucx", when="@1.18.0: fabrics=ucx")
    depends_on("uuid", when="fabrics=opx")
    depends_on("numactl", when="fabrics=opx")
    depends_on("liburing@2.1:", when="+uring")

    depends_on("m4", when="@main", type="build")
    depends_on("autoconf", when="@main", type="build")
    depends_on("automake", when="@main", type="build")
    depends_on("libtool", when="@main", type="build")

    conflicts("@1.9.0", when="platform=darwin", msg="This distribution is missing critical files")
    conflicts("fabrics=opx", when="@:1.14.99")
    conflicts(
        "fabrics=opx",
        when="@1.20.0",
        msg="Libfabric 1.20.0 uses values in memory that are not correctly "
        "set by OPX, resulting in undefined behavior.",
    )

    flag_handler = build_system_flags

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"libfabric: (\d+\.\d+\.\d+)(\D*\S*)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        results = []
        for exe in exes:
            variants = []
            output = Executable(exe)("--list", output=str, error=os.devnull)
            # fabrics
            fabrics = get_options_from_variant(cls, "fabrics")
            used_fabrics = []
            for fabric in fabrics:
                match = re.search(r"^%s:.*\n.*version: (\S+)" % fabric, output, re.MULTILINE)
                if match:
                    used_fabrics.append(fabric)
            if used_fabrics:
                variants.append("fabrics=" + ",".join(used_fabrics))
            results.append(" ".join(variants))
        return results

    def setup_build_environment(self, env):
        if self.run_tests:
            env.prepend_path("PATH", self.prefix.bin)

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_run_environment(self, env):
        libfabric_home = self.spec["libfabric"].prefix
        env.prepend_path("LD_LIBRARY_PATH", libfabric_home.lib)
        env.prepend_path("LD_LIBRARY_PATH", libfabric_home.lib64)

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_dependent_run_environment(self, env, dependent_spec):
        libfabric_home = self.spec["libfabric"].prefix
        env.prepend_path("LD_LIBRARY_PATH", libfabric_home.lib)
        env.prepend_path("LD_LIBRARY_PATH", libfabric_home.lib64)

    @when("@main")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        args = []

        args.extend(self.enable_or_disable("debug"))

        if self.spec.satisfies("+kdreg"):
            args.append("--with-kdreg=yes")
        else:
            args.append("--with-kdreg=no")

        if self.spec.satisfies("+uring"):
            args.append("--with-uring=yes")

        for fabric in [f if isinstance(f, str) else f[0].value for f in self.fabrics]:
            if "fabrics=" + fabric in self.spec:
                args.append("--enable-{0}=yes".format(fabric))
            else:
                args.append("--enable-{0}=no".format(fabric))

        if self.spec.satisfies("+cuda"):
            args.append(f"--with-cuda={self.spec['cuda'].prefix}")

        return args

    def installcheck(self):
        fi_info = Executable(self.prefix.bin.fi_info)
        fi_info()


# This code gets all the fabric names from the variants list
# Idea taken from the AutotoolsPackage source.
def get_options_from_variant(self, name):
    values = self.variants[name][0].values
    explicit_values = []
    if getattr(values, "feature_values", None):
        values = values.feature_values
    for value in sorted(values):
        if hasattr(value, "when"):
            if value.when is True:
                # Explicitly extract the True value for downstream use
                explicit_values.append("{0}".format(value))
        else:
            explicit_values.append(value)
    return explicit_values
