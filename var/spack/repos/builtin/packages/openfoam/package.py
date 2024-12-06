# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Mark Olesen <mark.olesen@esi-group.com>
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
#
# Notes
# - mpi handling: WM_MPLIB=USERMPI and use spack to generate mplibUSERMPI
#   wmake rules.
#
# - Resolution of flex, zlib needs more attention (within OpenFOAM)
# - +paraview:
#   depends_on should just be 'paraview+plugins' but that resolves poorly.
#   Workaround: use preferred variants "+plugins +qt"
#       packages:
#           paraview:
#               variants: +plugins +qt
#   in ~/.spack/packages.yaml
#
# Known issues
# - Combining +zoltan with +int64 has not been tested, but probably won't work.
# - Combining +mgridgen with +int64 or +float32 probably won't work.
#
# The spack 'develop' version of openfoam retains the upstream
# WM_PROJECT_VERSION=com naming internally.
#
##############################################################################
import glob
import os
import re

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.builtin.boost import Boost
from spack.util.environment import EnvironmentModifications

# Not the nice way of doing things, but is a start for refactoring
__all__ = [
    "add_extra_files",
    "write_environ",
    "rewrite_environ_files",
    "mplib_content",
    "foam_add_path",
    "foam_add_lib",
    "OpenfoamArch",
]


def add_extra_files(foam_pkg, common, local, **kwargs):
    """Copy additional common and local files into the stage.source_path
    from the openfoam/common and the package/assets directories,
    respectively
    """
    outdir = foam_pkg.stage.source_path

    indir = join_path(os.path.dirname(__file__), "common")
    for f in common:
        tty.info("Added file {0}".format(f))
        install(join_path(indir, f), join_path(outdir, f))

    indir = join_path(foam_pkg.package_dir, "assets")
    for f in local:
        tty.info("Added file {0}".format(f))
        install(join_path(indir, f), join_path(outdir, f))


def format_export(key, value):
    """Format key,value pair as 'export' with newline for POSIX shell.
    A leading '#' for key adds a comment character to the entire line.
    A value of 'None' corresponds to 'unset'.
    """
    if key.startswith("#"):
        return "## export {0}={1}\n".format(re.sub(r"^#+\s*", "", key), value)
    elif value is None:
        return "unset {0}\n".format(key)
    else:
        return "export {0}={1}\n".format(key, value)


def format_setenv(key, value):
    """Format key,value pair as 'setenv' with newline for C-shell.
    A leading '#' for key adds a comment character to the entire line.
    A value of 'None' corresponds to 'unsetenv'.
    """
    if key.startswith("#"):
        return "## setenv {0} {1}\n".format(re.sub(r"^#+\s*", "", key), value)
    elif value is None:
        return "unsetenv {0}\n".format(key)
    else:
        return "setenv {0} {1}\n".format(key, value)


def _write_environ_entries(outfile, environ, formatter):
    """Write environment settings as 'export' or 'setenv'.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.
    Also descends into sub-dict and sub-list, but drops the key.
    """
    if isinstance(environ, dict):
        for key in sorted(environ):
            entry = environ[key]
            if isinstance(entry, dict):
                _write_environ_entries(outfile, entry, formatter)
            elif isinstance(entry, list):
                _write_environ_entries(outfile, entry, formatter)
            else:
                outfile.write(formatter(key, entry))
    elif isinstance(environ, list):
        for item in environ:
            outfile.write(formatter(item[0], item[1]))


def _write_environ_file(output, environ, formatter):
    """Write environment settings as 'export' or 'setenv'.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.
    Also descends into sub-dict and sub-list, but drops the key.
    """
    with open(output, "w") as outfile:
        outfile.write("# spack generated\n")
        _write_environ_entries(outfile, environ, formatter)
        outfile.write("# spack\n")


def write_environ(environ, **kwargs):
    """Write environment settings as 'export' or 'setenv'.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.

       Keyword Options:
         posix[=None]    If set, the name of the POSIX file to rewrite.
         cshell[=None]   If set, the name of the C-shell file to rewrite.
    """
    rcfile = kwargs.get("posix", None)
    if rcfile:
        _write_environ_file(rcfile, environ, format_export)
    rcfile = kwargs.get("cshell", None)
    if rcfile:
        _write_environ_file(rcfile, environ, format_setenv)


def rewrite_environ_files(environ, **kwargs):
    """Use filter_file to rewrite (existing) POSIX shell or C-shell files.
    Keyword Options:
      posix[=None]    If set, the name of the POSIX file to rewrite.
      cshell[=None]   If set, the name of the C-shell file to rewrite.
    """
    rcfile = kwargs.get("posix", None)
    if rcfile and os.path.isfile(rcfile):
        for k, v in environ.items():
            regex = r"^(\s*export\s+{0})=.*$".format(k)
            if not v:
                replace = r"unset {0}  #SPACK: unset".format(k)
            elif v.startswith("#"):
                replace = r"unset {0}  {1}".format(k, v)
            else:
                replace = r"\1={0}".format(v)
            filter_file(regex, replace, rcfile, backup=False)

    rcfile = kwargs.get("cshell", None)
    if rcfile and os.path.isfile(rcfile):
        for k, v in environ.items():
            regex = r"^(\s*setenv\s+{0})\s+.*$".format(k)
            if not v:
                replace = r"unsetenv {0}  #SPACK: unset".format(k)
            elif v.startswith("#"):
                replace = r"unsetenv {0}  {1}".format(k, v)
            else:
                replace = r"\1 {0}".format(v)
            filter_file(regex, replace, rcfile, backup=False)


