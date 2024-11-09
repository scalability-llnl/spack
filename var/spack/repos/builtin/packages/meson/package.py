# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *


class Meson(PythonPackage):
    """Meson is a portable open source build system meant to be both
    extremely fast, and as user friendly as possible."""

    homepage = "https://mesonbuild.com/"
    url = "https://github.com/mesonbuild/meson/archive/0.49.0.tar.gz"

    tags = ["build-tools"]

    maintainers("eli-schwartz", "michaelkuhn")

    license("Apache-2.0")

    version("1.5.1", sha256="55f6acd5bf72c14d4aa5a781993633f84a1d117bdf2c2057735902ced9b81390")
    version("1.4.2", sha256="11d1336fe35e1ade57510a846a31d7dc2e3b6ac1e2491c2831bce5a2a192ba0d")
    version("1.3.2", sha256="683082fb3c5cddf203b21d29bdf4c227e2f7964da5324a15e1a5f7db94322b4b")
    version("1.2.2", sha256="1caa0ef6082e311bdca9836e7907f548b8c3f041a42ed41f0ff916b83ac7dddd")
    version("1.1.1", sha256="1c3b9e1a3a36b51adb5de498d582fd5cbf6763fadbcf151de9f2a762e02bd2e6")
    version("1.0.2", sha256="1f1239c3091668643f7d2086663d6afd8cc87fbab84fe7462bc18b9ba6d65de8")

    with default_args(deprecated=True):
        version("1.2.1", sha256="e1f3b32b636cc86496261bd89e63f00f206754697c7069788b62beed5e042713")
        version("1.2.0", sha256="603489f0aaa6305f806c6cc4a4455a965f22290fc74f65871f589b002110c790")
        version("1.1.0", sha256="f29a3e14062043d75e82d16f1e41856e6b1ed7a7c016e10c7b13afa7ee6364cc")
        version("1.0.1", sha256="4ab3a5c0060dc22bdefb04507efc6c38acb910e91bcd467a38e1fa211e5a6cfe")
        version("1.0.0", sha256="a2ada84d43c7e57400daee80a880a1f5003d062b2cb6c9be1747b0db38f2eb8d")
        version(
            "0.64.1", sha256="1d12a4bc1cf3ab18946d12cf0b6452e5254ada1ad50aacc97f87e2cccd7da315"
        )
        version(
            "0.64.0", sha256="6477993d781b6efea93091616a6d6a0766c0e026076dbeb11249bf1c9b49a347"
        )
        version(
            "0.63.3", sha256="7c516c2099b762203e8a0a22412aa465b7396e6f9b1ab728bad6e6db44dc2659"
        )
        version(
            "0.63.2", sha256="023a3f7c74e68991154c3205a6975705861eedbf8130e013d15faa1df1af216e"
        )
        version(
            "0.63.1", sha256="f355829f0e8c714423f03a06604c04c216d4cbe3586f3154cb2181076b19207a"
        )
        version(
            "0.62.2", sha256="97108f4d9bb16bc758c44749bd25ec7d42c6a762961efbed8b7589a2a3551ea6"
        )
        version(
            "0.62.1", sha256="9fb52e66dbc613479a5f70e46cc2e8faf5aa65e09313f2c71fa63b8afd018107"
        )
        version(
            "0.62.0", sha256="72ac3bab701dfd597604de29cc74baaa1cc0ad8ca26ae23d5288de26abfe1c80"
        )
        version(
            "0.61.4", sha256="c9cc34bcb15c19cfd5ee0d7b07111152701f602db2b59ef6b63d3628e0bbe719"
        )
        version(
            "0.61.2", sha256="33cd555314a94d52acfbb3f6f44d4e61c4ad0bfec7acf4301be7e40bb969b3a8"
        )
        version(
            "0.60.3", sha256="6c191a9b4049e0c9a2a7d1275ab635b91f6ffec1912d75df4c5ec6acf35f74fe"
        )
        version(
            "0.60.0", sha256="5672a560fc4094c88ca5b8be0487e099fe84357e5045f5aecf1113084800e6fd"
        )
        version(
            "0.59.2", sha256="e6d5ccd503d41f938f6cfc4dc9e7326ffe28acabe091b1ff0c6535bdf09732dd"
        )
        version(
            "0.59.1", sha256="f256eb15329a6064f8cc1f23b29de1fa8d21e324f939041e1a4efe77cf1362ef"
        )
        version(
            "0.59.0", sha256="fdbbe8ea8a47f9e21cf4f578f85be8ec3d9c030df3d8cb17df1ae59d8683813a"
        )
        version(
            "0.58.2", sha256="58115604dea9c1f70811578df3c210f4d67cf795d21a4418f6e9bb35406953f5"
        )
        version(
            "0.58.1", sha256="78e0f553dd3bc632d5f96ab943b1bbccb599c2c84ff27c5fb7f7fff9c8a3f6b4"
        )
        version(
            "0.58.0", sha256="991b882bfe4d37acc23c064a29ca209458764a580d52f044f3d50055a132bed4"
        )
        version(
            "0.57.2", sha256="cd3773625253df4fd1c380faf03ffae3d02198d6301e7c8bc7bba6c66af66096"
        )
        version(
            "0.57.1", sha256="0c043c9b5350e9087cd4f6becf6c0d10b1d618ca3f919e0dcca2cdf342360d5d"
        )
        version(
            "0.57.0", sha256="fd26a27c1a509240c668ebd29d280649d9239cf8684ead51d5cb499d1e1188bd"
        )
        version(
            "0.56.2", sha256="aaae961c3413033789248ffe6762589e80b6cf487c334d0b808e31a32c48f35f"
        )
        version(
            "0.56.0", sha256="a9ca7adf66dc69fbb7e583f7c7aef16b9fe56ec2874a3d58747e69a3affdf300"
        )
        version(
            "0.55.3", sha256="2b276df50c5b13ccdbfb14d3333141e9e7985aca31b60400b3f3e0be2ee6897e"
        )
        version(
            "0.55.2", sha256="56244896e56c2b619f819d047b6de412ecc5250975ee8717f1e329113d178e06"
        )
        version(
            "0.55.1", sha256="c7ebf2fff5934a974c7edd1aebb5fc9c3e1da5ae3184a29581fde917638eea39"
        )
        version(
            "0.55.0", sha256="9034c943c8cf4d734c0e18e5ba038dd762fcdcc614c45b41703305da8382e90c"
        )
        version(
            "0.54.3", sha256="c25caff342b5368bfe33fab6108f454fcf12e2f2cef70817205872ddef669e8b"
        )
        version(
            "0.54.2", sha256="85cafdc70ae7d1d9d506e7356b917c649c4df2077bd6a0382db37648aa4ecbdb"
        )
        version(
            "0.54.1", sha256="854e8b94ab36e5aece813d2b2aee8a639bd52201dfea50890722ac9128e2f59e"
        )
        version(
            "0.54.0", sha256="95efdbaa7cb3e915ab9a7b26b1412475398fdc3e834842a780f1646c7764f2d9"
        )
        version(
            "0.53.2", sha256="eab4f5d5dde12d002b7ddd958a9a0658589b63622b6cea2715e0235b95917888"
        )
        version(
            "0.49.1", sha256="a944e7f25a2bc8e4ba3502ab5835d8a8b8f2530415c9d6fcffb53e0abaea2ced"
        )
        version(
            "0.49.0", sha256="11bc959e7173e714e4a4e85dd2bd9d0149b0a51c8ba82d5f44cc63735f603c74"
        )
        version(
            "0.42.0", sha256="6c318a2da3859326a37f8a380e3c50e97aaabff6990067218dffffea674ed76f"
        )
        version(
            "0.41.2", sha256="2daf448d3f2479d60e30617451f09bf02d26304dd1bd12ee1de936a53e42c7a4"
        )
        version(
            "0.41.1", sha256="a48901f02ffeb9ff5cf5361d71b1fca202f9cd72998043ad011fc5de0294cf8b"
        )

    depends_on("python@3.7:", when="@0.62.0:", type=("build", "run"))
    depends_on("python@3.6:", when="@0.57.0:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@0.62.0:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("ninja@1.8.2:", when="@0.62.0:", type="run")
    depends_on("ninja", type="run")

    # By default, Meson strips the rpath on installation. This patch disables
    # rpath modification completely to make sure that Spack's rpath changes
    # are not reverted.
    patch("rpath-0.49.patch", when="@0.49:0.53")
    patch("rpath-0.54.patch", when="@0.54:0.55")
    patch("rpath-0.56.patch", when="@0.56:0.57")
    patch("rpath-0.58.patch", when="@0.58:0.63")
    patch("rpath-0.64.patch", when="@0.64:")

    # Intel OneAPI compiler support
    # https://github.com/mesonbuild/meson/pull/10909
    # https://github.com/mesonbuild/meson/pull/9850
    patch("oneapi.patch", when="@0.62:0.63 %oneapi")

    # Python 3.12 detection support
    patch("python-3.12-support.patch", when="@1.1:1.2.2")

    executables = ["^meson$"]

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)("--version", output=str, error=str).rstrip()

    def setup_dependent_build_environment(self, env, dependent_spec):
        # https://github.com/pybind/pybind11/issues/595
        if self.spec.satisfies("platform=darwin"):
            env.set("STRIP", "strip -x")

    def _meson_bin_dir(self):
        bin_dir = self.spec.prefix.bin
        if sys.platform == "win32":
            bin_dir = self.spec.prefix.scripts
        return bin_dir

    def setup_dependent_package(self, module, dspec):
        module.meson = Executable(self._meson_bin_dir().meson)
