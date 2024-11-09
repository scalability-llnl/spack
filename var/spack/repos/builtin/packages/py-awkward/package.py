# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwkward(PythonPackage):
    """Manipulate JSON-like data with NumPy-like idioms."""

    git = "https://github.com/scikit-hep/awkward-1.0.git"
    pypi = "awkward/awkward-1.1.2.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers("vvolkl")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("2.6.6", sha256="6eeb426ca41b51fe3c36fbe767b90259979b08c14e3562497a71195a447c8b3c")
    version("2.1.1", sha256="fda8e1634161b8b46b151c074ff0fc631fc0feaec2ec277c4b40a2095110b0dd")
    version("2.1.0", sha256="73f7a76a1fb43e2557befee54b1381f3e6d90636983cdc54da1c2bcb9ad4c1a8")
    version("2.0.10", sha256="8dae67afe50f5cf1677b4062f9b29dc7e6893420d0af5a0649364b117a3502af")
    version("2.0.9", sha256="498e09e85894a952fa8ec4495a7865d2d7a57ab5c522c9e5dcc54419e2793ff2")
    version("2.0.8", sha256="32a57c29e13a2ae3bc1e6ac53637825bbd22c4286696163bd41a1dec284a8ee5")
    version("2.0.7", sha256="05397d659a5a8889c8afae193c0ea51585683038ecc7f666f3da9835ba2f6492")
    version("2.0.6", sha256="9e5133ba6be89ff1210d862edf83824fe0c1f21dccfe1d52161329760ffac821")
    version("2.0.5", sha256="2a07bb0409411782fea226de5c817eb6e48db06d64323977581e4f304f911029")
    version("2.0.4", sha256="fc36ef5934ced78b6d8a40bc94d3ea59667725516b36afea5ed1ef794263a7c7")
    version("2.0.3", sha256="563bb70ef7673ba4dd9dd7116493d1b661bba729305d1fa50efa8cc38ab43da9")
    version("2.0.2", sha256="c7b8194be5f9b1f19ed64c2a4b01d96b1b5a9a357e5a96186c6692d6b4cf439b")
    version("2.0.1", sha256="97fa7e119cc31f479b660a8213df5ba8c938b66f76aadf90b8bdb956c5b5654b")
    version("2.0.0", sha256="3782b34643083d6ee7644e9fdb3daeafc4b6030a667f219fd61cb7b234976b68")
    version("1.10.3", sha256="7e669b1d29da300ed4c4f0d3a14119356037e7cfa8c3aa9d130bf1be6e38f03b")
    version("1.10.2", sha256="303bc0919f0932db3e78a9254c17fcdeb125e4be65cd894b40dfbc3bfddfc054")
    version("1.10.1", sha256="c6394ed25fb14a086d63621d9d84fdc228f5d42a64586f215731b36fde17034b")
    version("1.10.0", sha256="1d89c7244e6184b35f4bce6bd08ff82eb2ef60be67f572923bc6aaee35dab544")
    version("1.9.0", sha256="cad799237e4370b50f77e716e78dd3565a7b3fd82fcd5a41a76aa1512d51075d")
    version("1.8.0", sha256="6655fa22d1b1d1dcb9ccee0d502350ab90c53467a10b540b7624422b594d2e72")
    version("1.7.0", sha256="e4e642dfe496d2acb245c90e37dc18028e25d5e936421e7371ea6ba0fde6435a")
    version("1.5.1", sha256="c0357c62223fefcfc7a7565389dbd4db900623bf10eccf2bc8e87586ec59b38d")
    version("1.5.0", sha256="3cb1b0e28f420232d894d89665d5c0c8241b99e56d806171f4faf5cdfec08ae1")
    version("1.4.0", sha256="25ae6114d5962c717cb87e3bc30a2f6eaa232b252cf8c51ba805b8f04664ae0d")
    version("1.3.0", sha256="b6021694adec9813842bad1987b837e439dabaf5b0dff9041201d238fca71fb4")
    version("1.2.3", sha256="7d727542927a926f488fa62d04e2c5728c72660f17f822e627f349285f295063")
    version("1.2.2", sha256="89f126a072d3a6eee091e1afeed87e0b2ed3c34ed31a1814062174de3cab8d9b")
    version("1.1.2", sha256="4ae8371d9e6d5bd3e90f3686b433cebc0541c88072655d2c75ec58e79b5d6943")
    version("1.0.2", sha256="3468cb80cab51252a1936e5e593c7df4588ea0e18dcb6fb31e3d2913ba883928")

    patch("pybind11.patch", when="@:1.2.2")
    patch("pybind11_02.patch", when="@1.2.3:1.8.0")

    depends_on("py-hatchling@1.10:", when="@2:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@2:", type="build")
    depends_on("py-setuptools@42.0:", when="@:1", type=("build", "run"))
    depends_on("py-pyyaml", when="@:1", type="build")

    _awkward_to_awkward_cpp_map = [
        ("@2.0.0", "@2"),
        ("@2.0.1", "@3"),
        ("@2.0.2", "@4"),
        ("@2.0.3:2.0.4", "@5"),
        ("@2.0.5", "@6"),
        ("@2.0.6", "@7"),
        ("@2.0.7", "@8"),
        ("@2.0.8", "@9"),
        ("@2.0.9", "@10"),
        ("@2.0.10", "@11"),
        ("@2.1.0:2.1.1", "@12"),
        ("@2.6.6:", "@35"),
    ]
    for _awkward, _awkward_cpp in _awkward_to_awkward_cpp_map:
        depends_on("py-awkward-cpp{}".format(_awkward_cpp), when=_awkward, type=("build", "run"))

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("python@3.6:", when="@1.9:", type=("build", "run"))
    depends_on("python@3.7:", when="@1.10:", type=("build", "run"))
    depends_on("python@3.8:", when="@2.3:", type=("build", "run"))
    depends_on("py-numpy@1.13.1:", when="@:1", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", when="@2.0", type=("build", "run"))
    depends_on("py-numpy@1.17.0:", when="@2.1:", type=("build", "run"))
    depends_on("py-numpy@1.18.0:", when="@2.3:", type=("build", "run"))
    depends_on("py-pybind11", type=("build", "link"))
    depends_on("py-importlib-resources", when="@2: ^python@:3.8", type=("build", "run"))
    depends_on("py-typing-extensions@4.1:", when="@2: ^python@:3.10", type=("build", "run"))
    depends_on("py-packaging", when="@2:", type=("build", "run"))
    depends_on("dlpack", when="@1.0.0:")
    depends_on("rapidjson")
    depends_on("cmake@3.13:", type="build")
    depends_on("py-wheel@0.36.0:", when="@:1.7.0", type="build")

    @when("@1.9.0:")
    def setup_build_environment(self, env):
        env.set("CMAKE_ARGS", "-DAWKWARD_EXTERNAL_PYBIND11=TRUE")