def foam_add_path(*args):
    """A string with args prepended to 'PATH'"""
    return '"' + ":".join(args) + ':${PATH}"'


def foam_add_lib(*args):
    """A string with args prepended to 'LD_LIBRARY_PATH'"""
    return '"' + ":".join(args) + ':${LD_LIBRARY_PATH}"'


def pkglib(package, pre=None):
    """Get lib64 or lib from package prefix.

    Optional parameter 'pre' to provide alternative prefix
    """
    libdir = package.prefix.lib64
    if not os.path.isdir(libdir):
        libdir = package.prefix.lib
    if pre:
        return join_path(pre, os.path.basename(libdir))
    else:
        return libdir


def mplib_content(spec, pre=None):
    """The mpi settings (from spack) for the OpenFOAM wmake includes, which
    allows later reuse within OpenFOAM.

    Optional parameter 'pre' to provide alternative prefix for
    bin and lib directories.
    """
    mpi_spec = spec["mpi"]
    bin = mpi_spec.prefix.bin
    inc = mpi_spec.headers.directories[0]  # Currently only need first one
    lib = pkglib(mpi_spec)

    libname = "mpi"
    if "mpich" in mpi_spec.name:
        libname = "mpich"

    if pre:
        bin = join_path(pre, os.path.basename(bin))
        inc = join_path(pre, os.path.basename(inc))
        lib = join_path(pre, os.path.basename(lib))
    else:
        pre = mpi_spec.prefix

    info = {
        "name": "{0}-{1}".format(mpi_spec.name, mpi_spec.version),
        "prefix": pre,
        "include": inc,
        "bindir": bin,
        "libdir": lib,
        "FLAGS": "-DOMPI_SKIP_MPICXX -DMPICH_SKIP_MPICXX",
        "PINC": "-I{0}".format(inc),
        "PLIBS": "-L{0} -l{1}".format(lib, libname),
    }
    return info


# -----------------------------------------------------------------------------


