# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

import llnl.util.tty as tty

from spack.package import *


class SingularityBase(MakefilePackage):
    variant("suid", default=True, description="install SUID binary")
    variant("network", default=True, description="install network plugins")

    depends_on("pkgconfig", type="build")
    depends_on("conmon", type=("build", "run"))
    depends_on("squashfs", type=("build", "run"))
    depends_on("go@1.16:")
    depends_on("uuid")
    depends_on("libgpg-error")
    depends_on("libseccomp")
    depends_on("squashfs", type="run")
    depends_on("git", when="@develop")  # mconfig uses it for version info
    depends_on("shadow", type="run", when="@3.3:")
    depends_on("cryptsetup", type=("build", "run"), when="@3.4:")
    depends_on("libfuse", type=("build", "run"), when="@4.0:")
    depends_on("autoconf", type="build", when="@4.0:")
    depends_on("automake", type="build", when="@4.0:")
    depends_on("libtool", type="build", when="@4.0:")

    conflicts("platform=darwin", msg="singularity requires a Linux VM on Windows & Mac")

    # Use these properties to buffer the renaming to Apptainer
    singularity_org = "sylabs"
    singularity_name = "singularity"
    singularity_security_urls = (
        "https://sylabs.io/guides/2.6/admin-guide/security.html",
        "https://sylabs.io/guides/3.2/admin-guide/admin_quickstart.html#singularity-security",
    )

    # Go has novel ideas about how projects should be organized.
    # We'll point GOPATH at the stage dir, and move the unpacked src
    # tree into the proper subdir in our overridden do_stage below.
    @property
    def gopath(self):
        return self.stage.path

    @property
    def singularity_gopath_dir(self):
        return join_path(
            self.gopath, "src", "github.com", self.singularity_org, self.singularity_name
        )

    # Unpack the tarball as usual, then move the src dir into
    # its home within GOPATH.
    def do_stage(self, mirror_only=False):
        super().do_stage(mirror_only)
        if not os.path.exists(self.singularity_gopath_dir):
            # Move the expanded source to its destination
            tty.debug(
                "Moving {0} to {1}".format(self.stage.source_path, self.singularity_gopath_dir)
            )
            shutil.move(self.stage.source_path, self.singularity_gopath_dir)

            # The build process still needs access to the source path,
            # so create a symlink.
            force_symlink(self.singularity_gopath_dir, self.stage.source_path)

    # MakefilePackage's stages use this via working_dir()
    @property
    def build_directory(self):
        return self.singularity_gopath_dir

    # Allow overriding config options
    @property
    def config_options(self):
        # Using conmon from spack
        return ["--without-conmon"]

    # Hijack the edit stage to run mconfig.
    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            _config_options = ["--prefix=%s" % prefix]
            _config_options += self.config_options
            if "~suid" in spec:
                _config_options += ["--without-suid"]
            if "~network" in spec:
                _config_options += ["--without-network"]
            configure = Executable("./mconfig")
            configure(*_config_options)

    # Set these for use by MakefilePackage's default build/install methods.
    build_targets = ["-C", "builddir", "parallel=False"]
    install_targets = ["install", "-C", "builddir", "parallel=False"]

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.gopath)

    # `singularity` has a fixed path where it will look for
    # mksquashfs.  If it lives somewhere else you need to specify the
    # full path in the config file.  This bit uses filter_file to edit
    # the config file, uncommenting and setting the mksquashfs path.
    @run_after("install")
    def fix_mksquashfs_path(self):
        prefix = self.spec.prefix
        squash_path = join_path(self.spec["squashfs"].prefix.bin, "mksquashfs")
        filter_file(
            r"^# mksquashfs path =",
            "mksquashfs path = {0}".format(squash_path),
            join_path(prefix.etc, self.singularity_name, self.singularity_name + ".conf"),
        )
        filter_file(
            r"^shared loop devices = no",
            "shared loop devices = yes",
            join_path(prefix.etc, self.singularity_name, self.singularity_name + ".conf"),
        )

    #
    # Assemble a script that fixes the ownership and permissions of several
    # key files, install it, and tty.warn() the user.
    # HEADSUP: https://github.com/spack/spack/pull/10412.
    #
    def perm_script(self):
        return "spack_perms_fix.sh"

    def perm_script_tmpl(self):
        return "{0}.j2".format(self.perm_script())

    def perm_script_path(self):
        return join_path(self.spec.prefix.bin, self.perm_script())

    def _build_script(self, filename, variable_data):
        with open(filename, "w") as f:
            env = spack.tengine.make_environment(dirs=self.package_dir)
            t = env.get_template(self.perm_script_tmpl())
            f.write(t.render(variable_data))

    @run_after("install")
    def build_perms_script(self):
        if self.spec.satisfies("+suid"):
            script = self.perm_script_path()
            chown_files = [
                fn.format(self.singularity_name)
                for fn in [
                    "libexec/{0}/bin/starter-suid",
                    "etc/{0}/{0}.conf",
                    "etc/{0}/capability.json",
                    "etc/{0}/ecl.toml",
                ]
            ]
            setuid_files = ["libexec/{0}/bin/starter-suid".format(self.singularity_name)]
            self._build_script(
                script,
                {
                    "prefix": self.spec.prefix,
                    "chown_files": chown_files,
                    "setuid_files": setuid_files,
                },
            )
            chmod = which("chmod")
            chmod("555", script)

    # Until tty output works better from build steps, this ends up in
    # the build log.  See https://github.com/spack/spack/pull/10412.
    @run_after("install")
    def caveats(self):
        if self.spec.satisfies("+suid"):
            tty.warn(
                """
            For full functionality, you'll need to chown and chmod some files
            after installing the package.  This has security implications.
            For details, see:
            {1}
            {2}

            We've installed a script that will make the necessary changes;
            read through it and then execute it as root (e.g. via sudo).

            The script is named:

            {0}
            """.format(
                    self.perm_script_path(), *self.singularity_security_urls
                )
            )


