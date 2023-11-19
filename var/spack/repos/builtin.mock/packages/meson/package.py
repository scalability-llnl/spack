# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Meson(Package):
    """A dummy package for the meson build system."""

    homepage = "https://mesonbuild.com/"
    url = "https://github.com/mesonbuild/meson/archive/0.49.0.tar.gz"

    version("0.49.0", sha256="11bc959e7173e714e4a4e85dd2bd9d0149b0a51c8ba82d5f44cc63735f603c74")

    def setup_build_environment(self, env):
        spack_cc  # Ensure spack module-scope variable is avaiable
        env.set("for_install", "for_install")

    def setup_dependent_build_environment(self, env, dependent_spec):
        spack_cc  # Ensure spack module-scope variable is avaiable
        env.set("from_meson", "from_meson")

    def setup_dependent_package(self, module, dspec):
        spack_cc  # Ensure spack module-scope variable is avaiable

        module.meson = Executable(self.spec.prefix.bin.meson)
        module.ctest = Executable(self.spec.prefix.bin.ctest)
        self.spec.from_meson = "from_meson"
        module.from_meson = "from_meson"

        self.spec.link_arg = "test link arg"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        check(
            os.environ["for_install"] == "for_install",
            "Couldn't read env var set in compile envieonmnt",
        )
        meson_exe_ext = ".exe" if sys.platform == "win32" else ""
        meson_exe = join_path(prefix.bin, "meson{}".format(meson_exe_ext))
        touch(meson_exe)
        set_executable(meson_exe)
