# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HipRocclr(CMakePackage):
    """Hip-ROCclr is a virtual device interface that compute runtimes interact
    with to different backends such as ROCr or PAL This abstraction allows
    runtimes to work on Windows as well as on Linux without much effort."""

    homepage = "https://github.com/ROCm/ROCclr"
    url = "https://github.com/ROCm/ROCclr/archive/rocm-5.6.1.tar.gz"
    git = "https://github.com/ROCm/ROCclr.git"
    tags = ["rocm"]

    phases = ["cmake", "build"]

    maintainers("srekolam", "renjithravindrankannath")

    license("MIT")

    version("master", branch="main")
    version("5.6.1", sha256="cc9a99c7e4de3d9360c0a471b27d626e84a39c9e60e0aff1e8e1500d82391819")
    version("5.6.0", sha256="864f87323e793e60b16905284fba381a7182b960dd4a37fb67420c174442c03c")
    version("5.5.1", sha256="1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e")
    version("5.5.0", sha256="efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1")
    with default_args(deprecated=True):
        version("5.4.3", sha256="71d9668619ab57ec8a4564d11860438c5aad5bd161a3e58fbc49555fbd59182d")
        version("5.4.0", sha256="46a1579310b3ab9dc8948d0fb5bed4c6b312f158ca76967af7ab69e328d43138")
        version("5.3.3", sha256="f8133a5934f9c53b253d324876d74f08a19e2f5b073bc94a62fe64b0d2183a18")
        version("5.3.0", sha256="2bf14116b5e2270928265f5d417b3d0f0f2e13cbc8ec5eb8c80d4d4a58ff7e94")
        version("5.2.3", sha256="0493c414d4db1af8e1eb30a651d9512044644244488ebb13478c2138a7612998")
        version("5.2.1", sha256="465ca9fa16869cd89dab8c2d66d9b9e3c14f744bbedaa1d215b0746d77a500ba")
        version("5.2.0", sha256="37f5fce04348183bce2ece8bac1117f6ef7e710ca68371ff82ab08e93368bafb")
        version("5.1.3", sha256="ddee63cdc6515c90bab89572b13e1627b145916cb8ede075ef8446cbb83f0a48")
        version("5.1.0", sha256="f4f265604b534795a275af902b2c814f416434d9c9e16db81b3ed5d062187dfa")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3:", type="build")
    depends_on("gl@4.5:", type="link")
    depends_on("numactl", type="link")

    for ver in ["5.3.0", "5.3.3", "5.4.0", "5.4.3", "5.5.0", "5.5.1", "5.6.0", "5.6.1", "master"]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")

    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ("5.6.1", "ec26049f7d93c95050c27ba65472736665ec7a40f25920a868616b2970f6b845"),
        ("5.6.0", "52ab260d00d279c2a86c353901ffd88ee61b934ad89e9eb480f210656705f04e"),
        ("5.5.1", "a8a62a7c6fc5398406d2203b8cb75621a24944688e545d917033d87de2724498"),
        ("5.5.0", "0df9fa0b8aa0c8e6711d34eec0fdf1ed356adcd9625bc8f1ce9b3e72090f3e4f"),
        ("5.4.3", "b0f8339c844a2e62773bd85cd1e7c5ecddfe71d7c8e8d604e1a1d60900c30873"),
        ("5.4.0", "a294639478e76c75dac0e094b418f9bd309309b07faf6af126cdfad9aab3c5c7"),
        ("5.3.3", "cab394e6ef16c35bab8de29a66b96a7dc0e7d1297aaacba3718fa1d369233c9f"),
        ("5.3.0", "d251e2efe95dc12f536ce119b2587bed64bbda013969fa72be58062788044a9e"),
    ]:
        resource(
            name="opencl-on-vdi",
            url=f"https://github.com/ROCm/ROCm-OpenCL-Runtime/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="opencl-on-vdi",
            when=f"@{d_version}",
        )

    resource(
        name="opencl-on-vdi",
        git="https://github.com/ROCm/ROCm-OpenCL-Runtime.git",
        destination="",
        placement="opencl-on-vdi",
        branch="main",
        when="@master",
    )

    def cmake_args(self):
        return [
            self.define("USE_COMGR_LIBRARY", "yes"),
            self.define("OPENCL_DIR", join_path(self.stage.source_path, "opencl-on-vdi")),
        ]
