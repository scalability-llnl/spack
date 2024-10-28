# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *

tools_url = "https://github.com/ROCm"
compute_url = "https://github.com/ROCm"

# Arrays of hashes are in order of the versions array below
# For example array[0] = 3.9.0, array[1] = 3.10.0, etc.

aomp = [
    "371ed037b95b83fac64fb2ff2fc17313fe7d3befc8671f0a08f0e2072393fa5b",
    "c86141fcde879fc78d06a41ba6a26ff528da539c6a1be8b714f635182c66e3f4",
    "bbca540897848fa95fd0f14fc05ab6deda31299a061424972d5e2bc09c7543dc",
    "7f90634fb621169b21bcbd920c2e299acc88ba0eeb1a33fd40ae26e13201b652",
    "23cc7d1c82e35c74f48285a0a1c27e7b3cae1767568bb7b9367ea21f53dd6598",
    "9ec03a69cc462ada43e1fd4ca905a765b08c10e0911fb7a202c893cc577855e6",
    "0673820a81986c9e2f28f15bbb45ad18934bca56a9d08aae6c49ec3895b38487",
    "6c051bf7625f682ba3d2ea80b46a38ca2cbcd20f5d89ae3433602d3e7ef0403a",
    "4f34fa02db410808c5e629f30f8804210b42c4ff7d31aa80606deaed43054c3c",
    "ed7bbf92230b6535a353ed032a39a9f16e9987397798100392fc25e40c8a1a4e",
    "1b2c0934ef16e17b2377944fae8c9b3db6dc64b7e43932ddfe2eeefdf6821410",
    "d6e13a15d5d25990d4bacbac8fabe2eb07973829f2e69abbc628e0736f95caf9",
    "832b7c48149a730619b577a2863b8d1bf1b2551eda5b815e1865a044929ab9fa",
    "62a5036a2299ed2e3053ee00b7ea1800469cd545fea486fa17266a8b3acfaf5d",
    "3de1c7a31a88c3f05a6a66ba6854ac8fdad1ce44462e561cb1e6ad59629029ce",
    "5f54d7c7c798bcf1cd47d3a7f17ceaf79991bf166cc5e47e5372a68e7cf7d520",
    "ac82e8da0c210ee14b911c833ae09a029a41541689930759737c135db52464a3",
]

devlib = [
    "f7e1665a1650d3d0481bec68252e8a5e68adc2c867c63c570f6190a1d2fe735c",
    "963c9a0561111788b55a8c3b492e2a5737047914752376226c97a28122a4d768",
    "d68813ded47179c39914c8d1b76af3dad8c714b10229d1e2246af67609473951",
    "f4f7281f2cea6d268fcc3662b37410957d4f0bc23e0df9f60b12eb0fcdf9e26e",
    "5ab95aeb9c8bed0514f96f7847e21e165ed901ed826cdc9382c14d199cbadbd3",
    "3b5f6dd85f0e3371f6078da7b59bf77d5b210e30f1cc66ef1e2de6bbcb775833",
    "efb5dcdca9b3a9fbe408d494fb4a23e0b78417eb5fa8eebd4a5d226088f28921",
    "f0dfab272ff936225bfa1e9dabeb3c5d12ce08b812bf53ffbddd2ddfac49761c",
    "0f8780b9098573f1c456bdc84358de924dcf00604330770a383983e1775bf61e",
    "703de8403c0bd0d80f37c970a698f10f148daf144d34f982e4484d04f7c7bbef",
    "198df4550d4560537ba60ac7af9bde31d59779c8ec5d6309627f77a43ab6ef6f",
    "c6d88b9b46e39d5d21bd5a0c1eba887ec473a370b1ed0cebd1d2e910eedc5837",
    "6bd9912441de6caf6b26d1323e1c899ecd14ff2431874a2f5883d3bc5212db34",
    "f1a67efb49f76a9b262e9735d3f75ad21e3bd6a05338c9b15c01e6c625c4460d",
    "300e9d6a137dcd91b18d5809a316fddb615e0e7f982dc7ef1bb56876dff6e097",
    "12ce17dc920ec6dac0c5484159b3eec00276e4a5b301ab1250488db3b2852200",
    "4840f109d8f267c28597e936c869c358de56b8ad6c3ed4881387cf531846e5a7",
]

