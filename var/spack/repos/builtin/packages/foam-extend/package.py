# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
# - mpi handling: WM_MPLIB=USERMPI and generate mplibUSERMPI wmake rules.
#
# Changes
# 2017-03-28 Mark Olesen <mark.olesen@esi-group.com>
#  - avoid installing intermediate targets.
#  - reworked to mirror the openfoam package.
#    If changes are needed here, consider if they need applying there too.
#
# Known issues
# - Combining +parmgridgen with +float32 probably won't work.
#
##############################################################################
import glob
import os
import re

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.builtin.openfoam import (
    OpenfoamArch,
    add_extra_files,
    rewrite_environ_files,
    write_environ,
)
from spack.util.environment import EnvironmentModifications


class FoamExtend(Package):
    """The Extend Project is a fork of the OpenFOAM opensource library
    for Computational Fluid Dynamics (CFD).
    This offering is not approved or endorsed by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    """

    homepage = "https://sourceforge.net/projects/foam-extend/"

    license("GPL-3.0-only")

    version("5.0", git="http://git.code.sf.net/p/foam-extend/foam-extend-5.0.git")
    version("4.1", git="http://git.code.sf.net/p/foam-extend/foam-extend-4.1.git")
    version("4.0", git="http://git.code.sf.net/p/foam-extend/foam-extend-4.0.git")
    version("3.2", git="http://git.code.sf.net/p/foam-extend/foam-extend-3.2.git")
    version("3.1", git="http://git.code.sf.net/p/foam-extend/foam-extend-3.1.git", deprecated=True)
    version("3.0", git="http://git.code.sf.net/p/foam-extend/foam-extend-3.0.git", deprecated=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # variant('int64', default=False,
    #         description='Compile with 64-bit label')
    variant("float32", default=False, description="Compile with 32-bit scalar (single-precision)")
    variant("paraview", default=False, description="Build paraview plugins (eg, paraFoam)")
    variant("scotch", default=True, description="With scotch for decomposition")
    variant("ptscotch", default=True, description="With ptscotch for decomposition")
    variant("metis", default=True, description="With metis for decomposition")
    variant("parmetis", default=True, description="With parmetis for decomposition")
    variant("parmgridgen", default=True, description="With parmgridgen support")
    variant(
        "source", default=True, description="Install library/application sources and tutorials"
    )

    depends_on("mpi")
    depends_on("python")
    depends_on("zlib-api")
    depends_on("flex", type="build")
    depends_on("cmake", type="build")

    depends_on("scotch~metis", when="~ptscotch+scotch")
    depends_on("scotch~metis+mpi", when="+ptscotch")
    depends_on("metis@5:", when="+metis")
    depends_on("parmetis", when="+parmetis")
    # mgridgen is statically linked
    depends_on("parmgridgen", when="+parmgridgen", type="build")
    depends_on("paraview@:5.0.1", when="+paraview")
    depends_on("mesquite")

    # General patches
    common = ["spack-Allwmake", "README-spack"]
    assets = []  # type: List[str]

    # Some user config settings
    config = {"label-size": False, "mplib": "USERMPI"}  # <- No int32/int64 support  # USERMPI

    # The openfoam architecture, compiler information etc
    _foam_arch = None

    # Content for etc/prefs.{csh,sh}
    etc_prefs = {}  # type: Dict[str, str]

    # Content for etc/config.{csh,sh}/ files
    etc_config = {}  # type: Dict[str, str]

    phases = ["configure", "build", "install"]
    build_script = "./spack-Allwmake"  # <- Added by patch() method.

    #
    # - End of definitions / setup -
    #

    def setup_run_environment(self, env):
        """Add environment variables to the generated module file.
        These environment variables come from running:

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
                        "PS1",  # Leave unaffected
                        "MANPATH",  # Leave unaffected
                        # Unneeded bits
                        # -------------
                        "FOAM_INST_DIR",  # Possibly incorrect
                        "FOAM_(APP|ETC|SRC|SOLVERS|UTILITIES)",
                        "FOAM_TEST_.*_DIR",
                        "WM_NCOMPPROCS",
                        # 'FOAM_TUTORIALS',  # can be useful
                        # Lots of third-party cruft
                        # -------------------------
                        "[A-Z].*_(BIN|LIB|INCLUDE)_DIR",
                        "[A-Z].*_SYSTEM",
                        "WM_THIRD_PARTY_.*",
                        "(BISON|FLEX|CMAKE|ZLIB)_DIR",
                        "(METIS|PARMETIS|PARMGRIDGEN|SCOTCH)_DIR",
                        # User-specific
                        # -------------
                        "FOAM_RUN",
                        "(FOAM|WM)_.*USER_.*",
                    ],
                    whitelist=[  # Whitelist these
                        "MPI_ARCH_PATH",  # Can be needed for compilation
                        "PYTHON_BIN_DIR",
                    ],
                )

                env.extend(mods)
                minimal = False
                tty.info("foam-extend env: {0}".format(bashrc))
            except Exception:
                minimal = True

        if minimal:
            # pre-build or minimal environment
            tty.info("foam-extend minimal env {0}".format(self.prefix))
            env.set("FOAM_INST_DIR", os.path.dirname(self.projectdir)),
            env.set("FOAM_PROJECT_DIR", self.projectdir)
            env.set("WM_PROJECT_DIR", self.projectdir)
            for d in ["wmake", self.archbin]:  # bin added automatically
                env.prepend_path("PATH", join_path(self.projectdir, d))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Location of the OpenFOAM project.
        This is identical to the WM_PROJECT_DIR value, but we avoid that
        variable since it would mask the normal OpenFOAM cleanup of
        previous versions.
        """
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
        return join_path("applications", "bin", self.foam_arch)

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        return join_path("lib", self.foam_arch)

    def rename_source(self):
        """The github tarfiles have weird names that do not correspond to the
        canonical name. We need to rename these, but leave a symlink for
        spack to work with.
        """
        # Note that this particular Foam-Extned requires absolute directories
        # to build correctly!
        parent = os.path.dirname(self.stage.source_path)
        original = os.path.basename(self.stage.source_path)
        target = "foam-extend-{0}".format(self.version)
        # Could also grep through etc/bashrc for WM_PROJECT_VERSION
        with working_dir(parent):
            if original != target and not os.path.lexists(target):
                os.rename(original, target)
                os.symlink(target, original)
                tty.info("renamed {0} -> {1}".format(original, target))

    def patch(self):
        """Adjust OpenFOAM build for spack.
        Where needed, apply filter as an alternative to normal patching."""
        add_extra_files(self, self.common, self.assets)
        self.rename_source()

        # Adjust ParMGridGen - this is still a mess
        files = [
            "src/dbns/Make/options",
            "src/fvAgglomerationMethods/MGridGenGamgAgglomeration/Make/options",
        ]
        for f in files:
            filter_file(r"-lMGridGen", r"-lmgrid", f, backup=False)

        # Adjust for flex version check
        files = [
            (
                "src/thermophysicalModels/reactionThermo/chemistryReaders/chemkinReader/"
                "chemkinLexer.L"
            ),
            "src/surfMesh/surfaceFormats/stl/STLsurfaceFormatASCII.L",
            "src/meshTools/triSurface/triSurface/interfaces/STL/readSTLASCII.L",
            "applications/utilities/preProcessing/fluentDataToFoam/fluentDataToFoam.L",
            "applications/utilities/mesh/conversion/gambitToFoam/gambitToFoam.L",
            "applications/utilities/mesh/conversion/fluent3DMeshToFoam/fluent3DMeshToFoam.L",
            "applications/utilities/mesh/conversion/ansysToFoam/ansysToFoam.L",
            "applications/utilities/mesh/conversion/fluentMeshToFoam/fluentMeshToFoam.L",
            "applications/utilities/mesh/conversion/fluent3DMeshToElmer/fluent3DMeshToElmer.L",
        ]
        for f in files:
            filter_file(
                r"#if YY_FLEX_SUBMINOR_VERSION < 34",
                (
                    r"#if YY_FLEX_MAJOR_VERSION <= 2 "
                    r"&& YY_FLEX_MINOR_VERSION <= 5 "
                    r"&& YY_FLEX_SUBMINOR_VERSION < 34"
                ),
                f,
                backup=False,
            )

    def configure(self, spec, prefix):
        """Make adjustments to the OpenFOAM configuration files in their various
        locations: etc/bashrc, etc/config.sh/FEATURE and customizations that
        don't properly fit get placed in the etc/prefs.sh file (similiarly for
        csh).
        """
        # Content for etc/prefs.{csh,sh}
        self.etc_prefs = {
            "000": {"compilerInstall": "System"},  # Sort first
            "001": {},
            "cmake": {
                "CMAKE_DIR": spec["cmake"].prefix,
                "CMAKE_BIN_DIR": spec["cmake"].prefix.bin,
            },
            "python": {
                "PYTHON_DIR": spec["python"].home,
                "PYTHON_BIN_DIR": spec["python"].home.bin,
            },
            "flex": {"FLEX_SYSTEM": 1, "FLEX_DIR": spec["flex"].prefix},
            "bison": {"BISON_SYSTEM": 1, "BISON_DIR": spec["flex"].prefix},
            "zlib": {"ZLIB_SYSTEM": 1, "ZLIB_DIR": spec["zlib-api"].prefix},
            "mesquite": {
                "MESQUITE_SYSTEM": 1,
                "MESQUITE_DIR": spec["mesquite"].prefix,
                "MESQUITE_INCLUDE_DIR": spec["mesquite"].prefix.include,
                "NESQUITE_LIB_DIR": spec["mesquite"].prefix.lib,
            },
        }
        # Adjust configuration via prefs - sort second
        self.etc_prefs["001"].update(self.foam_arch.foam_dict())

        if spec.satisfies("+scotch") or spec.satisfies("+ptscotch"):
            pkg = spec["scotch"].prefix
            self.etc_prefs["scotch"] = {
                "SCOTCH_SYSTEM": 1,
                "SCOTCH_DIR": pkg,
                "SCOTCH_BIN_DIR": pkg.bin,
                "SCOTCH_LIB_DIR": pkg.lib,
                "SCOTCH_INCLUDE_DIR": pkg.include,
            }

        if spec.satisfies("+metis"):
            pkg = spec["metis"].prefix
            self.etc_prefs["metis"] = {
                "METIS_SYSTEM": 1,
                "METIS_DIR": pkg,
                "METIS_BIN_DIR": pkg.bin,
                "METIS_LIB_DIR": pkg.lib,
                "METIS_INCLUDE_DIR": pkg.include,
            }

        if spec.satisfies("+parmetis"):
            pkg = spec["parmetis"].prefix
            self.etc_prefs["parametis"] = {
                "PARMETIS_SYSTEM": 1,
                "PARMETIS_DIR": pkg,
                "PARMETIS_BIN_DIR": pkg.bin,
                "PARMETIS_LIB_DIR": pkg.lib,
                "PARMETIS_INCLUDE_DIR": pkg.include,
            }

        if spec.satisfies("+parmgridgen"):
            pkg = spec["parmgridgen"].prefix
            self.etc_prefs["parmgridgen"] = {
                "PARMGRIDGEN_SYSTEM": 1,
                "PARMGRIDGEN_DIR": pkg,
                "PARMGRIDGEN_BIN_DIR": pkg.bin,
                "PARMGRIDGEN_LIB_DIR": pkg.lib,
                "PARMGRIDGEN_INCLUDE_DIR": pkg.include,
            }

        if self.spec.satisfies("+paraview"):
            self.etc_prefs["paraview"] = {
                "PARAVIEW_SYSTEM": 1,
                "PARAVIEW_DIR": spec["paraview"].prefix,
                "PARAVIEW_BIN_DIR": spec["paraview"].prefix.bin,
            }
            self.etc_prefs["qt"] = {
                "QT_SYSTEM": 1,
                "QT_DIR": spec["qt"].prefix,
                "QT_BIN_DIR": spec["qt"].prefix.bin,
            }

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        write_environ(
            self.etc_prefs,
            posix=join_path("etc", "prefs.sh"),
            cshell=join_path("etc", "prefs.csh"),
        )

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        Only build if the compiler is known to be supported.
        """
        self.foam_arch.has_rule(self.stage.source_path)
        self.foam_arch.create_rules(self.stage.source_path, self)

        args = []
        if self.parallel:  # Build in parallel? - pass via the environment
            os.environ["WM_NCOMPPROCS"] = str(make_jobs)
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the projectdir"""

        # Fairly ugly since intermediate targets are scattered inside sources
        appdir = "applications"
        projdir = os.path.basename(self.projectdir)
        mkdirp(self.projectdir, join_path(self.projectdir, appdir))
        # Filtering: bashrc, cshrc
        edits = {
            "WM_PROJECT_INST_DIR": os.path.dirname(self.projectdir),
            "WM_PROJECT_DIR": join_path("$WM_PROJECT_INST_DIR", projdir),
        }

        # All top-level files, except spack build info and possibly Allwmake
        if spec.satisfies("+source"):
            ignored = re.compile(r"^spack-.*")
        else:
            ignored = re.compile(r"^(Allclean|Allwmake|spack-).*")

        files = [f for f in glob.glob("*") if os.path.isfile(f) and not ignored.search(f)]
        for f in files:
            install(f, self.projectdir)

        # Install directories. install applications/bin directly
        # Install 'etc' before 'bin' (for symlinks)
        for d in ["etc", "bin", "wmake", "lib", join_path(appdir, "bin")]:
            install_tree(d, join_path(self.projectdir, d), symlinks=True)

        if spec.satisfies("+source"):
            subitem = join_path(appdir, "Allwmake")
            install(subitem, join_path(self.projectdir, subitem))

            foam_arch_str = str(self.foam_arch)
            # Ignore intermediate targets
            ignore = lambda p: os.path.basename(p) == foam_arch_str

            for d in ["src", "tutorials"]:
                install_tree(d, join_path(self.projectdir, d), ignore=ignore, symlinks=True)

            for d in ["solvers", "utilities"]:
                install_tree(
                    join_path(appdir, d),
                    join_path(self.projectdir, appdir, d),
                    ignore=ignore,
                    symlinks=True,
                )

        etc_dir = join_path(self.projectdir, "etc")
        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            edits, posix=join_path(etc_dir, "bashrc"), cshell=join_path(etc_dir, "cshrc")
        )
        self.install_links()

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        # Make build log visible - it contains OpenFOAM-specific information
        with working_dir(self.projectdir):
            os.symlink(
                join_path(os.path.relpath(self.install_log_path)),
                join_path("log." + str(self.foam_arch)),
            )


# -----------------------------------------------------------------------------
