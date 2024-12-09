# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bubblewrap(AutotoolsPackage):
    """Unprivileged sandboxing tool"""

    homepage = "https://github.com/containers/bubblewrap"
    url = (
        "https://github.com/containers/bubblewrap/releases/download/v0.3.0/bubblewrap-0.3.0.tar.xz"
    )
    maintainers("haampie")

    license("LGPL-2.0-or-later")

    version("0.8.0", sha256="957ad1149db9033db88e988b12bcebe349a445e1efc8a9b59ad2939a113d333a")
    version("0.7.0", sha256="764ab7100bd037ea53d440d362e099d7a425966bc62d1f00ab26b8fbb882a9dc")
    version("0.6.2", sha256="8a0ec802d1b3e956c5bb0a40a81c9ce0b055a31bf30a8efa547433603b8af20b")
    version("0.6.1", sha256="9609c7dc162bc68abc29abfab566934fdca37520a15ed01b675adcf3a4303282")
    version("0.6.0", sha256="11393cf2058f22e6a6c6e9cca3c85ff4c4239806cb28fee657c62a544df35693")
    version("0.5.0", sha256="16fdaf33799d63104e347e0133f909196fe90d0c50515d010bcb422eb5a00818")
    version("0.4.1", sha256="b9c69b9b1c61a608f34325c8e1a495229bacf6e4a07cbb0c80cf7a814d7ccc03")
    version("0.4.0", sha256="e5fe7d2f74bd7029b5306b0b70587cec31f74357739295e5276b4a3718712023")
    version("0.3.3", sha256="c6a45f51794a908b76833b132471397a7413f07620af08e76c273d9f7b364dff")
    version("0.3.1", sha256="deca6b608c54df4be0669b8bb6d254858924588e9f86e116eb04656a3b6d4bf8")

    depends_on("c", type="build")  # generated

    def configure_args(self):
        return ["--disable-sudo", "--disable-man", "--without-bash-completion-dir"]

    depends_on("pkgconfig", type="build")
    depends_on("libcap")