class Singularityce(SingularityBase):
    """Singularity is a container technology focused on building portable
    encapsulated environments to support "Mobility of Compute" For older
    versions of Singularity (pre 3.0) you should use singularity-legacy,
    which has a different install base (Autotools).

    Needs post-install chmod/chown steps to enable full functionality.
    See package definition or `spack-build-out.txt` build log for details,
    e.g.

    tail -15 $(spack location -i singularityce)/.spack/spack-build-out.txt
    """

    homepage = "https://sylabs.io/singularity/"
    url = "https://github.com/sylabs/singularity/releases/download/v3.9.1/singularity-ce-3.9.1.tar.gz"
    git = "https://github.com/sylabs/singularity.git"

    license("Apache-2.0")

    maintainers("alalazo")
    version("master", branch="master")

    version("4.1.0", sha256="119667f18e76a750b7d4f8612d7878c18a824ee171852795019aa68875244813")
    version("4.0.3", sha256="b3789c9113edcac62032ce67cd1815cab74da6c33c96da20e523ffb54cdcedf3")
    version("3.11.5", sha256="5acfbb4a109d9c63a25c230e263f07c1e83f6c726007fbcd97a533f03d33a86a")
    version("3.11.4", sha256="751dbea64ec16fd7e7af1e36953134c778c404909f9d27ba89006644160b2fde")
    version("3.11.3", sha256="a77ede063fd115f85f98f82d2e30459b5565db7d098665497bcd684bf8edaec9")
    version("3.10.3", sha256="f87d8e212ce209c5212d6faf253b97a24b5d0b6e6b17b5e58b316cdda27a332f")
    version("3.10.2", sha256="b4f279856ea4bf28a1f34f89320c02b545d6e57d4143679920e1ac4267f540e1")
    version("3.10.1", sha256="e3af12edc0260bc3a3a481459a3a4457de9235025e6b37288da80e3cdc011a7a")
    version("3.10.0", sha256="5e22e6cdad66c331668f6cff4544c83917bb3db90da3cf92403a394c5bf8cc8f")
    version("3.9.9", sha256="1381433d64138c08e93ffacdfb4844e82c2288f1e39a9d2c631a1c4021381f2a")
    version("3.9.1", sha256="1ba3bb1719a420f48e9b0a6afdb5011f6c786d0f107ef272528c632fff9fd153")
    version("3.8.0", sha256="5fa2c0e7ef2b814d8aa170826b833f91e5031a85d85cd1292a234e6c55da1be1")

    depends_on("c", type="build")
