# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

import os

import llnl.util.tty as tty

import spack.tengine
from spack.package import *


class GaussianView(Package):
    """GaussView 6 is the latest iteration of a graphical interface used with
    Gaussian. It aids in the creation of Gaussian input files, enables the
    user to run Gaussian calculations from a graphical interface without the
    need for using a command line instruction, and helps in the interpretation
    of Gaussian output.

    Needs post-install steps to make it run!
    See package installation logs for details."""

    homepage = "https://gaussian.com/gaussview6/"
    manual_download = True

    maintainers("antoniokaust", "dev-zero")

    version(
        "6.1.6",
        sha256="c9824fd0372c27425b53de350f3a83b27de75ca694219b3ef18cd7d92937db6c",
        extension="tbz",
    )

    version(
        "6.0.16",
        sha256="5dd6a8df8c81763e43a308b3a18d2d3b825d3597e9628dcf43e563d1867b9638",
        extension="tbz",
    )

    depends_on("gaussian@16-B.01", type="run", when="@:6.0")

    depends_on("libx11", type=("run", "link"))
    depends_on("libxext", type=("run", "link"))
    depends_on("gl@3:", type=("run", "link"))
    depends_on("glu@1.3", type=("run", "link"))
    depends_on("libxrender", type=("run", "link"))
    depends_on("libsm", type=("run", "link"))
    depends_on("libice", type=("run", "link"))
    depends_on("patchelf", type="build")

    def url_for_version(self, version):
        return "file://{0}/gv{1}-linux-x86_64.tbz".format(os.getcwd(), version.up_to(2).joined)

    def install(self, spec, prefix):
        install_tree(".", prefix)

        # make sure the executable finds and uses the Spack-provided
        # libraries, otherwise the executable may or may not run depending
        # on what is installed on the host
        # the $ORIGIN prefix is required for the executable to find its
        # own bundled shared libraries
        patchelf = which("patchelf")
        rpath = "$ORIGIN:$ORIGIN/lib" + ":".join(
            self.spec[dep].libs.directories[0]
            for dep in ["libx11", "libxext", "libxrender", "libice", "libsm", "gl", "glu"]
        )
        patchelf("--set-rpath", rpath, join_path(self.prefix, "gview.exe"))

    @run_after("install")
    def caveats(self):
        perm_script = "spack_perms_fix.sh"
        perm_script_path = join_path(self.spec.prefix.bin, perm_script)
        with open(perm_script_path, "w") as f:
            env = spack.tengine.make_environment(dirs=self.package_dir)
            t = env.get_template(perm_script + ".j2")
            f.write(t.render({"prefix": self.spec.prefix}))
        chmod = which("chmod")
        chmod("0555", perm_script_path)

        tty.warn(
            """
For a working GaussianView installation, all executable files can only be accessible by
the owner and the group but not the world.

We've installed a script that will make the necessary changes;
read through it and then execute it:

    {0}

If you have to give others access, please customize the group membership of the package
files as documented here:

    https://spack.readthedocs.io/en/latest/packages_yaml.html#package-permissions""".format(
                perm_script_path
            )
        )

    @when("@:6.0")
    def setup_run_environment(self, env):
        env.set("GV_DIR", self.prefix)

        env.set("GV_LIB_PATH", self.prefix.lib)
        env.set("ALLOWINDIRECT", "1")
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("GV_LIB_PATH", self.prefix.lib.MesaGL)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib.MesaGL)
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)

    @when("@6.1:")
    def setup_run_environment(self, env):
        env.set("GV_DIR", self.prefix)

        # the wrappers in gv/exec setup everything just nicely
        env.prepend_path("PATH", join_path(self.prefix, "exec"))
