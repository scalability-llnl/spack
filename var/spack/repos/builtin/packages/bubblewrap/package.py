# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.autotools
import spack.build_systems.meson
from spack.package import *


class Bubblewrap(AutotoolsPackage, MesonPackage):
    """Unprivileged sandboxing tool"""

    homepage = "https://github.com/containers/bubblewrap"
    url = (
        "https://github.com/containers/bubblewrap/releases/download/v0.3.0/bubblewrap-0.3.0.tar.xz"
    )
    maintainers("haampie")

    license("LGPL-2.0-or-later")

    build_system(
        conditional("autotools", when="@:0.10"),
        conditional("meson", when="@0.6:"),
        default="meson",
    )

    version("0.11.0", sha256="988fd6b232dafa04b8b8198723efeaccdb3c6aa9c1c7936219d5791a8b7a8646")
    version("0.10.0", sha256="65d92cf44a63a51e1b7771f70c05013dce5bd6b0b2841c4b4be54b0c45565471")
    version("0.9.0", sha256="c6347eaced49ac0141996f46bba3b089e5e6ea4408bc1c43bab9f2d05dd094e1")
    version("0.8.0", sha256="957ad1149db9033db88e988b12bcebe349a445e1efc8a9b59ad2939a113d333a")
    version("0.7.0", sha256="764ab7100bd037ea53d440d362e099d7a425966bc62d1f00ab26b8fbb882a9dc")
    version("0.6.3", sha256="d8cab8943a36cd1bc1b8c63596c6ef6b29b12883d90ed9b14a969795ac60ddef")
    version("0.6.2", sha256="8a0ec802d1b3e956c5bb0a40a81c9ce0b055a31bf30a8efa547433603b8af20b")
    version("0.6.1", sha256="9609c7dc162bc68abc29abfab566934fdca37520a15ed01b675adcf3a4303282")
    version("0.6.0", sha256="11393cf2058f22e6a6c6e9cca3c85ff4c4239806cb28fee657c62a544df35693")
    version("0.5.0", sha256="16fdaf33799d63104e347e0133f909196fe90d0c50515d010bcb422eb5a00818")
    version("0.4.1", sha256="b9c69b9b1c61a608f34325c8e1a495229bacf6e4a07cbb0c80cf7a814d7ccc03")
    version("0.4.0", sha256="e5fe7d2f74bd7029b5306b0b70587cec31f74357739295e5276b4a3718712023")
    version("0.3.3", sha256="c6a45f51794a908b76833b132471397a7413f07620af08e76c273d9f7b364dff")
    version("0.3.1", sha256="deca6b608c54df4be0669b8bb6d254858924588e9f86e116eb04656a3b6d4bf8")

    depends_on("c", type="build")
    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
    with when("build_system=meson"):
        depends_on("meson@0.49:", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("libcap", type="link")


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        return ["-Dman=disabled", "-Dselinux=disabled"]


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        return [
            "--disable-sudo",
            "--disable-man",
            "--disable-selinux",
            "--with-bash-completion-dir="
            + join_path(self.spec.prefix, "share", "bash-completion", "completions"),
        ]
