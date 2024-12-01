# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pypy(Package):
    """A fast, compliant alternative implementation of Python."""

    homepage = "https://www.pypy.org/"
    url = "https://downloads.python.org/pypy/pypy3.10-v7.3.12-src.tar.bz2"
    hg = "https://foss.heptapod.net/pypy/pypy"

    maintainers("adamjstewart")

    license("MIT")

    version(
        "3.10-v7.3.12", sha256="86e4e4eacc36046c6182f43018796537fe33a60e1d2a2cc6b8e7f91a5dcb3e42"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("ctypes", default=True, description="Build ctypes module")
    variant("zlib", default=True, description="Build zlib module")
    variant("bz2", default=True, description="Build bz2 module")
    variant("pyexpat", default=True, description="Build pyexpat module")
    variant("sqlite3", default=True, description="Build sqlite3 module")
    variant("ssl", default=True, description="Build ssl module")
    variant("curses", default=True, description="Build curses module")
    variant("dbm", default=True, description="Build dbm module")
    variant("tkinter", default=False, description="Build tkinter module")
    variant("lzma", default=True, description="Build lzma module")

    # https://doc.pypy.org/en/latest/build.html#install-build-time-dependencies
    depends_on("pypy-bootstrap", type="build")  # any Python 2 executable
    # depends_on("py-cffi", type="build")  # only for CPython

    depends_on("libffi", when="+ctypes")
    depends_on("pkgconfig", when="+ctypes", type="build")
    depends_on("zlib-api", when="+zlib")
    depends_on("bzip2", when="+bz2")
    depends_on("expat", when="+pyexpat")
    depends_on("sqlite", when="+sqlite3")
    depends_on("openssl", when="+ssl")
    depends_on("ncurses", when="+curses")
    depends_on("gdbm", when="+dbm")
    depends_on("tcl", when="+tkinter")
    depends_on("tk", when="+tkinter")
    depends_on("libx11", when="+tkinter")
    depends_on("xz", when="+lzma")

    # TODO: add testing
    # https://doc.pypy.org/en/latest/contributing.html#testing
    # depends_on("bdw-gc@7.4:", type="test")
    # depends_on("openssl", type="test")
    # depends_on("py-pycparser", type="test")
    # depends_on("py-hypothesis", type="test")

    phases = ["translate", "build", "package", "install"]

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, "pypy", "goal")

    def patch(self):
        # Fix detection of tcl/tk
        tklib_build = FileFilter(join_path("lib_pypy", "_tkinter", "tklib_build.py"))
        if "+tkinter" in self.spec:
            incs = self.spec["tcl"].headers + self.spec["tk"].headers
            libs = self.spec["tcl"].libs + self.spec["tk"].libs
            tklib_build.filter("incdirs = .*", f"incdirs = {incs.directories}")
            tklib_build.filter("linklibs = .*", f"linklibs = {libs.names}")
            tklib_build.filter("libdirs = .*", f"libdirs = {libs.directories}")

    def setup_build_environment(self, env):
        # https://doc.pypy.org/en/latest/build.html#set-environment-variables-that-will-affect-translation
        env.set("PYPY_USESSION_DIR", self.stage.source_path)
        env.prepend_path("PYTHONPATH", self.stage.source_path)

    def translate_args(self):
        args = ["--opt=jit", "--shared", "--make-jobs", str(make_jobs), "targetpypystandalone.py"]

        variant_to_flag = {
            "ctypes": "_cffi_backend",
            "bz2": "bz2",
            "zlib": "zlib",
            "pyexpat": "pyexpat",
        }

        for variant, flag in variant_to_flag.items():
            if f"+{variant}" in self.spec:
                args.append(f"--withmod-{flag}")
            else:
                args.append(f"--withoutmod-{flag}")

        return args

    def translate(self, spec, prefix):
        # https://doc.pypy.org/en/latest/build.html#run-the-translation
        rpython = join_path(self.stage.source_path, "rpython", "bin", "rpython")
        with working_dir(self.build_directory):
            pypy(rpython, *self.translate_args())

    def build_args(self):
        modules = ["audioop", "syslog", "grp", "resource", "_posixshmem"]

        if "+ctypes" in self.spec:
            modules.extend(["_ctypes._ctypes_cffi", "_pypy_util_cffi_inner"])

        if "+ssl" in self.spec:
            modules.extend(["_blake2", "_ssl", "_sha3"])

        if "+sqlite3" in self.spec:
            modules.append("sqlite3")

        if "+tkinter" in self.spec:
            modules.append("_tkinter")

        if "+curses" in self.spec:
            modules.append("curses")

        if "+dbm" in self.spec:
            modules.append("_gdbm")

        if "+lzma" in self.spec:
            modules.append("lzma")

        return ["--only=" + ",".join(modules)]

    def build(self, spec, prefix):
        # https://doc.pypy.org/en/latest/build.html#build-cffi-import-libraries-for-the-stdlib
        build_cffi_imports = join_path(
            self.stage.source_path, "lib_pypy", "pypy_tools", "build_cffi_imports.py"
        )
        pypy_c = Executable(join_path(self.build_directory, f"pypy{self.version.up_to(2)}-c"))
        with working_dir(self.build_directory):
            pypy_c(build_cffi_imports, *self.build_args())

    def package_args(self):
        args = [
            f"--builddir={self.build_directory}",
            "--no-embedded-dependencies",
            "--no-make-portable",
        ]

        variant_to_flag = {
            "dbm": "_gdbm",
            "ssl": "_ssl",
            "curses": "curses",
            "lzma": "lzma",
            "sqlite3": "sqlite3",
            "tkinter": "_tkinter",
            "ctypes": "cffi",
        }

        for variant, flag in variant_to_flag.items():
            if f"~{variant}" in self.spec:
                args.append(f"--without-{flag}")

        return args

    def package(self, spec, prefix):
        # https://doc.pypy.org/en/latest/build.html#packaging-preparing-for-installation
        package = join_path(self.stage.source_path, "pypy", "tool", "release", "package.py")
        pypy(package, *self.package_args())

    def install(self, spec, prefix):
        # https://doc.pypy.org/en/latest/build.html#installation
        with working_dir(join_path(self.build_directory, "pypy-nightly")):
            install_tree("bin", prefix.bin)
            install_tree("include", prefix.include)
            install_tree("lib", prefix.lib)