class Openfoam(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    This offering is supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    maintainers("olesenm")
    homepage = "https://www.openfoam.com/"
    url = "https://sourceforge.net/projects/openfoam/files/v1906/OpenFOAM-v1906.tgz"
    git = "https://develop.openfoam.com/Development/openfoam.git"
    list_url = "https://sourceforge.net/projects/openfoam/files/"
    list_depth = 2

    license("GPL-3.0-or-later")

    version("develop", branch="develop", submodules="True")
    version("master", branch="master", submodules="True")
    version("2312", sha256="f113183a4d027c93939212af8967053c5f8fe76fb62e5848cb11bbcf8e829552")
    version("2306", sha256="d7fba773658c0f06ad17f90199565f32e9bf502b7bb03077503642064e1f5344")
    version(
        "2212_230612", sha256="604cd731173ec2a3645c838cf2468fae050a35c6340e2ca7c157699899d904c0"
    )
    version("2212", sha256="0a3ddbfea9abca04c3a811e72fcbb184c6b1f92c295461e63b231f1a97e96476")
    version("2206", sha256="db95eda4afb97ca870733b2d4201ef539099d0778e3f3eca9a075d4f1a0eea46")
    version(
        "2112_220610", sha256="e07fd7220520e4bcfd6c8100a7e027fba13eeca2b11085c9dd4642758422a63d"
    )
    version("2112", sha256="3e838731e79db1c288acc27aad8cc8a43d9dac1f24e5773e3b9fa91419a8c3f7")
    version(
        "2106_220610", sha256="5081a1493f4a316c165abf273c69bc2d1e07cf184e8b17ff97f845f876673231"
    )
    version(
        "2106_211215", sha256="08c0d0b90b43505693ff8838e827f09e14ec9fb475956ef53cc2206c736277b1"
    )
    version("2106", sha256="11e41e5b9a253ef592a8f6b79f6aded623b28308192d02cec1327078523b5a37")
    version(
        "2012_220610", sha256="abbe46b0e93f0653397429f1fa2867d4459e0f6c28d90a08da0d4272f89d0757"
    )
    version(
        "2012_210414", sha256="5260aaa79f91aad58a3a305c1a12d0d48b10f12e37cd99a6fa561969b15ea09d"
    )
    version("2012", sha256="3d6e39e39e7ae61d321fbc6db6c3748e6e5e1c4886454207a7f1a7321469e65a")
    version(
        "2006_220610", sha256="b8e9801c304f3fdf512ed8840093bf3f348fb8701121c88f3febd45e3826cb22"
    )
    version(
        "2006_201012", sha256="9afb7eee072bfddcf7f3e58420c93463027db2394997ac4c3b87a8b07c707fb0"
    )
    version("2006", sha256="30c6376d6f403985fc2ab381d364522d1420dd58a42cb270d2ad86f8af227edc")
    version(
        "1912_220610", sha256="a0be015bd651b8eaa9c0fca0ffa97708821979fde9e2e23a1d98d9064c5c3f02"
    )
    version(
        "1912_200506", sha256="831a39ff56e268e88374d0a3922479fd80260683e141e51980242cc281484121"
    )
    version(
        "1912_200403", sha256="1de8f4ddd39722b75f6b01ace9f1ba727b53dd999d1cd2b344a8c677ac2db4c0"
    )
    version("1912", sha256="437feadf075419290aa8bf461673b723a60dc39525b23322850fb58cb48548f2")
    version(
        "1906_200312", sha256="f75645151ed5d8c5da592d307480979fe580a25627cc0c9718ef370211577594"
    )
    version(
        "1906_191103", sha256="631a7fcd926ccbcdef0ab737a9dc55e58d6bedae2f3acaa041ea679db6c9303b"
    )
    version("1906", sha256="bee03c4b1da0d2c9f98eb469eeffbce3a8614728ef8e87f664042a7490976537")
    version(
        "1812_200312", sha256="925d2877c12740fab177a30fdcaa8899c262c15b90225f9c29d18a2d97532de0"
    )
    version(
        "1812_191001", sha256="857a3d476696679313ea9a3f022b33446ddef2bcd417049a9486d504c12038dd"
    )
    version(
        "1812_190531", sha256="51f0ef49a199edf3cd94e2ccfc7330e54e93c8e4ddb29ee66fe3e6b443583b34"
    )
    version("1812", sha256="d4d23d913419c6a364b1fe91509c1fadb5661bdf2eedb8fe9a8a005924eb2032")
    version("1806", sha256="6951aab6405294fe59cec90b0a4e425f5403043191cda02ebaaa890ce1fcc819")
    version("1712", sha256="4d22caa25d638d4c59bb93ee4dec51e8f71724f9f507eeb4162f771ebe885d21")
    version("1706", sha256="7779048bb53798d9a5bd2b2be0bf302c5fd3dff98e29249d6e0ef7eeb83db79a")
    version("1612", sha256="2909c43506a68e1f23efd0ca6186a6948ae0fc8fe1e39c78cc23ef0d69f3569d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("int64", default=False, description="With 64-bit labels")
    variant("knl", default=False, description="Use KNL compiler settings")
    variant("kahip", default=False, description="With kahip decomposition")
    variant("metis", default=False, description="With metis decomposition")
    variant("scotch", default=True, description="With scotch/ptscotch decomposition")
    variant("zoltan", default=False, description="With zoltan renumbering")
    variant("mgridgen", default=False, description="With mgridgen support")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")
    variant(
        "source", default=True, description="Install library/application sources and tutorials"
    )
    variant(
        "precision",
        default="dp",
        description="Precision option",
        values=("sp", "dp", conditional("spdp", when="@1906:")),
        multi=False,
    )

    depends_on("mpi")

    # After 1712, could suggest openmpi+thread_multiple for collated output
    # but particular mixes of mpi versions and InfiniBand may not work so well
    # conflicts('^openmpi~thread_multiple', when='@1712:')

    depends_on("zlib-api")
    depends_on("fftw-api")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # Earlier versions of OpenFOAM may not work with CGAL 5.6. I do
    # not know which OpenFOAM added support for 5.x and conservatively
    # use 2312 in the check.
    depends_on("cgal", when="@2312:")
    depends_on("cgal@:4", when="@:2306")

    # The flex restriction is ONLY to deal with a spec resolution clash
    # introduced by the restriction within scotch!
    depends_on("flex@:2.6.1,2.6.4:")
    depends_on("cmake", type="build")
    depends_on("m4", type="build")

    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    depends_on("scotch~metis+mpi~int64", when="+scotch~int64")
    depends_on("scotch~metis+mpi+int64", when="+scotch+int64")
    depends_on("kahip", when="+kahip")
    depends_on("metis@5:", when="+metis")
    depends_on("metis+int64", when="+metis+int64")
    # mgridgen is statically linked
    depends_on("parmgridgen", when="+mgridgen", type="build")
    depends_on("zoltan", when="+zoltan")
    depends_on("vtk", when="+vtk")
    depends_on("adios2~fortran", when="@1912:")

    # For OpenFOAM plugins and run-time post-processing this should just be
    # 'paraview+plugins' but that resolves poorly.
    # Workaround: use preferred variants "+plugins +qt" in
    #   ~/.spack/packages.yaml

    # 1706 ok with newer paraview but avoid pv-5.2, pv-5.3 readers
    depends_on("paraview@5.4:", when="@1706:+paraview")
    # 1612 plugins need older paraview
    depends_on("paraview@:5.0.1", when="@1612+paraview")

    # Icx only support from v2106 onwards
    conflicts("%oneapi", when="@:2012", msg="OneAPI compiler not supported. Try v2106 or greater.")

    # General patches
    common = ["spack-Allwmake", "README-spack"]
    assets = []  # type: List[str]

    # Version-specific patches
    patch("1612-spack-patches.patch", when="@1612")
    # kahip patch (wmake)
    patch(
        "https://develop.openfoam.com/Development/openfoam/commit/8831dfc58b0295d0d301a78341dd6f4599073d45.patch",
        when="@1806",
        sha256="531146be868dd0cda70c1cf12a22110a38a30fd93b5ada6234be3d6c9256c6cf",
    )
    # Fix: missing std::array include (searchable sphere)
    patch(
        "https://develop.openfoam.com/Development/openfoam/commit/b4324b1297761545d5b10f50b60ab29e71c172aa.patch",
        when="@2012_220610",
        sha256="bad4b0e80fd26ea702bce9ccfb925edbbaa3308f70392fe6da2c7671b1d39bea",
    )

    # Some user config settings
    # default: 'compile-option': '-spack',
    # default: 'mplib': 'USERMPI',  # User-defined mpi for spack
    config = {
        # Add links into bin/, lib/ (eg, for other applications)
        "link": False
    }

    # The openfoam architecture, compiler information etc
    _foam_arch = None

    # Content for etc/prefs.{csh,sh}
    etc_prefs = {}  # type: Dict[str,str]

    # Content for etc/config.{csh,sh}/ files
    etc_config = {}  # type: Dict[str,str]

    phases = ["configure", "build", "install"]
    build_script = "./spack-Allwmake"  # From patch() method.

    #
    # - End of definitions / setup -
    #

    def url_for_version(self, version):
        """Handles locations for patched and unpatched versions.
        Patched version (eg '1906_191103') are located in the
        corresponding unpatched directories (eg '1906').
        Older versions (eg, v1612+) had additional '+' in naming
        """
        if version <= Version("1612"):
            fmt = "v{0}+/OpenFOAM-v{1}+.tgz"
        else:
            fmt = "v{0}/OpenFOAM-v{1}.tgz"
        return self.list_url + fmt.format(version.up_to(1), version)

    def setup_minimal_environment(self, env):
        """Sets a minimal openfoam environment."""
        tty.info("OpenFOAM minimal env {0}".format(self.prefix))
        env.set("FOAM_PROJECT_DIR", self.projectdir)
        env.set("WM_PROJECT_DIR", self.projectdir)
        for d in ["wmake", self.archbin]:  # bin added automatically
            env.prepend_path("PATH", join_path(self.projectdir, d))

    def setup_build_environment(self, env):
        """Sets the build environment (prior to unpacking the sources)."""
        pass

    def setup_run_environment(self, env):
        """Sets the run environment (post-installation).
        The environment comes from running:

        .. code-block:: console

           $ . $WM_PROJECT_DIR/etc/bashrc
        """

        bashrc = join_path(self.projectdir, "etc", "bashrc")
        minimal = True
        if os.path.isfile(bashrc):
            # post-install: source the installed bashrc
            try:
                mods = EnvironmentModifications.from_sourcing_file(
                    bashrc,
                    clean=True,  # Remove duplicate entries
                    blacklist=[  # Blacklist these
                        # Inadvertent changes
                        # -------------------
                        "PS1",  # Leave untouched
                        "MANPATH",  # Leave untouched
                        # Unneeded bits
                        # -------------
                        # 'FOAM_SETTINGS',  # Do not use with modules
                        # 'FOAM_INST_DIR',  # Old
                        # 'FOAM_(APP|ETC|SRC|SOLVERS|UTILITIES)',
                        # 'FOAM_TUTORIALS', # May be useful
                        # 'WM_OSTYPE',      # Purely optional value
                        # Third-party cruft - only used for orig compilation
                        # -----------------
                        "[A-Z].*_ARCH_PATH",
                        # '(KAHIP|METIS|SCOTCH)_VERSION',
                        # User-specific
                        # -------------
                        "FOAM_RUN",
                        "(FOAM|WM)_.*USER_.*",
                    ],
                    whitelist=[  # Whitelist these
                        "MPI_ARCH_PATH"  # Can be required for compilation
                    ],
                )

                env.extend(mods)
                minimal = False
                tty.debug("OpenFOAM bashrc env: {0}".format(bashrc))
            except Exception:
                minimal = True

        if minimal:
            # pre-build or minimal environment
            self.setup_minimal_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Use full OpenFOAM environment when building.
        Mirror WM_PROJECT_DIR value as FOAM_PROJECT_DIR to avoid
        masking the normal OpenFOAM cleanup of previous versions.
        """
        self.setup_run_environment(env)
        env.set("FOAM_PROJECT_DIR", self.projectdir)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Use full OpenFOAM environment when running.
        Mirror WM_PROJECT_DIR value as FOAM_PROJECT_DIR to avoid
        masking the normal OpenFOAM cleanup of previous versions.
        """
        self.setup_run_environment(env)
        env.set("FOAM_PROJECT_DIR", self.projectdir)

    @property
    def projectdir(self):
        """Absolute location of project directory: WM_PROJECT_DIR/"""
        return self.prefix  # <- install directly under prefix

    @property
    def foam_arch(self):
        if not self._foam_arch:
            self._foam_arch = OpenfoamArch(self.spec, **self.config)
        return self._foam_arch

    @property
    def archbin(self):
        """Relative location of architecture-specific executables"""
        return join_path("platforms", self.foam_arch, "bin")

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        return join_path("platforms", self.foam_arch, "lib")

    def patch(self):
        """Adjust OpenFOAM build for spack.
        Where needed, apply filter as an alternative to normal patching."""
        add_extra_files(self, self.common, self.assets)

    @when("@:1806")
    def patch(self):
        """Adjust OpenFOAM build for spack.
        Where needed, apply filter as an alternative to normal patching."""
        add_extra_files(self, self.common, self.assets)

        # Prior to 1812, required OpenFOAM-v{VER} directory when sourcing
        projdir = "OpenFOAM-v{0}".format(self.version)
        if not os.path.exists(join_path(self.stage.path, projdir)):
            tty.info("Added directory link {0}".format(projdir))
            os.symlink(
                os.path.relpath(self.stage.source_path, self.stage.path),
                join_path(self.stage.path, projdir),
            )

        # Avoid WM_PROJECT_INST_DIR for ThirdParty
        # This modification is non-critical
        edits = {
            "WM_THIRD_PARTY_DIR": r"$WM_PROJECT_DIR/ThirdParty  #SPACK: No separate third-party"
        }
        rewrite_environ_files(  # etc/{bashrc,cshrc}
            edits, posix=join_path("etc", "bashrc"), cshell=join_path("etc", "cshrc")
        )

        # The following filtering is non-critical.
        # It simply prevents 'site' dirs at the wrong level
        # (likely non-existent anyhow) from being added to
        # PATH, LD_LIBRARY_PATH.
        for rcdir in ["config.sh", "config.csh"]:
            rcfile = join_path("etc", rcdir, "settings")
            if os.path.isfile(rcfile):
                filter_file("WM_PROJECT_INST_DIR/", "WM_PROJECT_DIR/", rcfile, backup=False)

    def configure_trapFpe_off(self):
        """Disable trapFpe handling.
        Seems to be needed for several clang-derivatives.
        """
        # Set 'trapFpe 0' in etc/controlDict
        controlDict = "etc/controlDict"
        if os.path.exists(controlDict):
            filter_file(r"trapFpe\s+\d+\s*;", "trapFpe 0;", controlDict, backup=False)

    @when("@:2106 %aocc@3.2.0:")
    @run_before("configure")
    def make_amd_rules(self):
        """Due to the change in the linker behavior in AOCC v3.2, it is now
        issuing diagnostic messages for the unreferenced symbols in the
        shared objects as it may lead to run time failures.
        """
        general_rules = "wmake/rules/General"
        src = join_path(general_rules, "Clang")
        filter_file(
            "clang++", spack_cxx + " -pthread", join_path(src, "c++"), backup=False, string=True
        )

    @when("@1812: %fj")
    @run_before("configure")
    def make_fujitsu_rules(self):
        """Create Fujitsu rules (clang variant) unless supplied upstream.
        Implemented for 1812 and later (older rules are too messy to edit).
        Already included after 1912.
        """
        general_rules = "wmake/rules/General"
        arch_rules = "wmake/rules/linuxARM64"  # self.arch
        src = arch_rules + "Clang"
        dst = arch_rules + "Fujitsu"  # self.compiler
        self.configure_trapFpe_off()  # LLVM may falsely trigger FPE

        if os.path.exists(dst):
            return

        # Handle rules/<ARCH><COMP> or rules/<ARCH>/<COMP>
        if not os.path.exists(src):
            src = join_path(arch_rules, "Clang")
            dst = join_path(arch_rules, "Fujitsu")  # self.compiler
            if os.path.exists(dst):
                return

        tty.info("Add Fujitsu wmake rules")
        copy_tree(src, dst)

        if self.spec.version >= Version("1906"):
            for cfg in ["c", "c++", "general"]:
                rule = join_path(dst, cfg)
                filter_file("Clang", "Fujitsu", rule, backup=False)
        else:
            filter_file("clang", spack_cc, join_path(dst, "c"), backup=False, string=True)
            filter_file("clang++", spack_cxx, join_path(dst, "c++"), backup=False, string=True)

        src = join_path(general_rules, "Clang")
        dst = join_path(general_rules, "Fujitsu")  # self.compiler
        copy_tree(src, dst)
        if self.spec.version >= Version("1906"):
            filter_file("clang", spack_cc, join_path(dst, "c"), backup=False, string=True)
        filter_file("clang++", spack_cxx, join_path(dst, "c++"), backup=False, string=True)

    def configure(self, spec, prefix):
        """Make adjustments to the OpenFOAM configuration files in their
        various locations: etc/bashrc, etc/config.sh/FEATURE and
        customizations that don't properly fit get placed in the etc/prefs.sh
        file (similiarly for csh).
        """
        # Filtering bashrc, cshrc
        edits = {}
        edits.update(self.foam_arch.foam_dict())
        rewrite_environ_files(  # etc/{bashrc,cshrc}
            edits, posix=join_path("etc", "bashrc"), cshell=join_path("etc", "cshrc")
        )

        # Content for etc/prefs.{csh,sh}
        self.etc_prefs = {
            # TODO
            # 'CMAKE_ARCH_PATH': spec['cmake'].prefix,
            # 'FLEX_ARCH_PATH':  spec['flex'].prefix,
            # 'ZLIB_ARCH_PATH':  spec['zlib'].prefix,
        }

        # MPI content, using MPI_ARCH_PATH
        user_mpi = mplib_content(spec, "${MPI_ARCH_PATH}")

        # Content for etc/config.{csh,sh}/ files
        self.etc_config = {
            "CGAL": [
                ("BOOST_ARCH_PATH", spec["boost"].prefix),
                ("CGAL_ARCH_PATH", spec["cgal"].prefix),
                ("MPFR_ARCH_PATH", spec["mpfr"].prefix),
                (
                    "LD_LIBRARY_PATH",
                    foam_add_lib(
                        pkglib(spec["boost"], "${BOOST_ARCH_PATH}"),
                        pkglib(spec["cgal"], "${CGAL_ARCH_PATH}"),
                        pkglib(spec["mpfr"], "${MPFR_ARCH_PATH}"),
                    ),
                ),
            ],
            "FFTW": [
                ("FFTW_ARCH_PATH", spec["fftw-api"].prefix),  # Absolute
                ("LD_LIBRARY_PATH", foam_add_lib(pkglib(spec["fftw-api"], "${BOOST_ARCH_PATH}"))),
            ],
            # User-defined MPI
            "mpi-user": [
                ("MPI_ARCH_PATH", spec["mpi"].prefix),  # Absolute
                ("LD_LIBRARY_PATH", foam_add_lib(user_mpi["libdir"])),
                ("PATH", foam_add_path(user_mpi["bindir"])),
            ],
            "adios2": {},
            "scotch": {},
            "kahip": {},
            "metis": {},
            "ensight": {},  # Disable settings
            "paraview": [],
            "gperftools": [],  # Disable settings
            "vtk": [],
        }

        # With adios2 after 1912
        if spec.satisfies("@1912:"):
            self.etc_config["adios2"] = [
                ("ADIOS2_ARCH_PATH", spec["adios2"].prefix),
                ("LD_LIBRARY_PATH", foam_add_lib(pkglib(spec["adios2"], "${ADIOS2_ARCH_PATH}"))),
                ("PATH", foam_add_path("${ADIOS2_ARCH_PATH}/bin")),
            ]

        if "+scotch" in spec:
            self.etc_config["scotch"] = {
                "SCOTCH_ARCH_PATH": spec["scotch"].prefix,
                # For src/parallel/decompose/Allwmake
                "SCOTCH_VERSION": "scotch-{0}".format(spec["scotch"].version),
            }

        if "+kahip" in spec:
            self.etc_config["kahip"] = {"KAHIP_ARCH_PATH": spec["kahip"].prefix}

        if "+metis" in spec:
            self.etc_config["metis"] = {"METIS_ARCH_PATH": spec["metis"].prefix}

        # ParaView_INCLUDE_DIR is not used in 1812, but has no ill-effect
        if "+paraview" in spec:
            pvmajor = "paraview-{0}".format(spec["paraview"].version.up_to(2))
            self.etc_config["paraview"] = [
                ("ParaView_DIR", spec["paraview"].prefix),
                ("ParaView_INCLUDE_DIR", "${ParaView_DIR}/include/" + pvmajor),
                ("PV_PLUGIN_PATH", "$FOAM_LIBBIN/" + pvmajor),
                ("PATH", foam_add_path("${ParaView_DIR}/bin")),
            ]

        if "+vtk" in spec:
            self.etc_config["vtk"] = [
                ("VTK_DIR", spec["vtk"].prefix),
                ("LD_LIBRARY_PATH", foam_add_lib(pkglib(spec["vtk"], "${VTK_DIR}"))),
            ]

        # Optional
        if "+mgridgen" in spec:
            self.etc_config["mgridgen"] = {"MGRIDGEN_ARCH_PATH": spec["parmgridgen"].prefix}

        # Optional
        if "+zoltan" in spec:
            self.etc_config["zoltan"] = {"ZOLTAN_ARCH_PATH": spec["zoltan"].prefix}

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        if self.etc_prefs:
            write_environ(
                self.etc_prefs,
                posix=join_path("etc", "prefs.sh"),
                cshell=join_path("etc", "prefs.csh"),
            )

        # Adjust components to use SPACK variants
        for component, subdict in self.etc_config.items():
            write_environ(
                subdict,
                posix=join_path("etc", "config.sh", component),
                cshell=join_path("etc", "config.csh", component),
            )

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        Only build if the compiler is known to be supported.
        """
        self.foam_arch.has_rule(self.stage.source_path)
        self.foam_arch.create_rules(self.stage.source_path, self)

        args = ["-silent"]
        if self.parallel:  # Build in parallel? - pass as an argument
            args.append("-j{0}".format(make_jobs))
        builder = Executable(self.build_script)
        builder(*args)

    def install_write_location(self):
        """Set the installation location (projectdir) in bashrc,cshrc."""
        mkdirp(self.projectdir)

        # Filtering: bashrc, cshrc
        edits = {"WM_PROJECT_DIR": self.projectdir}
        etc_dir = join_path(self.projectdir, "etc")
        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            edits, posix=join_path(etc_dir, "bashrc"), cshell=join_path(etc_dir, "cshrc")
        )

    @when("@:1806")
    def install_write_location(self):
        """Set the installation location (projectdir) in bashrc,cshrc.
        In 1806 and earlier, had WM_PROJECT_INST_DIR as the prefix
        directory where WM_PROJECT_DIR was installed.
        """
        mkdirp(self.projectdir)
        projdir = os.path.basename(self.projectdir)

        # Filtering: bashrc, cshrc
        edits = {
            "WM_PROJECT_INST_DIR": os.path.dirname(self.projectdir),
            "WM_PROJECT_DIR": join_path("$WM_PROJECT_INST_DIR", projdir),
        }
        etc_dir = join_path(self.projectdir, "etc")
        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            edits, posix=join_path(etc_dir, "bashrc"), cshell=join_path(etc_dir, "cshrc")
        )

    def install(self, spec, prefix):
        """Install under the projectdir"""
        mkdirp(self.projectdir)

        # All top-level files, except spack build info and possibly Allwmake
        if "+source" in spec:
            ignored = re.compile(r"^spack-.*")
        else:
            ignored = re.compile(r"^(Allwmake|spack-).*")

        files = [f for f in glob.glob("*") if os.path.isfile(f) and not ignored.search(f)]
        for f in files:
            install(f, self.projectdir)

        # Having wmake and ~source is actually somewhat pointless...
        # Install 'etc' before 'bin' (for symlinks)
        # META-INFO for 1812 and later (or backported)
        dirs = ["META-INFO", "etc", "bin", "wmake"]
        if "+source" in spec:
            dirs.extend(["applications", "src", "tutorials"])

        for d in dirs:
            if os.path.isdir(d):
                install_tree(d, join_path(self.projectdir, d), symlinks=True)

        dirs = ["platforms"]
        if "+source" in spec:
            dirs.extend(["doc"])

        # Install platforms (and doc) skipping intermediate targets
        relative_ignore_paths = ["src", "applications", "html", "Guides"]
        ignore = lambda p: p in relative_ignore_paths
        for d in dirs:
            install_tree(d, join_path(self.projectdir, d), ignore=ignore, symlinks=True)

        self.install_write_location()
        self.install_links()

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        # Make build log visible - it contains OpenFOAM-specific information
        with working_dir(self.projectdir):
            os.symlink(
                join_path(os.path.relpath(self.install_log_path)),
                join_path("log." + str(self.foam_arch)),
            )

        if not self.config["link"]:
            return

        # ln -s platforms/linux64GccXXX/lib lib
        with working_dir(self.projectdir):
            if os.path.isdir(self.archlib):
                os.symlink(self.archlib, "lib")

        # (cd bin && ln -s ../platforms/linux64GccXXX/bin/* .)
        with working_dir(join_path(self.projectdir, "bin")):
            for f in [
                f for f in glob.glob(join_path("..", self.archbin, "*")) if os.path.isfile(f)
            ]:
                os.symlink(f, os.path.basename(f))


# -----------------------------------------------------------------------------


class OpenfoamArch:
    """OpenfoamArch represents architecture/compiler settings for OpenFOAM.
    The string representation is WM_OPTIONS.

    Keywords
        label-size=[True]   supports int32/int64
        compile-option[=-spack]
        mplib[=USERMPI]
    """

    #: Map spack compiler names to OpenFOAM compiler names
    #  By default, simply capitalize the first letter
    compiler_mapping = {"aocc": "Amd", "fj": "Fujitsu", "intel": "Icc", "oneapi": "Icx"}

    def __init__(self, spec, **kwargs):
        # Some user settings, to be adjusted manually or via variants
        self.compiler = None  # <- %compiler
        self.arch_option = ""  # Eg, -march=knl
        self.label_size = None  # <- +int64
        self.precision_option = "DP"  # <- precision= sp | dp | spdp
        self.compile_option = kwargs.get("compile-option", "-spack")
        self.arch = None
        self.options = None
        self.mplib = kwargs.get("mplib", "USERMPI")

        # WM_LABEL_OPTION, but perhaps not yet for foam-extend
        if "+int64" in spec:
            self.label_size = "64"
        elif kwargs.get("label-size", True):
            self.label_size = "32"

        # WM_PRECISION_OPTION
        if "precision=sp" in spec:
            self.precision_option = "SP"
        elif "precision=spdp" in spec:
            self.precision_option = "SPDP"

        # Processor/architecture-specific optimizations
        if "+knl" in spec:
            self.arch_option = "-march=knl"

        # Capitalize first letter of compiler name to obtain the
        # OpenFOAM naming (eg, gcc -> Gcc, clang -> Clang, etc).
        # Use compiler_mapping[] for special cases
        comp = spec.compiler.name
        if comp in self.compiler_mapping:
            comp = self.compiler_mapping[comp]

        self.compiler = comp.capitalize()
        self.update_arch(spec)
        self.update_options()

    def update_arch(self, spec):
        """Set WM_ARCH string corresponding to spack platform/target"""
        # spec.architecture.platform is like `uname -s`, but lower-case
        platform = str(spec.architecture.platform)

        # spec.target.family is like `uname -m`
        target = str(spec.target.family)

        # No spack platform family for ia64 or armv7l
        if platform == "linux":
            if target == "x86_64":
                platform += "64"
            elif target == "ia64":
                platform += "IA64"
            elif target == "armv7l":
                platform += "ARM7"
            elif target == "aarch64":
                # overwritten as 'Arm64' in openfoam-org
                platform += "ARM64"
            elif target == "ppc64":
                platform += "PPC64"
            elif target == "ppc64le":
                platform += "PPC64le"
        elif platform == "darwin":
            platform += "64"  # aarch64 or x86_64
        # ... and others?
        self.arch = platform

    def update_options(self):
        """Set WM_OPTIONS string consistent with current settings"""
        # WM_OPTIONS
        # ----
        # WM_LABEL_OPTION=Int$WM_LABEL_SIZE
        # WM_OPTIONS_BASE=$WM_ARCH$WM_COMPILER$WM_PRECISION_OPTION
        # WM_OPTIONS=$WM_OPTIONS_BASE$WM_LABEL_OPTION$WM_COMPILE_OPTION
        # or
        # WM_OPTIONS=$WM_OPTIONS_BASE$WM_COMPILE_OPTION
        # ----
        self.options = "".join(
            [
                self.arch,
                self.compiler,
                self.precision_option,
                ("Int" + self.label_size if self.label_size else ""),
                self.compile_option,
            ]
        )

    def __str__(self):
        return self.options

    def __repr__(self):
        return str(self)

    def foam_dict(self):
        """Returns a dictionary for OpenFOAM prefs, bashrc, cshrc."""
        return dict(
            [
                ("WM_COMPILER", self.compiler),
                ("WM_LABEL_SIZE", self.label_size),
                ("WM_PRECISION_OPTION", self.precision_option),
                ("WM_COMPILE_OPTION", self.compile_option),
                ("WM_MPLIB", self.mplib),
            ]
        )

    def _rule_directory(self, projdir, general=False, common=False):
        """Return wmake/rules/ General/common, General or
        compiler rules directory.
        Supports wmake/rules/<ARCH><COMP> and wmake/rules/<ARCH>/<COMP>.
        """
        rules_dir = os.path.join(projdir, "wmake", "rules")
        if common:
            return os.path.join(rules_dir, "General", "common")
        if general:
            return os.path.join(rules_dir, "General")

        arch_dir = os.path.join(rules_dir, self.arch)
        comp_rules = arch_dir + self.compiler
        if os.path.isdir(comp_rules):
            return comp_rules
        else:
            return os.path.join(arch_dir, self.compiler)

    def has_rule(self, projdir):
        """Verify that a wmake/rules/ compiler rule exists in the project."""
        # Insist on a wmake rule for this architecture/compiler combination
        rule_dir = self._rule_directory(projdir)

        if not os.path.isdir(rule_dir):
            raise InstallError("No wmake rule for {0} {1}".format(self.arch, self.compiler))
        return True

    def _rule_add_rpath(self, rpath, src, dst):
        """Create {c,c++}-spack rules in the specified project directory.
        The compiler rules are based on the respective {cflags,cxxflags}-Opt or
        {c,c++}Opt rules with additional rpath information for the OpenFOAM libraries.

        The '-spack' rules channel spack information into OpenFOAM wmake
        rules with minimal modification to OpenFOAM.
        The rpath is used for the installed libpath (continue to use
        LD_LIBRARY_PATH for values during the build).
        """
        # Note: the 'c' rules normally don't need rpath, since they are just
        # used for some statically linked wmake tools, but left in anyhow.

        ok = os.path.isfile(src)

        if ok:
            with open(src, "r") as infile:
                with open(dst, "w") as outfile:
                    for line in infile:
                        line = line.rstrip()
                        outfile.write(line)
                        if re.match(r"^\S+DBUG\s*:?=", line):
                            outfile.write(" ")
                            outfile.write(rpath)
                        elif re.match(r"^\S+OPT\s*:?=", line):
                            if self.arch_option:
                                outfile.write(" ")
                                outfile.write(self.arch_option)
                        outfile.write("\n")
        return ok

    def create_rules(self, projdir, foam_pkg):
        """Create {c,c++}-spack and mplib{USERMPI} rules in the
        specified project directory.
        Uses General/common/{c,c++}Opt or arch-specific {c,c++}Opt rules,
        but with additional rpath information for the OpenFOAM libraries.

        The '-spack' rules channel spack information into OpenFOAM wmake
        rules with minimal modification to OpenFOAM.
        The rpath is used for the installed libpath (continue to use
        LD_LIBRARY_PATH for values during the build).
        """
        # Note: the 'c' rules normally don't need rpath, since they are just
        # used for some statically linked wmake tools, but left in anyhow.

        # rpath for installed OpenFOAM libraries
        rpath = "{0}{1}".format(
            foam_pkg.compiler.cxx_rpath_arg, join_path(foam_pkg.projectdir, foam_pkg.archlib)
        )

        user_mpi = mplib_content(foam_pkg.spec)
        rule_dir = self._rule_directory(projdir)
        comm_dir = self._rule_directory(projdir, False, True)

        # Compiler: copy existing {c,c++}Opt or General/common/{c,c++}Opt
        # and modify '*DBUG' value to include rpath

        for lang in ["c", "c++"]:
            gen = join_path(comm_dir, "{0}Opt".format(lang))
            src = join_path(rule_dir, "{0}Opt".format(lang))
            dst = join_path(rule_dir, "{0}{1}".format(lang, self.compile_option))

            if not self._rule_add_rpath(rpath, src, dst):
                self._rule_add_rpath(rpath, gen, dst)

        with working_dir(rule_dir):
            # MPI rules
            for mplib in ["mplibUSERMPI"]:
                with open(mplib, "w") as out:
                    out.write(
                        """# MPI from spack ({name})\n
PFLAGS  = {FLAGS}
PINC    = {PINC}
PLIBS   = {PLIBS}
#-------
""".format(
                            **user_mpi
                        )
                    )


# -----------------------------------------------------------------------------