llvm = [
    "4e3fcddb5b8ea8dcaa4417e0e31a9c2bbdc9e7d4ac3401635a636df32905c93e",
    "5296d5e474811c7d1e456cb6d5011db248b79b8d0512155e8a6c2aa5b5f12d38",
    "ff54f45a17723892cd775c1eaff9e5860527fcfd33d98759223c70e3362335bf",
    "a844d3cc01613f6284a75d44db67c495ac1e9b600eacbb1eb13d2649f5d5404d",
    "5dc6c99f612b69ff73145bee17524e3712990100e16445b71634106acf7927cf",
    "7d7181f20f89cb0715191aa32914186c67a34258c13457055570d47e15296553",
    "e922bd492b54d99e56ed88c81e2009ed6472059a180b10cc56ce1f9bd2d7b6ed",
    "045e43c0c4a3f4f2f1db9fb603a4f1ea3d56e128147e19ba17909eb57d7f08e5",
    "4abdf00b297a77c5886cedb37e63acda2ba11cb9f4c0a64e133b05800aadfcf0",
    "6b54c422e45ad19c9bf5ab090ec21753e7f7d854ca78132c30eb146657b168eb",
    "c673708d413d60ca8606ee75c77e9871b6953c59029c987b92f2f6e85f683626",
    "7d35acc84de1adee65406f92a369a30364703f84279241c444cd93a48c7eeb76",
    "6bd9912441de6caf6b26d1323e1c899ecd14ff2431874a2f5883d3bc5212db34",
    "f1a67efb49f76a9b262e9735d3f75ad21e3bd6a05338c9b15c01e6c625c4460d",
    "300e9d6a137dcd91b18d5809a316fddb615e0e7f982dc7ef1bb56876dff6e097",
    "12ce17dc920ec6dac0c5484159b3eec00276e4a5b301ab1250488db3b2852200",
    "4840f109d8f267c28597e936c869c358de56b8ad6c3ed4881387cf531846e5a7",
]

flang = [
    "ef1256ddf6cd9de10a1b88df4736dce48295136983a7e31eadd942fb39b156f7",
    "ddccd866d0c01086087fe21b5711668f85bcf9cbd9f62853f8bda32eaedb5339",
    "fae8195a5e1b3778e31dbc6cbeedeae9998ea4b5a54215534af41e91fdcb8ba0",
    "b283d76244d19ab16c9d087ee7de0d340036e9c842007aa9d288aa4e6bf3749f",
    "a18522588686672150c7862f2b23048a429baa4a66010c4196e969cc77bd152c",
    "7c3b4eb3e95b9e2f91234f202a76034628d230a92e57b7c5ee9dcca1097bec46",
    "fcefebddca0b373da81ff84f0f5469a1ef77a05430a5195d0f2e6399d3af31c3",
    "5ebcbca2e03bd0686e677f44ea551e97bd9395c6b119f832fa784818733aa652",
    "cc4f1973b1b8e7bcc4f09e3381bae4e1a2e51ea4e2598fc1b520ccb8bf24d28c",
    "8fd618d81af092416b267c4d00c801731f7a00c0f8d4aedb795e52a4ec1bf183",
    "fcb319ddb2aa3004a6ae60370ab4425f529336b1cee50f29200e697e61b53586",
    "8e6469415880bb068d788596b3ed713a24495eb42788f98cca92e73a2998f703",
    "51ecd2c154568c971f5b46ff0e1e1b57063afe28d128fc88c503de88f7240267",
    "1bcaa73e73a688cb092f01987cf3ec9ace4aa1fcaab2b812888c610722c4501d",
    "12418ea61cca58811b7e75fd9df48be568b406f84a489a41ba5a1fd70c47f7ba",
    "6af7785b1776aeb9229ce4e5083dcfd451e8450f6e5ebe34214560b13f679d96",
    "409ee98bf15e51ac68b7ed351f4582930dfa0288de042006e17eea6b64df5ad6",
]

