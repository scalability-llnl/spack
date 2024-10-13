# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.hooks.sbang import filter_shebang
from spack.package import *
from spack.util.prefix import Prefix


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
    create portable applications for AMD and NVIDIA GPUs from
    single source code."""

    homepage = "https://github.com/ROCm/HIP"
    git = "https://github.com/ROCm/HIP.git"
    url = "https://github.com/ROCm/HIP/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libamdhip64"]

    license("MIT")

    version("master", branch="master")
    version("6.2.1", sha256="a8b86666a59867cae67409c4a45e0b8f29a6328c9739e6512c2b5612376f30cf")
    version("6.2.0", sha256="7ca261eba79793427674bf2372c92ac5483cc0fac5278f8ad611de396fad8bee")
    version("6.1.2", sha256="9ba5f70a553b48b2cea25c7e16b97ad49320750c0152763b173b63b9f151e783")
    version("6.1.1", sha256="09e8013b8071fca2cf914758001bbd1dccaa237e798e945970e4356cb9b90050")
    version("6.1.0", sha256="6fd57910a16d0b54df822807e67b6207146233a2de5a46c6a05b940a21e2c4d7")
    version("6.0.2", sha256="b47178db94f2acc106e1a88ceb029844805266ebaba11ef63744e90d224b11be")
    version("6.0.0", sha256="0d575788e0b731124a8489a36652014a165b9ebab92d5456ec3c976e062f3a82")
    version("5.7.1", sha256="eaa0e14a9ae45c58ed37863797b683a7778b3cbbf92f5b6529ec65fd61d61f3e")
    version("5.7.0", sha256="cb61234eec7879fb7e20937659ad535b93a6e66fc8de0a543da8b7702474f2fc")
    version("5.6.1", sha256="4b3c4dfcf8595da0e1b8c3e8067b1ccebeaac337762ff098db14375fa8dd4487")
    version("5.6.0", sha256="a8237768c1ae70029d972376f8d279f4de18a1e6106fff6215d1e16847bc375e")
    version("5.5.1", sha256="1f5f6bb72d8d64335ccc8242ef2e2ea8efeb380cce2997f475b1ee77528d9fb4")
    version("5.5.0", sha256="5b0d0253e62f85cc21d043513f7c11c64e4a4ec416159668f0b160d732d09a3c")
    with default_args(deprecated=True):
        version("5.4.3", sha256="23e51d3af517cd63019f8d199e46b84d5a18251d148e727f3985e8d99ccb0e58")
        version("5.4.0", sha256="e290f835d69ef23e8b5833a7e616b0a989ff89ada4412d9742430819546efc6c")
        version("5.3.3", sha256="51d4049dc37d261afb9e1270e60e112708ff06b470721ff21023e16e040e4403")
        version("5.3.0", sha256="05225832fb5a4d24f49a773ac27e315239943a6f24291a50d184e2913f2cdbe0")

    variant("rocm", default=True, description="Enable ROCm support")
    variant("cuda", default=False, description="Build with CUDA")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")
    conflicts("~rocm +asan", msg="ROCm must be enabled for asan")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("cuda", when="+cuda")

    depends_on("cmake@3.16.8:", type="build")
    depends_on("libedit", type="build")
    depends_on("perl@5.10:", type=("build", "run"))

    test_requires_compiler = True

    with when("+rocm"):
        depends_on("gl@4.5:")
        depends_on("py-cppheaderparser", type="build", when="@5.3.3:")
        depends_on("libx11", when="+asan")
        depends_on("xproto", when="+asan")
        for ver in [
            "5.3.0",
            "5.3.3",
            "5.4.0",
            "5.4.3",
            "5.5.0",
            "5.5.1",
            "5.6.0",
            "5.6.1",
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
            "6.1.2",
            "6.2.0",
            "6.2.1",
        ]:
            depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
            depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
            depends_on(f"comgr@{ver}", when=f"@{ver}")
            depends_on(f"llvm-amdgpu@{ver} +rocm-device-libs", when=f"@{ver}")
            depends_on(f"rocminfo@{ver}", when=f"@{ver}")
            depends_on(f"roctracer-dev-api@{ver}", when=f"@{ver}")

        for ver in [
            "5.4.0",
            "5.4.3",
            "5.5.0",
            "5.5.1",
            "5.6.0",
            "5.6.1",
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
            "6.1.2",
            "6.2.0",
            "6.2.1",
        ]:
            depends_on(f"hipify-clang@{ver}", when=f"@{ver}")

        for ver in [
            "5.5.0",
            "5.5.1",
            "5.6.0",
            "5.6.1",
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
            "6.1.2",
            "6.2.0",
            "6.2.1",
        ]:
            depends_on(f"rocm-core@{ver}", when=f"@{ver}")

        # hipcc likes to add `-lnuma` by default :(
        # ref https://github.com/ROCm/HIP/pull/2202
        depends_on("numactl", when="@3.7.0:")

    for ver in ["6.0.0", "6.0.2", "6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on(f"hipcc@{ver}", when=f"@{ver}")

    for ver in ["6.2.0", "6.2.1"]:
        depends_on(f"rocprofiler-register@{ver}", when=f"@{ver}")

    # roc-obj-ls requirements
    depends_on("perl-file-which")
    depends_on("perl-uri-encode")

    # Add hip-amd sources thru the below
    for d_version, d_shasum in [
        ("5.5.1", "9c8cb7611b3a496a0e9db92269143ee33b608eb69a8384957ace04e135ac90e9"),
        ("5.5.0", "bf87ed3919987c1a3a3f293418d26b65b3f02b97464e48f0cfcdd8f35763a0b7"),
        ("5.4.3", "475edce0f29c4ccd82e5ee21d4cce4836f2b1e3b13cbc891475e423d38a0ebb9"),
        ("5.4.0", "c4b79738eb6e669160382b6c47d738ac59bd493fc681ca400ff012a2e8212955"),
        ("5.3.3", "36acce92af39b0fa06002e164f5a7f5a9c7daa19bf96645361325775a325499d"),
        ("5.3.0", "81e9bd5209a7b400c986f9bf1d7079bcf7169bbcb06fc4fe843644559a4d612e"),
    ]:
        resource(
            name="hipamd",
            url=f"https://github.com/ROCm/hipamd/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipamd",
            when=f"@{d_version}",
        )
    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ("5.5.1", "a8a62a7c6fc5398406d2203b8cb75621a24944688e545d917033d87de2724498"),
        ("5.5.0", "0df9fa0b8aa0c8e6711d34eec0fdf1ed356adcd9625bc8f1ce9b3e72090f3e4f"),
        ("5.4.3", "b0f8339c844a2e62773bd85cd1e7c5ecddfe71d7c8e8d604e1a1d60900c30873"),
        ("5.4.0", "a294639478e76c75dac0e094b418f9bd309309b07faf6af126cdfad9aab3c5c7"),
        ("5.3.3", "cab394e6ef16c35bab8de29a66b96a7dc0e7d1297aaacba3718fa1d369233c9f"),
        ("5.3.0", "d251e2efe95dc12f536ce119b2587bed64bbda013969fa72be58062788044a9e"),
    ]:
        resource(
            name="opencl",
            url=f"https://github.com/ROCm/ROCm-OpenCL-Runtime/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="opencl",
            when=f"@{d_version}",
        )
    for d_version, d_shasum in [
        ("5.5.1", "1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e"),
        ("5.5.0", "efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1"),
        ("5.4.3", "71d9668619ab57ec8a4564d11860438c5aad5bd161a3e58fbc49555fbd59182d"),
        ("5.4.0", "46a1579310b3ab9dc8948d0fb5bed4c6b312f158ca76967af7ab69e328d43138"),
        ("5.3.3", "f8133a5934f9c53b253d324876d74f08a19e2f5b073bc94a62fe64b0d2183a18"),
        ("5.3.0", "2bf14116b5e2270928265f5d417b3d0f0f2e13cbc8ec5eb8c80d4d4a58ff7e94"),
    ]:
        resource(
            name="rocclr",
            url=f"https://github.com/ROCm/ROCclr/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="rocclr",
            when=f"@{d_version}",
        )
    # Add hip-clr sources thru the below
    for d_version, d_shasum in [
        ("6.2.1", "e9cff3a8663defdbda833d49c9e7160171eca14dc285ffe4061378607d6c890d"),
        ("6.2.0", "620e4c6a7f05651cc7a170bc4700fef8cae002420307a667c638b981d00b25e8"),
        ("6.1.2", "1a1e21640035d957991559723cd093f0c7e202874423667d2ba0c7662b01fea4"),
        ("6.1.1", "2db02f335c9d6fa69befcf7c56278e5cecfe3db0b457eaaa41206c2585ef8256"),
        ("6.1.0", "49b23eef621f4e8e528bb4de8478a17436f42053a2f7fde21ff221aa683205c7"),
        ("6.0.2", "cb8ac610c8d4041b74fb3129c084f1e7b817ce1a5a9943feca1fa7531dc7bdcc"),
        ("6.0.0", "798b55b5b5fb90dd19db54f136d8d8e1da9ae1e408d5b12b896101d635f97e50"),
        ("5.7.1", "c78490335233a11b4d8a5426ace7417c555f5e2325de10422df06c0f0f00f7eb"),
        ("5.7.0", "bc2447cb6fd86dff6a333b04e77ce85755104d9011a14a044af53caf02449573"),
        ("5.6.1", "0b88af1e99643899d11b1c8cf8a3c46601051b328a5e0ffbd44ee88b7eb0db33"),
        ("5.6.0", "8dcd99110737a294f67a805639cf372890c8ca16c7603caaa793e71e84478fe4"),
    ]:
        resource(
            name="clr",
            url=f"https://github.com/ROCm/clr/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="clr",
            when=f"@{d_version}",
        )

        # For avx build, the start address of values_ buffer in KernelParameters is not
        # correct as it is computed based on 16-byte alignment.
        patch(
            "https://github.com/ROCm/clr/commit/c4f773db0b4ccbbeed4e3d6c0f6bff299c2aa3f0.patch?full_index=1",
            sha256="5bb9b0e08888830ccf3a0a658529fe25f4ee62b5b8890f349bf2cc914236eb2f",
            working_dir="clr",
            when="@5.7:6.0",
        )
        patch(
            "https://github.com/ROCm/clr/commit/7868876db742fb4d44483892856a66d2993add03.patch?full_index=1",
            sha256="7668b2a710baf4cb063e6b00280fb75c4c3e0511575e8298a9c7ae5143f60b33",
            working_dir="clr",
            when="@5.7:6.0",
        )

    # Add hipcc sources thru the below
    for d_version, d_shasum in [
        ("5.7.1", "d47d27ef2b5de7f49cdfd8547832ac9b437a32e6fc6f0e9c1646f4b704c90aee"),
        ("5.7.0", "9f839bf7226e5e26f3150f8ba6eca507ab9a668e68b207736301b3bb9040c973"),
        ("5.6.1", "5800fac92b841ef6f52acda78d9bf86f83970bec0fb848a6265d239bdb7eb51a"),
        ("5.6.0", "fdb7fdc9e4648376120330f034ee8353038d34c8a015f9eb0c208c56eeddd097"),
    ]:
        resource(
            name="hipcc",
            url=f"https://github.com/ROCm/HIPCC/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipcc",
            when=f"@{d_version}",
        )
    # Add hipother sources thru the below
    for d_version, d_shasum in [
        ("6.2.1", "5d99e498c1fece44a421574282fc89c6a2499979eaa9f850e5caa7fa3a8938b8"),
        ("6.2.0", "1f854b0c07d71b10450080e3bbffe47adaf10a9745a9212797d991756a100174"),
        ("6.1.2", "2740d1e3dcf1f2d07d2a8db6acf4c972941ae392172b83fd8ddcfe8706a40d0b"),
        ("6.1.1", "8b975623c8ed1db53feea2cfd5d29f2a615e890aee1157d0d17adeb97200643f"),
        ("6.1.0", "43a48ccc82f705a15852392ee7419e648d913716bfc04063a53d2d17979b1b46"),
        ("6.0.2", "0bebb3774debcecc0b29a0cc5aa98e373a3ee7acf161503d0d9c9d0ecc8b8010"),
        ("6.0.0", "d3bf62cc17c3c44fea52b34bcbf725e7af1afc3542c2884cefcd41f65371f552"),
    ]:
        resource(
            name="hipother",
            url=f"https://github.com/ROCm/hipother/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipother",
            when=f"@{d_version} +cuda",
        )

    # Add hiptests sources thru the below
    for d_version, d_shasum in [
        ("6.2.1", "90fcf0169889533b882d289f9cb8a7baf9bd46a3ce36752b915083931dc839f1"),
        ("6.2.0", "314837dbac78be71844ceb959476470c484fdcd4fb622ff8de9277783e0fcf1c"),
        ("6.1.2", "5b14e4a30d8d8fb56c43e262009646ba9188eac1c8ff882d9a606a4bec69b56b"),
        ("6.1.1", "10c96ee72adf4580056292ab17cfd858a2fd7bc07abeb41c6780bd147b47f7af"),
        ("6.1.0", "cf3a6a7c43116032d933cc3bc88bfc4b17a4ee1513c978e751755ca11a5ed381"),
        ("6.0.2", "740ca064f4909c20d83226a63c2f164f7555783ec5f5f70be5bc23d3587ad829"),
        ("6.0.0", "e8f92a0f5d1f6093ca1fb24ff1b7140128900fcdc6e9f01f153d6907e5c2d807"),
        ("5.7.1", "28fbdf49f405adfee903bc0f05a43ac392c55b34c514c3582dfb7d6d67e79985"),
        ("5.7.0", "b1dae3cfc715e71dce92ac1da94265a9398944c76cee85ffab8f0c93665a48d6"),
        ("5.6.1", "5b3002ddfafda162329e4d9e6ac1200eeb48ff08e666b342aa8aeca30750f48b"),
        ("5.6.0", "8cf4509bf9c0747dab8ed8fec1365a9156792034b517207a0b2d63270429fd2e"),
    ]:
        resource(
            name="hip-tests",
            url=f"https://github.com/ROCm/hip-tests/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hip-tests",
            when=f"@{d_version}",
        )

    # Improve compilation without git repo and remove compiler rt linkage
    # for host and correction in CMake target path variable and
    # correcting the CMake path variable.
    patch("0013-remove-compiler-rt-linkage-for-host.5.3.0.patch", when="@5.3.0:5.4")
    patch("0014-hip-test-file-reorg-5.4.0.patch", when="@5.4.0:5.5")
    patch("0016-hip-sample-fix-hipMalloc-call.patch", when="@5.4.3:5.5")
    patch("0014-remove-compiler-rt-linkage-for-host.5.5.0.patch", when="@5.5")
    patch("0014-remove-compiler-rt-linkage-for-host.5.6.0.patch", when="@5.6.0:5.6")
    patch("0014-Remove-compiler-rt-linkage-for-host-for-5.7.0.patch", when="@5.7.0:5.7")
    patch("0014-remove-compiler-rt-linkage-for-host.6.0.patch", when="@6.0")
    patch("0014-remove-compiler-rt-linkage-for-host.6.1.patch", when="@6.1")
    patch("0015-reverting-operator-mixup-fix-for-slate.patch", when="@5.6:6.0")
    patch("0018-reverting-hipMemoryType-with-memoryType.patch", when="@6.0:")

    # See https://github.com/ROCm/HIP/pull/3206
    patch(
        "https://github.com/ROCm/HIP/commit/50ee82f6bc4aad10908ce09198c9f7ebfb2a3561.patch?full_index=1",
        sha256="c2ee21cdc55262c7c6ba65546b5ca5f65ea89730",
        when="@5.2:5.7",
    )

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@4.5:5.5"):
            return "hipamd"
        else:
            return "clr"

    def get_paths(self):
        if self.spec.external:
            # For external packages we only assume the `hip` prefix is known,
            # because spack does not set prefixes of dependencies of externals.
            hip_libs_at_top = os.path.basename(self.spec.prefix) != "hip"
            # We assume self.spec.prefix is  /opt/rocm-x.y.z for rocm-5.2.0 and newer
            # and /opt/rocm-x.y.z/hip for older versions
            # However, depending on how an external is found it can be at either level
            # of the installation path
            if self.spec.satisfies("@5.2.0:"):
                if hip_libs_at_top:
                    rocm_prefix = Prefix(self.spec.prefix)
                else:
                    rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))
            else:
                # We assume self.spec.prefix is /opt/rocm-x.y.z/hip and rocm has a
                # default installation with everything installed under
                # /opt/rocm-x.y.z
                # Note that since the key hip library can also exist at the top of the
                # /opt/rocm-x.y.z/lib tree, it is possible that the package is detected
                # without the correct prefix.  Work around it.
                if hip_libs_at_top:
                    rocm_prefix = Prefix(self.spec.prefix)
                else:
                    rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))

            if not os.path.isdir(rocm_prefix):
                msg = "Could not determine prefix for other rocm components\n"
                msg += "Either report a bug at github.com/spack/spack or "
                msg += "manually edit rocm_prefix in the package file as "
                msg += "a workaround."
                raise RuntimeError(msg)

            if hip_libs_at_top:
                hip_path = "{0}/hip".format(self.spec.prefix)
            else:
                hip_path = self.spec.prefix

            paths = {
                "hip-path": hip_path,
                "rocm-path": rocm_prefix,
                "llvm-amdgpu": rocm_prefix.llvm,
                "hsa-rocr-dev": rocm_prefix.hsa,
                "rocminfo": rocm_prefix,
                "comgr": rocm_prefix,
                "rocm-device-libs": rocm_prefix,
                "hipify-clang": rocm_prefix,
            }

            if self.spec.satisfies("@5.7:"):
                paths["hip-path"] = rocm_prefix
            if self.spec.satisfies("@6.0:"):
                paths["hsa-rocr-dev"] = rocm_prefix

        else:
            paths = {
                "hip-path": self.spec.prefix,
                "rocm-path": self.spec.prefix,
                "llvm-amdgpu": self.spec["llvm-amdgpu"].prefix,
                "hsa-rocr-dev": self.spec["hsa-rocr-dev"].prefix,
                "rocminfo": self.spec["rocminfo"].prefix,
                "comgr": self.spec["comgr"].prefix,
                "rocm-device-libs": self.spec["llvm-amdgpu"].prefix,
                "hipify-clang": self.spec["hipify-clang"].prefix,
            }
        paths["bitcode"] = paths["rocm-device-libs"].amdgcn.bitcode

        return paths

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def set_variables(self, env):
        if self.spec.satisfies("+rocm"):
            # Note: do not use self.spec[name] here, since not all dependencies
            # have defined prefixes when hip is marked as external.
            paths = self.get_paths()

            # Used in hipcc, but only useful when hip is external, since only then
            # there is a common prefix /opt/rocm-x.y.z.
            env.set("ROCM_PATH", paths["rocm-path"])
            if self.spec.satisfies("@5.4:"):
                env.set("HIPIFY_CLANG_PATH", paths["hipify-clang"])
            if self.spec.satisfies("@6.1:"):
                env.prepend_path("LD_LIBRARY_PATH", paths["hsa-rocr-dev"].lib)

            # hipcc recognizes HIP_PLATFORM == hcc and HIP_COMPILER == clang, even
            # though below we specified HIP_PLATFORM=rocclr and HIP_COMPILER=clang
            # in the CMake args.
            env.set("HIP_PLATFORM", "amd")

            env.set("HIP_COMPILER", "clang")

            # bin directory where clang++ resides
            env.set("HIP_CLANG_PATH", paths["llvm-amdgpu"].bin)

            # Path to hsa-rocr-dev prefix used by hipcc.
            env.set("HSA_PATH", paths["hsa-rocr-dev"])

            # This is a variable that does not exist in hipcc but was introduced
            # in a patch of ours since 3.5.0 to locate rocm_agent_enumerator:
            # https://github.com/ROCm/HIP/pull/2138
            env.set("ROCMINFO_PATH", paths["rocminfo"])

            # This one is used in hipcc to run `clang --hip-device-lib-path=...`
            env.set("DEVICE_LIB_PATH", paths["bitcode"])

            # And this is used in clang whenever the --hip-device-lib-path is not
            # used (e.g. when clang is invoked directly)
            env.set("HIP_DEVICE_LIB_PATH", paths["bitcode"])

            # Just the prefix of hip (used in hipcc)
            # Deprecated in 5.1.0 and breaks hipcc in 5.5.1+
            if self.spec.satisfies("@:5.4"):
                env.set("HIP_PATH", paths["hip-path"])

            # Used in comgr and seems necessary when using the JIT compiler, e.g.
            # hiprtcCreateProgram:
            # https://github.com/ROCm/ROCm-CompilerSupport/blob/rocm-4.0.0/lib/comgr/src/comgr-env.cpp
            env.set("LLVM_PATH", paths["llvm-amdgpu"])
            env.set("COMGR_PATH", paths["comgr"])

            # Finally we have to set --rocm-path=<prefix> ourselves, which is not
            # the same as --hip-device-lib-path (set by hipcc). It's used to set
            # default bin, include and lib folders in clang. If it's not set it is
            # infered from the clang install dir (and they try to find
            # /opt/rocm again...). If this path is set, there is no strict checking
            # and parsing of the <prefix>/bin/.hipVersion file. Let's just set this
            # to the hip prefix directory for non-external builds so that the
            # bin/.hipVersion file can still be parsed.
            # See also https://github.com/ROCm/HIP/issues/2223
            env.append_path(
                "HIPCC_COMPILE_FLAGS_APPEND",
                "--rocm-path={0}".format(paths["rocm-path"]),
                separator=" ",
            )
        elif self.spec.satisfies("+cuda"):
            env.set("CUDA_PATH", self.spec["cuda"].prefix)
            env.set("HIP_PATH", self.spec.prefix)
            env.set("HIP_PLATFORM", "nvidia")

        # Set up hipcc/hip-clang to use the specific GCC toolchain that is
        # being used to compile. This is only important for external ROCm
        # installations, which may otherwise pick up the wrong GCC toolchain.
        if self.spec.external and self.spec.satisfies("%gcc"):
            # This is picked up by hipcc.
            env.append_path(
                "HIPCC_COMPILE_FLAGS_APPEND",
                f"--gcc-toolchain={self.compiler.prefix}",
                separator=" ",
            )
            # This is picked up by CMake when using HIP as a CMake language.
            env.append_path("HIPFLAGS", f"--gcc-toolchain={self.compiler.prefix}", separator=" ")

    def setup_build_environment(self, env):
        self.set_variables(env)

    def setup_run_environment(self, env):
        self.set_variables(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.set_variables(env)

        if "amdgpu_target" in dependent_spec.variants:
            arch = dependent_spec.variants["amdgpu_target"]
            if "none" not in arch and "auto" not in arch:
                env.set("HCC_AMDGPU_TARGET", ",".join(arch.value))

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_dependent_build_environment(env, dependent_spec)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, "hipcc")

    def patch(self):
        if self.spec.satisfies("@5.2:5.4 +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "hipamd/hip-config.cmake.in",
                string=True,
            )
        if self.spec.satisfies("@5.6.0:5.6 +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/hip-config.cmake.in",
                string=True,
            )
        if self.spec.satisfies("@5.7: +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/hip-config-amd.cmake",
                string=True,
            )
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/src/hiprtc/CMakeLists.txt",
                string=True,
            )
        perl = self.spec["perl"].command

        if self.spec.satisfies("@:5.5"):
            with working_dir("bin"):
                filter_shebang("hipconfig")
            with working_dir("hipamd/bin"):
                filter_file("^#!/usr/bin/perl", f"#!{perl}", "roc-obj-extract", "roc-obj-ls")
        if self.spec.satisfies("@5.6:"):
            with working_dir("clr/hipamd/bin"):
                filter_file("^#!/usr/bin/perl", f"#!{perl}", "roc-obj-extract", "roc-obj-ls")
        if self.spec.satisfies("@5.6:5.7"):
            with working_dir("hipcc/bin"):
                filter_shebang("hipconfig")

        if self.spec.satisfies("+rocm"):
            numactl = self.spec["numactl"].prefix.lib
            if self.spec.satisfies("@:5.5"):
                with working_dir("bin"):
                    filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipcc")
            elif self.spec.satisfies("@5.6:5.7"):
                with working_dir("hipcc/src"):
                    filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipBin_amd.h")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+rocm"):
            args.append(self.define("HSA_PATH", self.spec["hsa-rocr-dev"].prefix))
            args.append(self.define("HIP_COMPILER", "clang"))
            args.append(
                self.define(
                    "PROF_API_HEADER_PATH",
                    self.spec["roctracer-dev-api"].prefix.roctracer.include.ext,
                )
            )
            args.append(self.define("HIP_RUNTIME", "rocclr"))
            args.append(self.define("HIP_PLATFORM", "amd"))
            if self.spec.satisfies("@5.6.0:"):
                args.append(self.define("HIP_LLVM_ROOT", self.spec["llvm-amdgpu"].prefix))
            if self.spec.satisfies("@6.1.0:") and self.spec.satisfies("+asan"):
                args.append(self.define("ADDRESS_SANITIZER", "ON"))
                args.append(
                    self.define("CMAKE_C_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
                )
                args.append(
                    self.define(
                        "CMAKE_CXX_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++"
                    )
                )
                args.append(
                    self.define(
                        "CMAKE_CXX_FLAGS",
                        f"-I{self.spec['libx11'].prefix.include} "
                        f"-I{self.spec['mesa'].prefix.include} "
                        f"-I{self.spec['xproto'].prefix.include}",
                    )
                )

        if self.spec.satisfies("+cuda"):
            args.append(self.define("HIP_PLATFORM", "nvidia"))
            args.append(self.define("HIPNV_DIR", self.stage.source_path + "/hipother/hipnv"))

        args.append(self.define("HIP_COMMON_DIR", self.stage.source_path))
        args.append(self.define("HIP_CATCH_TEST", "OFF"))
        if self.spec.satisfies("@:5.5"):
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path + "opencl"))
        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if self.spec.satisfies("@5.6.0:"):
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "/clr/rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path + "/clr/opencl"))
            args.append(self.define("CLR_BUILD_HIP", True)),
            args.append(self.define("CLR_BUILD_OCL", False)),
        if self.spec.satisfies("@5.6:5.7"):
            args.append(self.define("HIPCC_BIN_DIR", self.stage.source_path + "/hipcc/bin")),
        if self.spec.satisfies("@6.0:"):
            args.append(self.define("HIPCC_BIN_DIR", self.spec["hipcc"].prefix.bin)),
        return args

    test_src_dir_old = "samples"
    test_src_dir = "hip-tests/samples"

    @run_after("install")
    def install_samples(self):
        if self.spec.satisfies("@5.6.0:"):
            install_tree(self.test_src_dir, self.spec.prefix.share.samples)

    @run_after("install")
    def cache_test_sources(self):
        """Copy the tests source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        if self.spec.satisfies("@5.1:5.5"):
            cache_extra_test_sources(self, [self.test_src_dir_old])
        elif self.spec.satisfies("@5.6:"):
            cache_extra_test_sources(self, [self.test_src_dir])

    def test_samples(self):
        """build and run all hip samples"""
        if self.spec.satisfies("@5.1:5.5"):
            test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir_old)
        elif self.spec.satisfies("@5.6:"):
            test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        prefixes = ";".join(
            [
                self.spec["hip"].prefix,
                self.spec["llvm-amdgpu"].prefix,
                self.spec["comgr"].prefix,
                self.spec["hsa-rocr-dev"].prefix,
            ]
        )
        cc_options = ["-DCMAKE_PREFIX_PATH=" + prefixes, ".."]

        amdclang_path = join_path(self.spec["llvm-amdgpu"].prefix, "bin", "amdclang++")
        os.environ["CXX"] = amdclang_path
        os.environ["FC"] = "/usr/bin/gfortran"

        cmake = which(self.spec["cmake"].prefix.bin.cmake)

        for root, dirs, files in os.walk(test_dir):
            dirs.sort()
            if "CMakeLists.txt" in files or "Makefile" in files:
                with working_dir(root, create=True):
                    head, test_name = os.path.split(root)
                    with test_part(
                        self,
                        "test_sample_{0}".format(test_name),
                        purpose="configure, build and run test: {0}".format(test_name),
                    ):
                        if "CMakeLists.txt" in files:
                            print("Configuring  test " + test_name)
                            os.mkdir("build")
                            os.chdir("build")
                            cmake(*cc_options)

                        print("Building test " + test_name)
                        make(parallel=False)
                        # iterate through the files in dir to find the newly built binary
                        for file in os.listdir("."):
                            if (
                                file not in files
                                and os.path.isfile(file)
                                and os.access(file, os.X_OK)
                                and not file.endswith(".o")
                            ):
                                print("Executing test binary: " + file)
                                exe = which(file)
                                if file == "hipDispatchEnqueueRateMT":
                                    options = ["16", "0"]
                                else:
                                    options = []
                                exe(*options)
