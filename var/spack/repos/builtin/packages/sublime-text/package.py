# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SublimeText(Package):
    """Sublime Text is a sophisticated text editor for code, markup and
    prose."""

    homepage = "https://www.sublimetext.com/"
    url = "https://download.sublimetext.com/sublime_text_build_4152_x64.tar.xz"

    maintainers("LRWeber")

    version("4.4152", sha256="6ede3c83519959897041c6506e850753c19962603b71bd9f73a625ae1e4d3554")
    version("4.4143", sha256="7de862c38d19367414117110328dded754ac709fed54c8cc5cb0737c894c073c")
    version(
        "3.2.2.3211", sha256="0b3c8ca5e6df376c3c24a4b9ac2e3b391333f73b229bc6e87d0b4a5f636d74ee"
    )
    version(
        "3.2.1.3207", sha256="acb64f1de024a0f004888096afa101051e48d96c7a3e7fe96e11312d524938c4"
    )
    version(
        "3.1.1.3176", sha256="74f17c1aec4ddec9d4d4c39f5aec0414a4755d407a05efa571e8892e0b9cf732"
    )
    version("3.0.3126", sha256="18db132e9a305fa3129014b608628e06f9442f48d09cfe933b3b1a84dd18727a")
    version("2.0.2", sha256="01baed30d66432e30002a309ff0393967be1daba5cce653e43bba6bd6c38ab84")

    # Licensing
    license_required = True
    license_url = "https://www.sublimehq.com/store/text"

    # Sublime text comes as a pre-compiled binary.
    # Since we can't link to Spack packages, we'll just have to
    # add them as runtime dependencies.

    # depends_on("libgobject", type="run")
    depends_on("gtkplus@:2", type="run", when="@:3.1")
    depends_on("gtkplus@3:", type="run", when="@3.2:3.2.2")
    depends_on("glib", type="run", when="@:3.2.2")
    depends_on("libx11", type="run", when="@:3.2.2")
    depends_on("pcre", type="run", when="@:3.2.2")
    depends_on("libffi", type="run", when="@:3.2.2")
    depends_on("libxcb", type="run", when="@:3.2.2")
    depends_on("libxau", type="run", when="@:3.2.2")

    def url_for_version(self, version):
        if version[0] == 2:
            return "https://download.sublimetext.com/Sublime%20Text%20{0}%20x64.tar.bz2".format(
                version
            )
        elif version[0] == 3:
            return (
                "https://download.sublimetext.com/sublime_text_{0}_build_{1}_x64.tar.bz2".format(
                    version[0], version[-1]
                )
            )
        else:
            return "https://download.sublimetext.com/sublime_text_build_{0}_x64.tar.xz".format(
                version[-1]
            )

    def install(self, spec, prefix):
        install_tree(".", prefix)
        src = join_path(prefix, "sublime_text")
        dst = join_path(prefix, "bin")
        mkdirp(dst)
        force_symlink(src, join_path(dst, "sublime_text"))
        force_symlink(src, join_path(dst, "subl"))