extras = [
    "b3beee383d9c130666c230595c950bdc2ce4c7a99d728b9ddf1bca3963152223",
    "b26b9f4b11a9ccfab53d0dd55aada7e5b98f7ab51981cb033b376321dd44bf87",
    "2546becd4b182d1e366f47660c731c8ff7366b6306782f04706b6a7bf4e2094c",
    "d393f27a85c9229433b50daee8154e11517160beb1049c1de9c55fc31dd11fac",
    "8f49026a80eb8685cbfb6d3d3b9898dd083df4d71893984ae5330d4804c685fb",
    "8955aa9d039fd6c1ff2e26d7298f0bf09bbcf03f09c6df92c91a9ab2510df9da",
    "017bfed52fbe08185d8dbde79377918454215683562519a9e47acf403d9a1c29",
    "437e2017cfe2ab73b15ada0fc1ea88f794f0b108cc5410f457268ae7e4e8985a",
    "be59433dd85d4b8f0eaff87e0cc424a814152c67f3a682d1343c4bd61dd49a0f",
    "8060c6879708faf5f7d417b19a479dec9b7b9583a1b885f12d247faf831f7f0b",
    "f37e1107e4da5b083e794244f3d0c9fd073ccb6fd6015e635349d8f0d679c4b8",
    "b2e117d703cefdc2858adaeee5bad95e9b6dab6263a9c13891a79a7b1e2defb6",
    "57d6d9d26c0cb6ea7f8373996c41165f463ae7936d32e5793822cfae03900f8f",
    "3dc837fbfcac64e000e1b5518e4f8a6b260eaf1a3e74152d8b8c22f128f575b7",
    "2b9351fdb1cba229669233919464ae906ca8f70910c6fa508a2812b7c3bed123",
    "7cef51c980f29d8b46d8d4b110e4f2f75d93544cf7d63c5e5d158cf531aeec7d",
    "4b0d250b5ebd997ed6d5d057689c3f67dfb4d82f09f582ebb439ca9134fae48d",
]

versions = [
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
]
versions_dict = dict()  # type: Dict[str,Dict[str,str]]
components = ["aomp", "devlib", "llvm", "flang", "extras"]
component_hashes = [aomp, devlib, llvm, flang, extras]

# Loop through versions and create necessary dictionaries of components
for outer_index, item in enumerate(versions):
    for inner_index, component in enumerate(component_hashes):
        versions_dict.setdefault(item, {})[components[inner_index]] = component_hashes[
            inner_index
        ][outer_index]


