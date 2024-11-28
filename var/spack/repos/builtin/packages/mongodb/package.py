# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------
import os

from spack.package import *


class Mongodb(SConsPackage):
    """MongoDB is a source-available cross-platform document-oriented database
    program. Classified as a NoSQL database program, MongoDB uses JSON-like
    documents with optional schemas."""

    homepage = "https://www.mongodb.com/"

    maintainers("DaxLynch")

    license("SSPL-1.0")

    version("6.2", git="https://github.com/mongodb/mongo.git", branch="v6.2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    requires(
        "%gcc", "%clang", policy="one_of", msg="<myNicePackage> builds only with GCC or Clang"
    )
    depends_on("xz")
    depends_on("curl")
    depends_on("py-cryptography@36.0.1")
    depends_on("py-requirements-parser")
    depends_on("py-psutil@:5.8")
    depends_on("py-pymongo@3.9:4.0")
    depends_on("py-pyyaml@3:6")
    depends_on("py-requests@2.0.0:2.26.0")
    depends_on("py-typing-extensions@3.7.4:")

    depends_on("py-cheetah3@:3.2.6")
    depends_on("py-packaging@:21.3")
    depends_on("py-regex@:2021.11.10")
    depends_on("py-setuptools")
    depends_on("ninja@1.10.0")

    depends_on("py-distro@1.5.0")
    depends_on("py-gitpython@3.1.7")
    depends_on("py-pydantic@1.8.2")
    depends_on("py-dnspython")

    def build(self, spec, prefix):
        pass  # This specific scons only uses the install phase

    def install(self, spec, prefix):
        library_dirs = []
        include_dirs = []
        # Sometimes scons does not detect curl or ninja, so these arrays
        # get the include and lib directories and then are explicitly
        # passed it to scons

        # Scons fails to find the the python packages, even when linking
        # with them with -I package-prefix/lib/python3.10/site_packages/
        # (this is one of the options for scons). To work around this, I
        # symlink package-prefix/lib/python3.X/site_packages/package/ to
        # python-prefix/lib/python3.X/site_package/package/ I then
        # remove these after the install.
        python_prefix_lib = self.spec["python"].prefix.lib  # python-prefix/lib
        lib_contents = os.scandir(python_prefix_lib)
        python_version = ""
        python_site_packages = ""
        for entry in lib_contents:
            if entry.is_dir() and entry.name.startswith("python3"):
                # this gets the path python-prefix/lib/python3.X
                python_version = entry.name
                # sets the version as python3.X
                python_site_packages = os.path.join(entry.path, "site-packages")
                # python-prefix/lib/python3.X/site-packages

        for dep in spec.dependencies(deptype="link"):  # iterate through the dependencies
            query = self.spec[dep.name]
            lib = query.prefix.lib
            if dep.name in ["curl", "ninja", "xz"]:
                # For the non python packages, we just extract the
                # package-prefix/lib and package-prefix/include
                try:
                    library_dirs.extend(query.libs.directories)
                    include_dirs.extend(query.headers.directories)
                except Exception:
                    pass
            else:
                dependency_site_packages = os.path.join(lib, python_version, "site-packages")
                # package-prefix/lib/python3.X/site-packages
                for entry in os.scandir(dependency_site_packages):
                    # iterates through files in site-packages
                    try:
                        os.symlink(entry.path, os.path.join(python_site_packages, entry.name))
                    except Exception:
                        pass

        # PYTHONDIRS="-I" + " -I".join(os.environ["PYTHONPATH"].split(":"))
        # ^This is an attempt to pass the python directories directly to scons.
        # Just add PYTHONDIRS as an argument to scons. It sadly does not work :(
        # but feel free to try it.To get more information on the options for scons,
        # do spack load scons, and then scons --help in the mongodb repo
        LINKFLAGS = "-L" + " -L".join(library_dirs)
        CXXFLAGS = "-I" + " -I".join(include_dirs)
        scons(
            "DESTDIR=%s" % prefix,
            "install-mongod",
            "--disable-warnings-as-errors",
            "MONGO_VERSION=6.2.0",
            "CC=%s" % self.compiler.cc,
            "CXX=%s" % self.compiler.cxx,
            "CCFLAGS=%s" % CXXFLAGS + " " + LINKFLAGS,
            "LINKFLAGS=%s" % LINKFLAGS,
        )

        prefix_lib_python_site_package = os.scandir(
            os.path.join(python_prefix_lib, python_version, "site-packages")
        )  # python-prefix/lib/python3.X/site-packages
        for entry in prefix_lib_python_site_package:  # remove symlinks after install
            if entry.is_symlink():
                os.unlink(entry.path)
