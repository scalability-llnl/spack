# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Sarus(CMakePackage):
    """Sarus is an OCI-compliant container engine for HPC systems."""

    homepage = "https://github.com/eth-cscs/sarus"
    url = "https://github.com/eth-cscs/sarus/archive/1.3.3.tar.gz"
    git = "https://github.com/eth-cscs/sarus.git"
    maintainers("Madeeks", "taliaga", "teonnik")

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.4.1", commit="a73f6ca9cafb768f3132cfcef8c826af34eeff94")
    version("1.4.0", commit="c6190faf45d5e0ff5348c70c2d4b1e49b2e01039")
    version("1.3.3", commit="f2c000caf3d6a89ea019c70e2703da46799b0e9c")
    version("1.3.2", commit="ac6a1b8708ec402bbe810812d8af41d1b7bf1860")
    version("1.3.1", commit="5117a0da8d2171c4bf9ebc6835e0dd6b73812930")
    version("1.3.0", commit="f52686fa942d5fc2b1302011e9a081865285357b")
    version("1.2.0", commit="16d27c0c10366dcaa0c72c6ec72331b6e4e6884d")
    version("1.1.0", commit="ed5b640a45ced6f6a7a2a9d295d3d6c6106f39c3")
    version("1.0.1", commit="abb8c314a196207204826f7b60e5064677687405")
    version("1.0.0", commit="d913b1d0ef3729f9f41ac5bd06dd5615c407ced4")

    depends_on("cxx", type="build")  # generated

    variant(
        "ssh",
        default=False,
        description="Build and install the SSH hook and custom SSH software "
        "to enable connections inside containers."
        "Requires a static version of the glibc libraries "
        "(including libcrypt) to be available on the system",
    )

    depends_on("expat", type="build")
    depends_on("squashfs", type=("build", "run"))
    depends_on("boost@1.65.0: cxxstd=11 +program_options")
    depends_on("cpprestsdk@2.10.0:")
    depends_on("libarchive@3.4.1:")
    depends_on("rapidjson@1.2.0-2021-08-13", type="build")
    depends_on("runc")
    depends_on("tini")

    # autoconf is required to build Dropbear for the SSH hook
    depends_on("autoconf", type="build")

    # Python 3 is used to run integration tests
    depends_on("python@3:", type="test", when="@develop")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_files/gcc.cmake",
            "-DENABLE_SSH=%s" % ("+ssh" in spec),
        ]

        if "@1.4.1:" in spec:
            args.append(self.define("ENABLE_UNIT_TESTS", self.run_tests))

        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make(*self.install_targets)
            mkdirp(prefix.var.OCIBundleDir)

    @run_after("install")
    def build_perms_script(self):
        script_sh = join_path(self.spec.prefix, "configure_installation.sh")
        tty.warn(
            """
                To complete Sarus's configuration:

                1. Make sure sarus and its dependencies (tini, squashfs) are in
                   PATH, for example do `spack load sarus`.

                2. Execute the script {} with root privileges.

                The script generates a basic working configuration. For more
                details:

                https://sarus.readthedocs.io/en/stable/config/basic_configuration.html

                For production it is strongly recommended to install with
                escalated privileges (sudo/root) in order to comply with Sarus'
                internal security checks. For more information on these checks,
                see :

                https://sarus.readthedocs.io/en/stable/install/post-installation.html#security-related

            """.format(
                script_sh
            )
        )