class RocmOpenmpExtras(Package):
    """OpenMP support for ROCm LLVM."""

    homepage = tools_url + "/aomp"
    url = tools_url + "/aomp/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    license("Apache-2.0")

    maintainers("srekolam", "renjithravindrankannath", "estewart08")
    version("6.2.1", sha256=versions_dict["6.2.1"]["aomp"])
    version("6.2.0", sha256=versions_dict["6.2.0"]["aomp"])
    version("6.1.2", sha256=versions_dict["6.1.2"]["aomp"])
    version("6.1.1", sha256=versions_dict["6.1.1"]["aomp"])
    version("6.1.0", sha256=versions_dict["6.1.0"]["aomp"])
    version("6.0.2", sha256=versions_dict["6.0.2"]["aomp"])
    version("6.0.0", sha256=versions_dict["6.0.0"]["aomp"])
    version("5.7.1", sha256=versions_dict["5.7.1"]["aomp"])
    version("5.7.0", sha256=versions_dict["5.7.0"]["aomp"])
    version("5.6.1", sha256=versions_dict["5.6.1"]["aomp"])
    version("5.6.0", sha256=versions_dict["5.6.0"]["aomp"])
    version("5.5.1", sha256=versions_dict["5.5.1"]["aomp"])
    version("5.5.0", sha256=versions_dict["5.5.0"]["aomp"])
    version("5.4.3", sha256=versions_dict["5.4.3"]["aomp"], deprecated=True)
    version("5.4.0", sha256=versions_dict["5.4.0"]["aomp"], deprecated=True)
    version("5.3.3", sha256=versions_dict["5.3.3"]["aomp"], deprecated=True)
    version("5.3.0", sha256=versions_dict["5.3.0"]["aomp"], deprecated=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("python@3:", type="build")
    depends_on("perl-data-dumper", type="build")
    depends_on("awk", type="build")
    depends_on("elfutils", type=("build", "link"))
    depends_on("libffi", type=("build", "link"))
    depends_on("libdrm", when="@5.7:6.0")
    depends_on("numactl", when="@5.7:6.0")

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
    ]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

        resource(
            name="rocm-device-libs",
            url=f"{compute_url}/ROCm-Device-Libs/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["devlib"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="rocm-device-libs",
            when=f"@{ver}",
        )
        resource(
            name="flang",
            url=f"{tools_url}/flang/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["flang"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="flang",
            when=f"@{ver}",
        )

        resource(
            name="aomp-extras",
            url=f"{tools_url}/aomp-extras/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["extras"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="aomp-extras",
            when=f"@{ver}",
        )

        resource(
            name="llvm-project",
            url=f"{compute_url}/llvm-project/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["llvm"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="llvm-project",
            when=f"@{ver}",
        )
    for ver in ["6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

        resource(
            name="flang",
            url=f"{tools_url}/flang/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["flang"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="flang",
            when=f"@{ver}",
        )

        resource(
            name="aomp-extras",
            url=f"{tools_url}/aomp-extras/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["extras"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="aomp-extras",
            when=f"@{ver}",
        )

        resource(
            name="llvm-project",
            url=f"{compute_url}/llvm-project/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["llvm"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="llvm-project",
            when=f"@{ver}",
        )
    patch("0001-Linking-hsakmt-libdrm-and-numactl-libraries.patch", when="@5.7:6.0")
    patch(
        "0001-Linking-hsakmt-libdrm-and-numactl-libraries-6.1.patch",
        working_dir="rocm-openmp-extras/llvm-project/openmp/libomptarget",
        when="@6.1",
    )
    patch("0001-Avoid-duplicate-registration-on-cuda-env.patch", when="@6.1")
    patch("0001-Avoid-duplicate-registration-on-cuda-env-6.2.patch", when="@6.2")

    def setup_run_environment(self, env):
        devlibs_prefix = self.spec["llvm-amdgpu"].prefix
        openmp_extras_prefix = self.spec["rocm-openmp-extras"].prefix
        llvm_prefix = self.spec["llvm-amdgpu"].prefix
        hsa_prefix = self.spec["hsa-rocr-dev"].prefix
        env.set("AOMP", "{0}".format(llvm_prefix))
        env.set("HIP_DEVICE_LIB_PATH", "{0}/amdgcn/bitcode".format(devlibs_prefix))
        env.prepend_path("CPATH", "{0}/include".format(openmp_extras_prefix))
        env.prepend_path("LIBRARY_PATH", "{0}/lib".format(openmp_extras_prefix))
        if self.spec.satisfies("@5.3.0:"):
            env.prepend_path("LD_LIBRARY_PATH", "{0}/lib".format(openmp_extras_prefix))
            env.prepend_path("LD_LIBRARY_PATH", "{0}/lib".format(hsa_prefix))
        env.set("AOMP_GPU", "`{0}/bin/mygpu`".format(openmp_extras_prefix))

    def setup_build_environment(self, env):
        openmp_extras_prefix = self.spec["rocm-openmp-extras"].prefix
        llvm_prefix = self.spec["llvm-amdgpu"].prefix
        env.set("AOMP", "{0}".format(llvm_prefix))
        env.set("FC", "{0}/bin/flang".format(openmp_extras_prefix))
        if self.spec.satisfies("@6.1:"):
            env.prepend_path("LD_LIBRARY_PATH", self.spec["hsa-rocr-dev"].prefix.lib)
        if self.spec.satisfies("+asan"):
            env.set("SANITIZER", 1)
            env.set("VERBOSE", 1)
            env.set(
                "LDSHARED",
                self.spec["llvm-amdgpu"].prefix.bin.clang
                + " -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2",
            )
        gfx_list = "gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908"

        if self.spec.version >= Version("4.3.1"):
            gfx_list = gfx_list + " gfx90a gfx1030 gfx1031"
        env.set("GFXLIST", gfx_list)

    def patch(self):
        src = self.stage.source_path
        libomptarget = "{0}/rocm-openmp-extras/llvm-project/openmp/libomptarget"
        flang = "{0}/rocm-openmp-extras/flang/"

        plugin = "/plugins/amdgpu/CMakeLists.txt"

        if self.spec.version < Version("5.2.0"):
            filter_file(
                "{ROCM_DIR}/amdgcn/bitcode",
                "{DEVICE_LIBS_DIR}",
                aomp_extras.format(src) + "/aompextras/CMakeLists.txt",
                libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
            )
        if self.spec.satisfies("@6.1"):
            filter_file(
                r"${HSAKMT_LIB_PATH}",
                "${HSAKMT_LIB_PATH} ${HSAKMT_LIB64}"
                + "${HSAKMT_LIB} ${LIBDRM_LIB} ${NUMACTL_DIR}/lib",
                libomptarget.format(src) + "/CMakeLists.txt",
            )
            filter_file(
                r"${LIBOMPTARGET_LLVM_INCLUDE_DIRS}",
                "${LIBOMPTARGET_LLVM_INCLUDE_DIRS} ${HSAKMT_INC_PATH}",
                libomptarget.format(src) + "/../CMakeLists.txt",
            )
            filter_file(
                r"${LIBOMPTARGET_LLVM_INCLUDE_DIRS}",
                "${LIBOMPTARGET_LLVM_INCLUDE_DIRS} ${HSAKMT_INC_PATH}",
                libomptarget.format(src) + "/CMakeLists.txt",
            )

        # Openmp adjustments
        # Fix relocation error with libffi by not using static lib.
        filter_file(
            "libffi.a",
            "",
            libomptarget.format(src) + "/cmake/Modules/LibomptargetGetDependencies.cmake",
        )
        if self.spec.satisfies("@:6.1"):
            filter_file(
                r"{OPENMP_INSTALL_LIBDIR}",
                "{OPENMP_INSTALL_LIBDIR}/libdevice",
                libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
            )
            filter_file(
                "-nogpulib",
                "-nogpulib -nogpuinc",
                libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
            )
            filter_file(
                "-x hip",
                "-x hip -nogpulib -nogpuinc",
                libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
            )
            filter_file(
                "-c ",
                "-c -nogpulib -nogpuinc -I{LIMIT}",
                libomptarget.format(src) + "/hostrpc/CMakeLists.txt",
            )
            filter_file(
                r"${ROCM_DIR}/hsa/include ${ROCM_DIR}/hsa/include/hsa",
                "${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa",
                libomptarget.format(src) + plugin,
                string=True,
            )

            filter_file("{ROCM_DIR}/hsa/lib", "{HSA_LIB}", libomptarget.format(src) + plugin)

            filter_file(
                r"{ROCM_DIR}/lib\)",
                "{HSAKMT_LIB})\nset(HSAKMT_LIB64 ${HSAKMT_LIB64})",
                libomptarget.format(src) + plugin,
            )

            filter_file(
                r"-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}",
                "-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS} -L${HSAKMT_LIB64}",
                libomptarget.format(src) + plugin,
                string=True,
            )

            filter_file(
                r"-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}",
                "-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}" + ",-rpath,${HSAKMT_LIB64}",
                libomptarget.format(src) + plugin,
                string=True,
            )

            filter_file("{ROCM_DIR}/include", "{COMGR_INCLUDE}", libomptarget.format(src) + plugin)

            filter_file(
                r"-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}",
                "-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}",
                libomptarget.format(src) + plugin,
                string=True,
            )

            filter_file(
                r"rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}",
                "rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}" + "-Wl,-rpath,${COMGR_LIB}",
                libomptarget.format(src) + plugin,
                string=True,
            )

        filter_file(
            "ADDITIONAL_VERSIONS 2.7",
            "ADDITIONAL_VERSIONS 3",
            flang.format(src) + "CMakeLists.txt",
        )

        filter_file(
            "if (LIBOMPTARGET_DEP_CUDA_FOUND)",
            "if (LIBOMPTARGET_DEP_CUDA_FOUND AND NOT LIBOMPTARGET_AMDGPU_ARCH)",
            libomptarget.format(src) + "/hostexec/CMakeLists.txt",
            string=True,
        )

    def install(self, spec, prefix):
        src = self.stage.source_path
        gfx_list = os.environ["GFXLIST"]
        gfx_list = gfx_list.replace(" ", ";")
        openmp_extras_prefix = self.spec["rocm-openmp-extras"].prefix
        devlibs_prefix = self.spec["llvm-amdgpu"].prefix
        if self.spec.satisfies("@6.1:"):
            devlibs_src = "{0}/rocm-openmp-extras/llvm-project/amd/device-libs".format(src)
        else:
            devlibs_src = "{0}/rocm-openmp-extras/rocm-device-libs".format(src)
        hsa_prefix = self.spec["hsa-rocr-dev"].prefix
        hsakmt_prefix = self.spec["hsakmt-roct"].prefix
        if self.spec.satisfies("@5.7:6.1"):
            libdrm_prefix = self.spec["libdrm"].prefix
            numactl_prefix = self.spec["numactl"].prefix
        comgr_prefix = self.spec["comgr"].prefix
        llvm_inc = "/rocm-openmp-extras/llvm-project/llvm/include"
        llvm_prefix = self.spec["llvm-amdgpu"].prefix
        omp_bin_dir = "{0}/bin".format(openmp_extras_prefix)
        omp_lib_dir = "{0}/lib".format(openmp_extras_prefix)
        bin_dir = "{0}/bin".format(llvm_prefix)
        lib_dir = "{0}/lib".format(llvm_prefix)
        flang_warning = "-Wno-incompatible-pointer-types-discards-qualifiers"
        libpgmath = "/rocm-openmp-extras/flang/runtime/libpgmath/lib/common"
        elfutils_inc = spec["elfutils"].prefix.include
        ffi_inc = spec["libffi"].prefix.include
        if self.spec.satisfies("@6.2:"):
            ncurses_lib_dir = self.spec["ncurses"].prefix.lib

        # flang1 and flang2 symlink needed for build of flang-runtime
        # libdevice symlink to rocm-openmp-extras for runtime
        # libdebug symlink to rocm-openmp-extras for runtime
        if os.path.islink((os.path.join(bin_dir, "flang1"))):
            os.unlink(os.path.join(bin_dir, "flang1"))
        if os.path.islink((os.path.join(bin_dir, "flang2"))):
            os.unlink(os.path.join(bin_dir, "flang2"))
        if self.spec.version >= Version("6.1.0"):
            if os.path.islink((os.path.join(bin_dir, "flang-legacy"))):
                os.unlink(os.path.join(bin_dir, "flang-legacy"))
        if os.path.islink((os.path.join(lib_dir, "libdevice"))):
            os.unlink(os.path.join(lib_dir, "libdevice"))
        if os.path.islink((os.path.join(llvm_prefix, "lib-debug"))):
            os.unlink(os.path.join(llvm_prefix, "lib-debug"))

        os.symlink(os.path.join(omp_bin_dir, "flang1"), os.path.join(bin_dir, "flang1"))
        os.symlink(os.path.join(omp_bin_dir, "flang2"), os.path.join(bin_dir, "flang2"))

        if self.spec.version >= Version("6.1.0"):
            os.symlink(
                os.path.join(omp_bin_dir, "flang-legacy"), os.path.join(bin_dir, "flang-legacy")
            )
        os.symlink(os.path.join(omp_lib_dir, "libdevice"), os.path.join(lib_dir, "libdevice"))
        os.symlink(
            os.path.join(openmp_extras_prefix, "lib-debug"), os.path.join(llvm_prefix, "lib-debug")
        )

        # Set cmake args
        components = dict()

        components["aomp-extras"] = [
            "../rocm-openmp-extras/aomp-extras",
            "-DLLVM_DIR={0}".format(llvm_prefix),
            "-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode".format(devlibs_prefix),
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DAOMP_STANDALONE_BUILD=0",
            "-DDEVICELIBS_ROOT={0}".format(devlibs_src),
            "-DNEW_BC_PATH=1",
            "-DAOMP={0}".format(llvm_prefix),
        ]

        # Shared cmake configuration for openmp, openmp-debug
        # Due to hsa-rocr-dev using libelf instead of elfutils
        # the build of openmp fails because the include path
        # for libelf is placed before elfutils in SPACK_INCLUDE_DIRS.
        # Passing the elfutils include path via cmake options is a
        # workaround until hsa-rocr-dev switches to elfutils.
        openmp_common_args = [
            "-DROCM_DIR={0}".format(hsa_prefix),
            "-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode".format(devlibs_prefix),
            "-DAOMP_STANDALONE_BUILD=0",
            "-DDEVICELIBS_ROOT={0}".format(devlibs_src),
            "-DOPENMP_TEST_C_COMPILER={0}/clang".format(bin_dir),
            "-DOPENMP_TEST_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DLIBOMPTARGET_AMDGCN_GFXLIST={0}".format(gfx_list),
            "-DLIBOMP_COPY_EXPORTS=OFF",
            "-DHSA_LIB={0}/lib".format(hsa_prefix),
            "-DHSAKMT_LIB={0}/lib".format(hsakmt_prefix),
            "-DHSAKMT_LIB64={0}/lib64".format(hsakmt_prefix),
            "-DCOMGR_INCLUDE={0}/include".format(comgr_prefix),
            "-DCOMGR_LIB={0}/lib".format(comgr_prefix),
            "-DOPENMP_ENABLE_LIBOMPTARGET=1",
            "-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1",
            "-DLLVM_MAIN_INCLUDE_DIR={0}{1}".format(src, llvm_inc),
            "-DLLVM_INSTALL_PREFIX={0}".format(llvm_prefix),
            "-DCMAKE_C_FLAGS=-isystem{0} -I{1}".format(elfutils_inc, ffi_inc),
            "-DCMAKE_CXX_FLAGS=-isystem{0} -I{1}".format(elfutils_inc, ffi_inc),
            "-DNEW_BC_PATH=1",
            "-DHSA_INCLUDE={0}/include/hsa".format(hsa_prefix),
        ]
        if self.spec.satisfies("@5.7:6.1"):
            openmp_common_args += [
                "-DLIBDRM_LIB={0}/lib".format(libdrm_prefix),
                "-DHSAKMT_INC_PATH={0}/include".format(hsakmt_prefix),
                "-DNUMACTL_DIR={0}".format(numactl_prefix),
            ]

        if self.spec.satisfies("@5.3.0:"):
            openmp_common_args += ["-DLIBOMPTARGET_ENABLE_DEBUG=ON"]

        components["openmp"] = ["../rocm-openmp-extras/llvm-project/openmp"]
        components["openmp"] += openmp_common_args

        components["openmp-debug"] = [
            "../rocm-openmp-extras/llvm-project/openmp",
            "-DLIBOMPTARGET_NVPTX_DEBUG=ON",
            "-DCMAKE_CXX_FLAGS=-g",
            "-DCMAKE_C_FLAGS=-g",
        ]

        components["openmp-debug"] += openmp_common_args

        # Shared cmake configuration for pgmath, flang, flang-runtime
        flang_common_args = [
            "-DLLVM_ENABLE_ASSERTIONS=ON",
            "-DLLVM_CONFIG={0}/llvm-config".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_Fortran_COMPILER={0}/flang".format(bin_dir),
            "-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86",
            # Spack thinks some warnings from the flang build are errors.
            # Disable those warnings in C and CXX flags.
            "-DCMAKE_CXX_FLAGS={0}".format(flang_warning) + " -I{0}{1}".format(src, libpgmath),
            "-DCMAKE_C_FLAGS={0}".format(flang_warning) + " -I{0}{1}".format(src, libpgmath),
        ]

        components["pgmath"] = ["../rocm-openmp-extras/flang/runtime/libpgmath"]

        components["pgmath"] += flang_common_args

        flang_legacy_version = "17.0-4"

        components["flang-legacy-llvm"] = [
            "-DLLVM_ENABLE_PROJECTS=clang",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DLLVM_ENABLE_ASSERTIONS=ON",
            "-DLLVM_TARGETS_TO_BUILD=AMDGPU;X86",
            "-DCLANG_DEFAULT_LINKER=lld",
            "-DLLVM_INCLUDE_BENCHMARKS=0",
            "-DLLVM_INCLUDE_RUNTIMES=0",
            "-DLLVM_INCLUDE_EXAMPLES=0",
            "-DLLVM_INCLUDE_TESTS=0",
            "-DLLVM_INCLUDE_DOCS=0",
            "-DLLVM_INCLUDE_UTILS=0",
            "-DCLANG_DEFAULT_PIE_ON_LINUX=0",
            "../../rocm-openmp-extras/flang/flang-legacy/{0}/llvm-legacy/llvm".format(
                flang_legacy_version
            ),
        ]

        components["flang-legacy"] = [
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "../rocm-openmp-extras/flang/flang-legacy/{0}".format(flang_legacy_version),
        ]

        flang_legacy_flags = []
        if (
            self.compiler.name == "gcc"
            and self.compiler.version >= Version("7.0.0")
            and self.compiler.version < Version("9.0.0")
        ):
            flang_legacy_flags.append("-D_GLIBCXX_USE_CXX11_ABI=0")
        if self.spec.satisfies("@6.2:"):
            flang_legacy_flags.append("-L{0}".format(ncurses_lib_dir))
        components["flang-legacy-llvm"] += [
            "-DCMAKE_CXX_FLAGS={0}".format(",".join(flang_legacy_flags))
        ]
        components["flang-legacy"] += [
            "-DCMAKE_CXX_FLAGS={0}".format(",".join(flang_legacy_flags))
        ]

        components["flang"] = [
            "../rocm-openmp-extras/flang",
            "-DFLANG_OPENMP_GPU_AMD=ON",
            "-DFLANG_OPENMP_GPU_NVIDIA=ON",
        ]

        components["flang"] += flang_common_args

        components["flang-runtime"] = [
            "../rocm-openmp-extras/flang",
            "-DLLVM_INSTALL_RUNTIME=ON",
            "-DFLANG_BUILD_RUNTIME=ON",
            "-DOPENMP_BUILD_DIR={0}/spack-build-openmp/runtime/src".format(src),
        ]
        components["flang-runtime"] += flang_common_args

        build_order = ["aomp-extras", "openmp"]
        if self.spec.version >= Version("6.1.0"):
            build_order += ["flang-legacy-llvm", "flang-legacy"]

        build_order += ["pgmath", "flang", "flang-runtime"]
        # Override standard CMAKE_BUILD_TYPE
        std_cmake_args = CMakeBuilder.std_args(self, generator="Unix Makefiles")
        for arg in std_cmake_args:
            found = re.search("CMAKE_BUILD_TYPE", arg)
            if found:
                std_cmake_args.remove(arg)
        for component in build_order:
            cmake_args = components[component]
            cmake_args.extend(std_cmake_args)
            if component == "flang-legacy-llvm":
                with working_dir("spack-build-{0}/llvm-legacy".format(component), create=True):
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                    cmake(*cmake_args)
                    make()
            elif component == "flang-legacy":
                with working_dir("spack-build-flang-legacy-llvm"):
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                    cmake(*cmake_args)
                    make()
                    make("install")
                    os.symlink(os.path.join(bin_dir, "clang"), os.path.join(omp_bin_dir, "clang"))
            else:
                with working_dir("spack-build-{0}".format(component), create=True):
                    # OpenMP build needs to be run twice(Release, Debug)
                    if component == "openmp-debug":
                        cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")
                    else:
                        cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                    cmake(*cmake_args)
                    make()
                    make("install")
