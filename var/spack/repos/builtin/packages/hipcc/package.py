# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.hooks.sbang import filter_shebang
from spack.package import *


class Hipcc(CMakePackage):
    """HIPCC: HIP compiler driver"""

    homepage = "https://github.com/ROCm/hipcc"
    git = "https://github.com/ROCm/hipcc.git"

    def url_for_version(self, version):
        if version <= Version("6.0.2"):
            url = "https://github.com/ROCm/HIPCC/archive/rocm-{0}.tar.gz"
        else:
            url = "https://github.com/ROCm/llvm-project/archive/rocm-{0}.tar.gz"
        return url.format(version)

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    license("MIT")
    version("6.2.1", sha256="4840f109d8f267c28597e936c869c358de56b8ad6c3ed4881387cf531846e5a7")
    version("6.2.0", sha256="12ce17dc920ec6dac0c5484159b3eec00276e4a5b301ab1250488db3b2852200")
    version("6.1.2", sha256="300e9d6a137dcd91b18d5809a316fddb615e0e7f982dc7ef1bb56876dff6e097")
    version("6.1.1", sha256="f1a67efb49f76a9b262e9735d3f75ad21e3bd6a05338c9b15c01e6c625c4460d")
    version("6.1.0", sha256="6bd9912441de6caf6b26d1323e1c899ecd14ff2431874a2f5883d3bc5212db34")
    version("6.0.2", sha256="d6209b14fccdd00d7231dec4b4f962aa23914b9dde389ba961370e8ba918bde5")
    version("6.0.0", sha256="e9cfaaecaf0e6ed363946439197f340c115e8e1189f96dbd716cf20245c29255")
    version("5.7.1", sha256="d47d27ef2b5de7f49cdfd8547832ac9b437a32e6fc6f0e9c1646f4b704c90aee")
    version("5.7.0", sha256="9f839bf7226e5e26f3150f8ba6eca507ab9a668e68b207736301b3bb9040c973")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("numactl")

    patch("0014-remove-compiler-rt-linkage-for-host.6.0.patch", when="@6.0")
    patch("0014-remove-compiler-rt-linkage-for-host.6.1.patch", when="@6.1")
    patch("0001-Update-the-ROCMINFO-HIPCLANG-PATHS-inside-hipcc-6.2.0.patch", when="@6.2:")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:6.0"):
            return "."
        else:
            return join_path("amd", "hipcc")

    def patch(self):
        numactl = self.spec["numactl"].prefix.lib
        if self.spec.satisfies("@:6.0"):
            with working_dir("bin"):
                filter_shebang("hipconfig")
        else:
            with working_dir("amd/hipcc/bin"):
                filter_shebang("hipconfig")

        if self.spec.satisfies("@:6.0"):
            with working_dir("src"):
                filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipBin_amd.h")
        else:
            with working_dir("amd/hipcc/src"):
                filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipBin_amd.h")
