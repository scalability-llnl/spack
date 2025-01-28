# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Detray(CMakePackage):
    """Detray is a description library for high energy physics experiments that
    works entirely without polymorphism, making it exceptionally suitable for
    use on GPU platforms."""

    homepage = "https://github.com/acts-project/detray"
    url = "https://github.com/acts-project/detray/archive/refs/tags/v0.67.0.tar.gz"

    tags = ["hep"]

    maintainers("stephenswat")

    license("MPL-2.0", checked_by="stephenswat")

    version("0.87.0", sha256="2d4a76432dd6ddbfc00b88b5d482072e471fefc264b60748bb1f9a123963576e")
    version("0.86.0", sha256="98350c94e8a2395b8712b7102fd449536857e8158b38a96cc913c79b70301170")
    version("0.85.0", sha256="a0121a27fd08243d4a6aab060e8ab379ad5129e96775b45f6a683835767fa8e7")
    version("0.84.0", sha256="b1d133a97dc90b1513f8c1ef235ceaa542d80243028a41f59a79300c7d71eb25")
    version("0.83.0", sha256="c870a0459d1f9284750f6afbb97c759392e636b56d107f32b9bc891df717a0fe")
    version("0.82.0", sha256="48794d37496dd5013b755d5d401da7b9d1023fadff86b2a454e5c21e2aaf8c60")
    version("0.81.0", sha256="821313a7e3ea90fcf5c92153d28bba1f85844e03d7c6b6b98d0b3407adb86357")
    version("0.80.0", sha256="a12f3e333778ddd20a568b5c8df5b2375f9a4d74caf921822c1864b07b3f8ab7")
    version("0.79.0", sha256="3b9f18cb003e59795a0e4b1414069ac8558b975714626449293a71bc4398a380")
    version("0.78.0", sha256="ca3a348f4e12ed690c3106197e107b9c393b6902224b2543b00382050864bcf3")
    version("0.77.0", sha256="c2c72f65a7ff2426335b850c0b3cfbbbf666208612b2458c97a534ecf8029cb8")
    version("0.76.1", sha256="54d9abee395e9faf0f56b5d9c137a9990f23712fbcc88fd90af20643bcae635e")
    version("0.76.0", sha256="affa0e28ca96d168e377ba33642e0b626aacdc79f9436233f5561006018f9b9e")
    version("0.75.3", sha256="1249d7398d1e534bd36b6f5a7d06a5e67adf6adeb8bca188d7e35490a675de7a")
    version("0.75.2", sha256="249066c138eac4114032e8d558f3a05885140a809332a347c7667978dbff54ee")
    version("0.74.2", sha256="9fd14cf1ec30477d33c530670e9fed86b07db083912fe51dac64bf2453b321e8")
    version("0.73.0", sha256="f574016bc7515a34a675b577e93316e18cf753f1ab7581dcf1c8271a28cb7406")
    version("0.72.1", sha256="6cc8d34bc0d801338e9ab142c4a9884d19d9c02555dbb56972fab86b98d0f75b")
    version("0.71.0", sha256="2be2b3dac6f77aa8cea033eba841378dc3703ff93c99e4d05ea03df685e6d508")
    version("0.70.0", sha256="14fa1d478d44d5d987caea6f4b365bce870aa8e140c21b802c527afa3a5db869")
    version("0.69.1", sha256="7100ec86a47458a35f5943cd6c7da07c68b8c1c2f62d36d13b8bb50568d0abe5")
    version("0.68.0", sha256="6d57835f22ced9243fbcc29b84ea4c01878a46bfa5910e320c933e9bf8e96612")
    version("0.67.0", sha256="87b1b29f333c955ea6160f9dda89628490d85a9e5186c2f35f57b322bbe27e18")

    variant("csv", default=True, description="Enable the CSV IO plugin")
    _cxxstd_values = (
        conditional("17", when="@:0.72.1"),
        conditional("20", when="@0.67.0:"),
        conditional("23", when="@0.67.0:"),
    )
    _cxxstd_common = {
        "values": _cxxstd_values,
        "multi": False,
        "description": "C++ standard used.",
    }
    variant("cxxstd", default="17", when="@:0.72.1", **_cxxstd_common)
    variant("cxxstd", default="20", when="@0.73.0:", **_cxxstd_common)
    variant("json", default=True, description="Enable the JSON IO plugin")
    variant(
        "scalar",
        default="float",
        values=("float", "double"),
        multi=False,
        description="Scalar type to use by default",
    )
    variant("eigen", default=True, description="Enable the Eigen math plugin")
    variant("smatrix", default=False, description="Enable the SMatrix math plugin")
    variant("vc", default=True, description="Enable the Vc math plugin")

    depends_on("cmake@3.11:", type="build")
    depends_on("vecmem@1.6.0:")
    depends_on("vecmem@1.8.0:", when="@0.76:")
    depends_on("covfie@0.10.0:")
    depends_on("nlohmann-json@3.11.0:", when="+json")
    depends_on("dfelibs@20211029:")
    depends_on("acts-algebra-plugins@0.18.0: +vecmem")
    depends_on("acts-algebra-plugins +vc", when="+vc")
    depends_on("acts-algebra-plugins +eigen", when="+eigen")
    depends_on("acts-algebra-plugins +smatrix", when="+smatrix")
    depends_on("acts-algebra-plugins@0.26.0:", when="@0.87:")

    # Detray imposes requirements on the C++ standard values used by Algebra
    # Plugins.
    with when("+smatrix"):
        for _cxxstd in _cxxstd_values:
            for _v in _cxxstd:
                depends_on(
                    f"acts-algebra-plugins cxxstd={_v.value}", when=f"cxxstd={_v.value} {_v.when}"
                )

    depends_on("actsvg +meta")

    def cmake_args(self):
        args = [
            self.define("DETRAY_USE_SYSTEM_LIBS", True),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("CMAKE_CUDA_STANDARD", "cxxstd"),
            self.define_from_variant("CMAKE_SYCL_STANDARD", "cxxstd"),
            self.define_from_variant("DETRAY_CUSTOM_SCALARTYPE", "scalar"),
            self.define_from_variant("DETRAY_EIGEN_PLUGIN", "eigen"),
            self.define_from_variant("DETRAY_SMATRIX_PLUGIN", "smatrix"),
            self.define_from_variant("DETRAY_IO_CSV", "csv"),
            self.define_from_variant("DETRAY_IO_JSON", "json"),
            self.define_from_variant("DETRAY_VC_PLUGIN", "vc"),
            self.define_from_variant("DETRAY_VC_AOS_PLUGIN", "vc"),
            self.define_from_variant("DETRAY_VC_SOA_PLUGIN", "vc"),
            self.define("DETRAY_SVG_DISPLAY", True),
            self.define("DETRAY_SETUP_ACTSVG", True),
            self.define("DETRAY_BUILD_TESTING", False),
            self.define("DETRAY_SETUP_GOOGLETEST", False),
            self.define("DETRAY_SETUP_BENCHMARK", False),
            self.define("DETRAY_BUILD_TUTORIALS", False),
            self.define("DETRAY_BUILD_TEST_UTILS", True),
        ]

        return args
