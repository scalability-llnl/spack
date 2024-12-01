# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AsdfCxx(CMakePackage):
    """ASDF - Advanced Scientific Data Format, a C++ implementation"""

    homepage = "https://github.com/eschnett/asdf-cxx"
    url = "https://github.com/eschnett/asdf-cxx/archive/version/1.0.0.tar.gz"

    maintainers("eschnett")

    license("MIT")

    version("7.2.1", sha256="40864f4f27d3ce8acb5169b57211ce6ac3805f0a6de9c1dfd5f994f4a5beccda")
    version("7.2.0", sha256="faded85d44288afb83f13634d2139adee07e06f7ea60960c6f2ef8d898c0aa09")
    version("7.1.0", sha256="81fd8c7f91f8daf0f85a1486480ae9e736b9712e82ccb858271f7ee2c2b425f7")
    version("7.0.0", sha256="a50718dfa68b86b0c3e280e6a9d0a4edb03d500ba70244bd38fa86bac1433979")
    version("6.3.0", sha256="44a24cc490cf776106edcfded6006d63d28889dfe985cce3bd565d5151add9c8")
    version("6.0.0", sha256="76ab0a893191a33a88a753d09a20135470f809c66173794fa3e37a2437ea3cde")
    version("5.0.0", sha256="876c83bcc7514f2584dbf5462bd5b7de89b41301ec127451342079e703cd6a67")
    version("4.0.1", sha256="c4597b8353b0e181d97c6702dae0cb69a558ae5b553945298757433615bb199b")
    version("3.1.0", sha256="15de5156460ed581e1e755955e6a1b557758a6497d083c4873d143c05e720078")
    version("3.0.0", sha256="a6d42f7d875eff2f1ff6af836a44e7a44fcc6be3409605d45f236e07d70c65db")
    version("2.6.1", sha256="631426bd2784c2175b5a5035c12e91b0b0d36691f9972df427b41080ace43fc3")
    version("2.5.1", sha256="d3c1f690716bd0883c4d429c9fa895ce41e6223bafa87624f9f1530c0d2e654c")
    version("2.5.0", sha256="916e9021063c41eb7922ed69c958ea87757cdfcb7263d0d3fda31f0233dbbaaf")
    version("2.4.1", sha256="a300bf11d4fd9923eb109c5f8e1067f2ef96f284ea43fafd871b469118d42597")
    version("2.4.0", sha256="965360858bcacb6df4602fdff55924f7b9daf0750b27ac3f31781e23b54e8f93")
    version("2.3.1", sha256="7c3ecf4fdafff5da57edb8b0c75b2e1f9c6bf42097c483025ff49f0a65094e22")
    version("2.2.1", sha256="a34679d8690ff118bedd20652caebdb9c3fb5f628aca7ed2f535a026b28b3853")
    version("2.1.1", sha256="f1a801b82facb2c0913ca3dce9c62970651e58fae8bc232f5079a1c4773ec6fa")
    version("2.1.0", sha256="066c2c1033be41e10b874ceec1e87267fd792c40d46cbc768b05ba94cca234a1")
    version("1.1.0", sha256="3e23b9cd16254f5adbf878145e320f56b4d3ad75de23d2c761eb7f04150926c5")
    version("1.0.0", sha256="0b63594a1dec27cc85d25adbf900b6e936b5015f579b9b892b983151bec96775")

    depends_on("cxx", type="build")  # generated

    variant("python", default=True, description="Enable Python support")

    depends_on("bzip2")
    depends_on("openssl")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("python", type=("build", "run"), when="+python")
    # An error in the cmake script requires swig all the time, not only when
    # Python bindings are used
    depends_on("swig @3.0.0:3", type="build")
    # Neither earlier nor later versions of yaml-cpp work
    depends_on("yaml-cpp @0.6.3")
    depends_on("zlib-api")
