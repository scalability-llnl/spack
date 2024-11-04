# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import inspect
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ElementTree

import llnl.util.tty as tty
from llnl.util.filesystem import (
    HeaderList,
    LibraryList,
    ancestor,
    filter_file,
    find_headers,
    find_libraries,
    find_system_libraries,
    install,
)

import spack.builder
import spack.error
from spack.build_environment import dso_suffix
from spack.error import InstallError
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable
from spack.util.prefix import Prefix
from spack.version import Version, ver

from .generic import Package

# A couple of utility functions that might be useful in general. If so, they
# should really be defined elsewhere, unless deemed heretical.
# (Or na"ive on my part).


def debug_print(msg, *args):
    """Prints a message (usu. a variable) and the callers' names for a couple
    of stack frames.
    """
    # https://docs.python.org/2/library/inspect.html#the-interpreter-stack
    stack = inspect.stack()
    _func_name = 3
    tty.debug("%s.%s:\t%s" % (stack[2][_func_name], stack[1][_func_name], msg), *args)


def raise_lib_error(*args):
    """Bails out with an error message. Shows args after the first as one per
    line, tab-indented, useful for long paths to line up and stand out.
    """
    raise InstallError("\n\t".join(str(i) for i in args))


def _expand_fields(s):
    """[Experimental] Expand arch-related fields in a string, typically a
    filename.

    Supported fields and their typical expansions are::

        {platform}  linux, mac
        {arch}      intel64 (including on Mac)
        {libarch}   intel64, empty on Mac
        {bits}      64

    """
    # Python-native string formatting requires arg list counts to match the
    # replacement field count; optional fields are far easier with regexes.

    _bits = "64"
    _arch = "intel64"  # TBD: ia32

    if "linux" in sys.platform:  # NB: linux2 vs. linux
        s = re.sub("{platform}", "linux", s)
        s = re.sub("{libarch}", _arch, s)
    elif "darwin" in sys.platform:
        s = re.sub("{platform}", "mac", s)
        s = re.sub("{libarch}", "", s)  # no arch dirs are used (as of 2018)
    # elif 'win' in sys.platform:            # TBD
    #     s = re.sub('{platform}', 'windows', s)

    s = re.sub("{arch}", _arch, s)
    s = re.sub("{bits}", _bits, s)
    return s


class IntelPackage(Package):
    """Specialized class for licensed Intel software.

    This class provides two phases that can be overridden:

    1. :py:meth:`~.IntelPackage.configure`
    2. :py:meth:`~.IntelPackage.install`

    They both have sensible defaults and for many packages the
    only thing necessary will be to override setup_run_environment
    to set the appropriate environment variables.
    """

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "IntelPackage"

    #: A dict that maps Spack version specs to release years, needed to infer
    #: the installation directory layout for pre-2016 versions in the family of
    #: Intel packages.
    #
    # Like any property, it can be overridden in client packages, should older
    # versions ever be added there.  The initial dict here contains the
    # packages defined in Spack as of 2018-04.  Keys could conceivably overlap
    # but preferably should not - only the first key in hash traversal order
    # that satisfies self.spec will be used.
    version_years = {
        # intel-daal is versioned 2016 and later, no divining is needed
        "intel-ipp@9.0:9": 2016,
        "intel-mkl@11.3.0:11.3": 2016,
        "intel-mpi@5.1:5": 2016,
    }

    # Below is the list of possible values for setting auto dispatch functions
    # for the Intel compilers. Using these allows for the building of fat
    # binaries that will detect the CPU SIMD capabilities at run time and
    # activate the appropriate extensions.
    auto_dispatch_options = (
        "COMMON-AVX512",
        "MIC-AVX512",
        "CORE-AVX512",
        "CORE-AVX2",
        "CORE-AVX-I",
        "AVX",
        "SSE4.2",
        "SSE4.1",
        "SSSE3",
        "SSE3",
        "SSE2",
    )

    @property
    def license_required(self):
        # The Intel libraries are provided without requiring a license as of
        # version 2017.2. Trying to specify one anyway will fail. See:
        # https://software.intel.com/en-us/articles/free-ipsxe-tools-and-libraries
        return self._has_compilers or self.version < Version("2017.2")

    #: Comment symbol used in the license.lic file
    license_comment = "#"

    #: Environment variables that Intel searches for a license file
    license_vars = ["INTEL_LICENSE_FILE"]

    #: URL providing information on how to acquire a license key
    license_url = "https://software.intel.com/en-us/articles/intel-license-manager-faq"

    #: Location where Intel searches for a license file
    @property
    def license_files(self):
        dirs = ["Licenses"]

        if self._has_compilers:
            dirs.append(self.component_bin_dir("compiler"))

            for variant, component_suite_dir in {
                "+advisor": "advisor",
                "+inspector": "inspector",
                "+itac": "itac",
                "+vtune": "vtune_profiler",
            }.items():
                if variant in self.spec:
                    dirs.append(
                        self.normalize_path("licenses", component_suite_dir, relative=True)
                    )

        files = [os.path.join(d, "license.lic") for d in dirs]
        return files

    #: Components to install (list of name patterns from pset/mediaconfig.xml)
    # NB: Renamed from plain components() for coding and maintainability.
    @property
    def pset_components(self):
        # Do not detail single-purpose client packages.
        if not self._has_compilers:
            return ["ALL"]

        # tty.warn('DEBUG: installing ALL components')
        # return ['ALL']

        # Always include compilers and closely related components.
        # Pre-2016 compiler components have different names - throw in all.
        # Later releases have overlapping minor parts that differ by "edition".
        # NB: The spack package 'intel' is a subset of
        # 'intel-parallel-studio@composer' without the lib variants.
        c = (
            " intel-icc          intel-ifort"
            " intel-ccomp        intel-fcomp        intel-comp-"
            " intel-compilerproc intel-compilerprof intel-compilerpro-"
            " intel-psxe intel-openmp"
        )

        additions_for = {
            "cluster": " intel-icsxe",
            "professional": " intel-ips-",
            "composer": " intel-compxe",
        }
        if self._edition in additions_for:
            c += additions_for[self._edition]

        for variant, components_to_add in {
            "+daal": " intel-daal",  # Data Analytics Acceleration Lib
            "+gdb": " intel-gdb",  # Integrated Performance Primitives
            "+ipp": " intel-ipp intel-crypto-ipp",
            "+mkl": " intel-mkl",  # Math Kernel Library
            "+mpi": " intel-mpi intel-imb",  # MPI runtime, SDK, benchm.
            "+tbb": " intel-tbb",  # Threading Building Blocks
            "+advisor": " intel-advisor",
            "+clck": " intel_clck",  # Cluster Checker
            "+inspector": " intel-inspector",
            "+itac": " intel-itac intel-ta intel-tc" " intel-trace-analyzer intel-trace-collector",
            # Trace Analyzer and Collector
            "+vtune": " intel-vtune",
            # VTune, ..-profiler since 2020, ..-amplifier before
        }.items():
            if variant in self.spec:
                c += components_to_add

        debug_print(c)
        return c.split()

    # ---------------------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------------------
    @property
    def _filtered_components(self):
        """Expands the list of desired component patterns to the exact names
        present in the given download.
        """
        c = self.pset_components
        if "ALL" in c or "DEFAULTS" in c:  # No filter needed
            return c

        # mediaconfig.xml is known to contain duplicate components.
        # If more than one copy of the same component is used, you
        # will get an error message about invalid components.
        # Use sets to prevent duplicates and for efficient traversal.
        requested = set(c)
        confirmed = set()

        # NB: To get a reasonable overview in pretty much the documented way:
        #
        #   grep -E '<Product|<Abbr|<Name>..[a-z]'  pset/mediaconfig.xml
        #
        # https://software.intel.com/en-us/articles/configuration-file-format
        #
        xmltree = ElementTree.parse("pset/mediaconfig.xml")
        for entry in xmltree.getroot().findall(".//Abbr"):  # XPath expression
            name_present = entry.text
            for name_requested in requested:
                if name_present.startswith(name_requested):
                    confirmed.add(name_present)

        return list(confirmed)

    @property
    def intel64_int_suffix(self):
        """Provide the suffix for Intel library names to match a client
        application's desired int size, conveyed by the active spec variant.
        The possible suffixes and their meanings are:

          ``ilp64``  all of int, long, and pointer are 64 bit,
          `` lp64``  only long and pointer are 64 bit; int will be 32bit.
        """
        if "+ilp64" in self.spec:
            return "ilp64"
        else:
            return "lp64"

    @property
    def _has_compilers(self):
        return self.name in ["intel", "intel-parallel-studio"]

    @property
    def _edition(self):
        if self.name == "intel-parallel-studio":
            return self.version[0]  # clearer than .up_to(1), I think.
        elif self.name == "intel":
            return "composer"
        else:
            return ""

    @property
    def version_yearlike(self):
        """Return the version in a unified style, suitable for Version class
        conditionals.
        """
        # Input data for this routine:  self.version
        # Returns:                      YYYY.Nupdate[.Buildseq]
        #
        # Specifics by package:
        #
        #   Package                     Format of self.version
        #   ------------------------------------------------------------
        #   'intel-parallel-studio'     <edition>.YYYY.Nupdate
        #   'intel'                     YY.0.Nupdate (some assigned ad-hoc)
        #   Recent lib packages         YYYY.Nupdate.Buildseq
        #   Early lib packages          Major.Minor.Patch.Buildseq
        #   ------------------------------------------------------------
        #
        #   Package                     Output
        #   ------------------------------------------------------------
        #   'intel-parallel-studio'     YYYY.Nupdate
        #   'intel'                     YYYY.Nupdate
        #   Recent lib packages         YYYY.Nupdate.Buildseq
        #   Known early lib packages    YYYY.Minor.Patch.Buildseq (*)
        #   Unknown early lib packages  (2000 + Major).Minor.Patch.Buildseq
        #   ----------------------------------------------------------------
        #
        #   (*) YYYY is taken from @property "version_years" (a dict of specs)
        #
        try:
            if self.name == "intel":
                # Has a "Minor" version element, but it is always set as 0. To
                # be useful for comparisons, drop it and get YYYY.Nupdate.
                v_tail = self.version[2:]  # coerced just fine via __getitem__
            else:
                v_tail = self.version[1:]
        except IndexError:
            # Hmm - this happens on "spack install intel-mkl@11".
            # I thought concretization picks an actual version??
            return self.version  # give up

        if self.name == "intel-parallel-studio":
            return v_tail

        v_year = self.version[0]
        if v_year < 2000:
            # Shoehorn Major into release year until we know better.
            v_year += 2000
            for spec, year in self.version_years.items():
                if self.spec.satisfies(spec):
                    v_year = year
                    break

        return Version("%s.%s" % (v_year, v_tail))

    # ---------------------------------------------------------------------
    # Directory handling common to all Intel components
    # ---------------------------------------------------------------------
    # For reference: classes using IntelPackage, as of Spack-0.11:
    #
    #  intel/               intel-ipp/          intel-mpi/
    #  intel-daal/          intel-mkl/          intel-parallel-studio/
    #
    # Not using class IntelPackage:
    #  intel-gpu-tools/        intel-mkl-dnn/          intel-tbb/
    #
    def normalize_suite_dir(self, suite_dir_name, version_globs=["*.*.*"]):
        """Returns the version-specific and absolute path to the directory of
        an Intel product or a suite of product components.

        Parameters:

            suite_dir_name (str):
                Name of the product directory, without numeric version.

                - Examples::

                    composer_xe, parallel_studio_xe, compilers_and_libraries

                The following will work as well, even though they are not
                directly targets for Spack installation::

                    advisor_xe, inspector_xe, vtune_amplifier_xe,
                    performance_snapshots (new name for vtune as of 2018)

                These are single-component products without subordinate
                components and are normally made available to users by a
                toplevel psxevars.sh or equivalent file to source (and thus by
                the modulefiles that Spack produces).

            version_globs (list): Suffix glob patterns (most specific
                first) expected to qualify suite_dir_name to its fully
                version-specific install directory (as opposed to a
                compatibility directory or symlink).
        """
        # See ./README-intel.rst for background and analysis of dir layouts.

        d = self.prefix

        # Distinguish between product installations that were done external to
        # Spack (integrated via packages.yaml) and Spack-internal ones. The
        # resulting prefixes may differ in directory depth and specificity.
        unversioned_dirname = ""
        if suite_dir_name and suite_dir_name in d:
            # If e.g. MKL was installed outside of Spack, it is likely just one
            # product or product component among possibly many other Intel
            # products and their releases that were installed in sibling or
            # cousin directories.  In such cases, the prefix given to Spack
            # will inevitably be a highly product-specific and preferably fully
            # version-specific directory.  This is what we want and need, and
            # nothing more specific than that, i.e., if needed, convert, e.g.:
            #   .../compilers_and_libraries*/* -> .../compilers_and_libraries*
            d = re.sub("(%s%s.*?)%s.*" % (os.sep, re.escape(suite_dir_name), os.sep), r"\1", d)

            # The Intel installer scripts try hard to place compatibility links
            # named like this in the install dir to convey upgrade benefits to
            # traditional client apps. But such a generic name can be trouble
            # when given to Spack: the link target is bound to change outside
            # of Spack's purview and when it does, the outcome of subsequent
            # builds of dependent packages may be affected. (Though Intel has
            # been remarkably good at backward compatibility.)
            # I'm not sure if Spack's package hashing includes link targets.
            if d.endswith(suite_dir_name):
                # NB: This could get tiresome without a seen++ test.
                # tty.warn('Intel product found in a version-neutral directory'
                #          ' - future builds may not be reproducible.')
                #
                # Simply doing realpath() would not be enough, because:
                #   compilers_and_libraries -> compilers_and_libraries_2018
                # which is mostly a staging directory for symlinks (see next).
                unversioned_dirname = d
        else:
            # By contrast, a Spack-internal MKL installation will inherit its
            # prefix from install.sh of Intel's package distribution, where it
            # means the high-level installation directory that is specific to
            # the *vendor* (think of the default "/opt/intel"). We must now
            # step down into the *product* directory to get the usual
            # hierarchy. But let's not do that in haste ...
            #
            # For a Spack-born install, the fully-qualified release directory
            # desired above may seem less important since product upgrades
            # won't land in the same parent. However, only the fully qualified
            # directory contains the regular files for the compiler commands:
            #
            # $ ls -lF <HASH>/compilers_and_libraries*/linux/bin/intel64/icc
            #
            # <HASH>/compilers_and_libraries_2018.1.163/linux/bin/intel64/icc*
            #   A regular file in the actual release directory. Bingo!
            #
            # <HASH>/compilers_and_libraries_2018/linux/bin/intel64/icc -> ...
            #   A symlink - no good. Note that "compilers_and_libraries_2018/"
            #   is itself a directory (not symlink) but it merely holds a
            #   compatibility dir hierarchy with lots of symlinks into the
            #   release dir.
            #
            # <HASH>/compilers_and_libraries/linux/bin/intel64/icc -> ...
            #   Ditto.
            #
            #  Now, the Spack packages for MKL and MPI packges use version
            #  triplets, but the one for intel-parallel-studio does not.
            #  So, we can't have it quite as easy as:
            # d = Prefix(d.append('compilers_and_libraries_' + self.version))
            #  Alright, let's see what we can find instead:
            unversioned_dirname = os.path.join(d, suite_dir_name)

        if unversioned_dirname:
            for g in version_globs:
                try_glob = unversioned_dirname + g
                debug_print("trying %s" % try_glob)

                matching_dirs = sorted(glob.glob(try_glob))
                # NB: Python glob() returns results in arbitrary order - ugh!
                # NB2: sorted() is a shortcut that is NOT number-aware.

                if matching_dirs:
                    debug_print("found %d:" % len(matching_dirs), matching_dirs)
                    # Take the highest and thus presumably newest match, which
                    # better be the sole one anyway.
                    d = matching_dirs[-1]
                    break

            if not matching_dirs:
                # No match -- return a sensible value anyway.
                d = unversioned_dirname

        debug_print(d)
        return Prefix(d)

    def normalize_path(self, component_path, component_suite_dir=None, relative=False):
        """Returns the absolute or relative path to a component or file under a
        component suite directory.

        Intel's product names, scope, and directory layout changed over the
        years.  This function provides a unified interface to their directory
        names.

        Parameters:

            component_path (str): a component name like 'mkl', or 'mpi', or a
                deeper relative path.

            component_suite_dir (str): _Unversioned_ name of the expected
                parent directory of component_path.  When absent or `None`, an
                appropriate default will be used.  A present but empty string
                `""` requests that `component_path` refer to `self.prefix`
                directly.

                Typical values: `compilers_and_libraries`, `composer_xe`,
                `parallel_studio_xe`.

                Also supported: `advisor`, `inspector`, `vtune`. The actual
                directory name for these suites varies by release year. The
                name will be corrected as needed for use in the return value.

            relative (bool): When True, return path relative to self.prefix,
                otherwise, return an absolute path (the default).
        """
        # Design note: Choosing the default for `component_suite_dir` was a bit
        # tricky since there better be a sensible means to specify direct
        # parentage under self.prefix (even though you normally shouldn't need
        # a function for that).  I chose "" to allow that case be represented,
        # and 'None' or the absence of the kwarg to represent the most relevant
        # case for the time of writing.
        #
        # In the 2015 releases (the earliest in Spack as of 2018), there were
        # nominally two separate products that provided the compilers:
        # "Composer" as lower tier, and "Parallel Studio" as upper tier. In
        # Spack, we justifiably retcon both as "intel-parallel-studio@composer"
        # and "...@cluster", respectively.  Both of these use the older
        # "composer_xe" dir layout, as do their virtual package personas.
        #
        # All other "intel-foo" packages in Spack as of 2018-04 use the
        # "compilers_and_libraries" layout, including the 2016 releases that
        # are not natively versioned by year.

        cs = component_suite_dir
        if cs is None and component_path.startswith("ism"):
            cs = "parallel_studio_xe"

        v = self.version_yearlike

        # Glob variants to complete component_suite_dir.
        # Helper var for older MPI versions - those are reparented, with each
        # version in their own version-named dir.
        standalone_glob = "[1-9]*.*.*"

        # Most other components; try most specific glob first.
        # flake8 is far too opinionated about lists - ugh.
        normalize_kwargs = {
            "version_globs": [
                "_%s" % self.version,
                "_%s.*" % v.up_to(2),  # should be: YYYY.Nupdate
                "_*.*.*",  # last resort
            ]
        }
        for rename_rule in [
            # cs given as arg, in years, dir actually used, [version_globs]
            [None, ":2015", "composer_xe"],
            [None, "2016:", "compilers_and_libraries"],
            ["advisor", ":2016", "advisor_xe"],
            ["inspector", ":2016", "inspector_xe"],
            ["vtune_profiler", ":2017", "vtune_amplifier_xe"],
            ["vtune", ":2017", "vtune_amplifier_xe"],  # alt.
            ["vtune_profiler", ":2019", "vtune_amplifier"],
            ["itac", ":", "itac", [os.sep + standalone_glob]],
        ]:
            if cs == rename_rule[0] and v.satisfies(ver(rename_rule[1])):
                cs = rename_rule[2]
                if len(rename_rule) > 3:
                    normalize_kwargs = {"version_globs": rename_rule[3]}
                break

        d = self.normalize_suite_dir(cs, **normalize_kwargs)

        # Help find components not located directly under d.
        # NB: ancestor() not well suited if version_globs may contain os.sep .
        parent_dir = re.sub(os.sep + re.escape(cs) + ".*", "", d)

        reparent_as = {}
        if cs == "compilers_and_libraries":  # must qualify further
            d = os.path.join(d, _expand_fields("{platform}"))
        elif cs == "composer_xe":
            reparent_as = {"mpi": "impi"}
            # ignore 'imb' (MPI Benchmarks)

        for nominal_p, actual_p in reparent_as.items():
            if component_path.startswith(nominal_p):
                dirs = glob.glob(os.path.join(parent_dir, actual_p, standalone_glob))
                debug_print("reparent dirs: %s" % dirs)
                # Brazenly assume last match is the most recent version;
                # convert back to relative of parent_dir, and re-assemble.
                rel_dir = dirs[-1].split(parent_dir + os.sep, 1)[-1]
                component_path = component_path.replace(nominal_p, rel_dir, 1)
                d = parent_dir

        d = os.path.join(d, component_path)

        if relative:
            d = os.path.relpath(os.path.realpath(d), parent_dir)

        debug_print(d)
        return d

    def component_bin_dir(self, component, **kwargs):
        d = self.normalize_path(component, **kwargs)

        if component == "compiler":  # bin dir is always under PARENT
            d = os.path.join(ancestor(d), "bin", _expand_fields("{libarch}"))
            d = d.rstrip(os.sep)  # cosmetics, when {libarch} is empty
            # NB: Works fine even with relative=True, e.g.:
            #   composer_xe/compiler -> composer_xe/bin/intel64
        elif component == "mpi":
            d = os.path.join(d, _expand_fields("{libarch}"), "bin")
        else:
            d = os.path.join(d, "bin")
        debug_print(d)
        return d

    def component_lib_dir(self, component, **kwargs):
        """Provide directory suitable for find_libraries() and
        SPACK_COMPILER_EXTRA_RPATHS.
        """
        d = self.normalize_path(component, **kwargs)

        if component == "mpi":
            d = os.path.join(d, _expand_fields("{libarch}"), "lib")
        else:
            d = os.path.join(d, "lib", _expand_fields("{libarch}"))
            d = d.rstrip(os.sep)  # cosmetics, when {libarch} is empty

        if component == "tbb":  # must qualify further for abi
            d = os.path.join(d, self._tbb_abi)

        debug_print(d)
        return d

    def component_include_dir(self, component, **kwargs):
        d = self.normalize_path(component, **kwargs)

        if component == "mpi":
            d = os.path.join(d, _expand_fields("{libarch}"), "include")
        else:
            d = os.path.join(d, "include")

        debug_print(d)
        return d

    @property
    def file_to_source(self):
        """Full path of file to source for initializing an Intel package.
        A client package could override as follows:
        `    @property`
        `    def file_to_source(self):`
        `        return self.normalize_path("apsvars.sh", "vtune_amplifier")`
        """
        vars_file_info_for = {
            # key (usu. spack package name) -> [rel_path, component_suite_dir]
            # Extension note: handle additions by Spack name or ad-hoc keys.
            "@early_compiler": ["bin/compilervars", None],
            "intel-parallel-studio": ["bin/psxevars", "parallel_studio_xe"],
            "intel": ["bin/compilervars", None],
            "intel-daal": ["daal/bin/daalvars", None],
            "intel-ipp": ["ipp/bin/ippvars", None],
            "intel-mkl": ["mkl/bin/mklvars", None],
            "intel-mpi": ["mpi/{libarch}/bin/mpivars", None],
        }
        key = self.name
        if self.version_yearlike.satisfies(ver(":2015")):
            # Same file as 'intel' but 'None' for component_suite_dir will
            # resolve differently. Listed as a separate entry to serve as
            # example and to avoid pitfalls upon possible refactoring.
            key = "@early_compiler"

        f, component_suite_dir = vars_file_info_for[key]
        f = _expand_fields(f) + ".sh"
        # TODO?? win32 would have to handle os.sep, '.bat' (unless POSIX??)

        f = self.normalize_path(f, component_suite_dir)
        return f

    # ---------------------------------------------------------------------
    # Threading, including (WIP) support for virtual 'tbb'
    # ---------------------------------------------------------------------
    @property
    def openmp_libs(self):
        """Supply LibraryList for linking OpenMP"""

        if "%intel" in self.spec:
            # NB: Hunting down explicit library files may be the Spack way of
            # doing things, but be aware that "{icc|ifort} --help openmp"
            # steers us towards options instead: -qopenmp-link={dynamic,static}

            omp_libnames = ["libiomp5"]
            omp_libs = find_libraries(
                omp_libnames,
                root=self.component_lib_dir("compiler"),
                shared=("+shared" in self.spec),
            )
            # Note about search root here: For MKL, the directory
            # "$MKLROOT/../compiler" will be present even for an MKL-only
            # product installation (as opposed to one being ghosted via
            # packages.yaml), specificially to provide the 'iomp5' libs.

        elif "%gcc" in self.spec:
            with self.compiler.compiler_environment():
                omp_lib_path = Executable(self.compiler.cc)(
                    "--print-file-name", "libgomp.%s" % dso_suffix, output=str
                )
            omp_libs = LibraryList(omp_lib_path.strip())

        elif "%clang" in self.spec:
            with self.compiler.compiler_environment():
                omp_lib_path = Executable(self.compiler.cc)(
                    "--print-file-name", "libomp.%s" % dso_suffix, output=str
                )
            omp_libs = LibraryList(omp_lib_path.strip())

        if len(omp_libs) < 1:
            raise_lib_error("Cannot locate OpenMP libraries:", omp_libnames)

        debug_print(omp_libs)
        return omp_libs

    @property
    def _gcc_executable(self):
        """Return GCC executable"""
        # Match the available gcc, as it's done in tbbvars.sh.
        gcc_name = "gcc"
        # but first check if -gcc-name is specified in cflags
        for flag in self.spec.compiler_flags["cflags"]:
            if flag.startswith("-gcc-name="):
                gcc_name = flag.split("-gcc-name=")[1]
                break
        debug_print(gcc_name)
        return Executable(gcc_name)

    @property
    def tbb_headers(self):
        # Note: TBB is included as
        # #include <tbb/task_scheduler_init.h>
        return HeaderList([self.component_include_dir("tbb") + "/dummy.h"])

    @property
    def tbb_libs(self):
        """Supply LibraryList for linking TBB"""

        # TODO: When is 'libtbbmalloc' needed?
        tbb_lib = find_libraries(["libtbb"], root=self.component_lib_dir("tbb"))
        # NB: Like icc with -qopenmp, so does icpc steer us towards using an
        # option: "icpc -tbb"

        # TODO: clang(?)
        gcc = self._gcc_executable  # must be gcc, not self.compiler.cc
        with self.compiler.compiler_environment():
            cxx_lib_path = gcc("--print-file-name", "libstdc++.%s" % dso_suffix, output=str)

        libs = tbb_lib + LibraryList(cxx_lib_path.rstrip())
        debug_print(libs)
        return libs

    @property
    def _tbb_abi(self):
        """Select the ABI needed for linking TBB"""
        gcc = self._gcc_executable
        with self.compiler.compiler_environment():
            matches = re.search(
                r"(gcc|LLVM).* ([0-9]+\.[0-9]+\.[0-9]+).*",
                gcc("--version", output=str),
                re.I | re.M,
            )
        abi = ""
        if sys.platform == "darwin":
            pass
        elif matches:
            # TODO: Confirm that this covers clang (needed on Linux only)
            gcc_version = Version(matches.groups()[1])
            if gcc_version >= Version("4.7"):
                abi = "gcc4.7"
            elif gcc_version >= Version("4.4"):
                abi = "gcc4.4"
            else:
                abi = "gcc4.1"  # unlikely, one hopes.

        # Alrighty then ...
        debug_print(abi)
        return abi

    # ---------------------------------------------------------------------
    # Support for virtual 'blas/lapack/scalapack'
    # ---------------------------------------------------------------------
    @property
    def blas_libs(self):
        # Main magic here.
        # For reference, see The Intel Math Kernel Library Link Line Advisor:
        # https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/

        mkl_integer = "libmkl_intel_" + self.intel64_int_suffix

        if self.spec.satisfies("threads=openmp"):
            if "%intel" in self.spec:
                mkl_threading = "libmkl_intel_thread"
            elif "%gcc" in self.spec or "%clang" in self.spec:
                mkl_threading = "libmkl_gnu_thread"
            threading_engine_libs = self.openmp_libs
        elif self.spec.satisfies("threads=tbb"):
            mkl_threading = "libmkl_tbb_thread"
            threading_engine_libs = self.tbb_libs
        elif self.spec.satisfies("threads=none"):
            mkl_threading = "libmkl_sequential"
            threading_engine_libs = LibraryList([])
        else:
            raise_lib_error("Cannot determine MKL threading libraries.")

        mkl_libnames = [mkl_integer, mkl_threading, "libmkl_core"]
        mkl_libs = find_libraries(
            mkl_libnames, root=self.component_lib_dir("mkl"), shared=("+shared" in self.spec)
        )
        debug_print(mkl_libs)

        if len(mkl_libs) < 3:
            raise_lib_error(
                "Cannot locate core MKL libraries:",
                mkl_libnames,
                "in:",
                self.component_lib_dir("mkl"),
            )

        # The Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            "libpthread libm libdl".split(), shared=("+shared" in self.spec)
        )
        debug_print(system_libs)

        return mkl_libs + threading_engine_libs + system_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        # Intel MKL does not directly depend on MPI but the BLACS library
        # which underlies ScaLapack does. It comes in several personalities;
        # we must supply a personality matching the MPI implementation that
        # is active for the root package that asked for ScaLapack.
        spec_root = self.spec.root
        if sys.platform == "darwin" and "^mpich" in spec_root:
            # The only supported choice for MKL 2018 on Mac.
            blacs_lib = "libmkl_blacs_mpich"
        elif "^openmpi" in spec_root:
            blacs_lib = "libmkl_blacs_openmpi"
        elif "^mpich@1" in spec_root:
            # Was supported only up to 2015.
            blacs_lib = "libmkl_blacs"
        elif (
            "^mpich@2:" in spec_root
            or "^cray-mpich" in spec_root
            or "^mvapich2" in spec_root
            or "^mvapich" in spec_root
            or "^intel-mpi" in spec_root
            or "^intel-oneapi-mpi" in spec_root
            or "^intel-parallel-studio" in spec_root
        ):
            blacs_lib = "libmkl_blacs_intelmpi"
        elif "^mpt" in spec_root:
            blacs_lib = "libmkl_blacs_sgimpt"
        else:
            raise_lib_error("Cannot find a BLACS library for the given MPI.")

        int_suff = "_" + self.intel64_int_suffix
        scalapack_libnames = ["libmkl_scalapack" + int_suff, blacs_lib + int_suff]
        sca_libs = find_libraries(
            scalapack_libnames, root=self.component_lib_dir("mkl"), shared=("+shared" in self.spec)
        )
        debug_print(sca_libs)

        if len(sca_libs) < 2:
            raise_lib_error("Cannot locate ScaLapack/BLACS libraries:", scalapack_libnames)
        # NB: ScaLapack is installed as "cluster" components within MKL or
        # MKL-encompassing products.  But those were *optional* for the ca.
        # 2015/2016 product releases, which was easy to overlook, and I have
        # been bitten by that.  Thus, complain early because it'd be a sore
        # disappointment to have missing ScaLapack libs show up as a link error
        # near the end phase of a client package's build phase.

        return sca_libs

    # ---------------------------------------------------------------------
    # Support for virtual 'mpi'
    # ---------------------------------------------------------------------
    @property
    def mpi_compiler_wrappers(self):
        """Return paths to compiler wrappers as a dict of env-like names"""
        # Intel comes with 2 different flavors of MPI wrappers:
        #
        # * mpiicc, mpiicpc, and mpiifort are hardcoded to wrap around
        #   the Intel compilers.
        # * mpicc, mpicxx, mpif90, and mpif77 allow you to set which
        #   compilers to wrap using I_MPI_CC and friends. By default,
        #   wraps around the GCC compilers.
        #
        # In theory, these should be equivalent as long as I_MPI_CC
        # and friends are set to point to the Intel compilers, but in
        # practice, mpicc fails to compile some applications while
        # mpiicc works.
        bindir = self.component_bin_dir("mpi")
        if self.compiler.name == "intel":
            wrapper_vars = {
                # eschew Prefix objects -- emphasize the command strings.
                "MPICC": os.path.join(bindir, "mpiicc"),
                "MPICXX": os.path.join(bindir, "mpiicpc"),
                "MPIF77": os.path.join(bindir, "mpiifort"),
                "MPIF90": os.path.join(bindir, "mpiifort"),
                "MPIFC": os.path.join(bindir, "mpiifort"),
            }
        else:
            wrapper_vars = {
                "MPICC": os.path.join(bindir, "mpicc"),
                "MPICXX": os.path.join(bindir, "mpicxx"),
                "MPIF77": os.path.join(bindir, "mpif77"),
                "MPIF90": os.path.join(bindir, "mpif90"),
                "MPIFC": os.path.join(bindir, "mpif90"),
            }
        # debug_print("wrapper_vars =", wrapper_vars)
        return wrapper_vars

    def mpi_setup_dependent_build_environment(self, env, dependent_spec, compilers_of_client={}):
        """Unified back-end for setup_dependent_build_environment() of
        Intel packages that provide 'mpi'.

        Parameters:

            env, dependent_spec: same as in
                setup_dependent_build_environment().

            compilers_of_client (dict): Conveys spack_cc, spack_cxx, etc.,
                from the scope of dependent packages; constructed in caller.
        """
        # See also: setup_dependent_package()
        wrapper_vars = {
            "I_MPI_CC": compilers_of_client["CC"],
            "I_MPI_CXX": compilers_of_client["CXX"],
            "I_MPI_F77": compilers_of_client["F77"],
            "I_MPI_F90": compilers_of_client["F90"],
            "I_MPI_FC": compilers_of_client["FC"],
            # NB: Normally set by the modulefile, but that is not active here:
            "I_MPI_ROOT": self.normalize_path("mpi"),
        }

        compiler_wrapper_commands = self.mpi_compiler_wrappers
        wrapper_vars.update(
            {
                "MPICC": compiler_wrapper_commands["MPICC"],
                "MPICXX": compiler_wrapper_commands["MPICXX"],
                "MPIF77": compiler_wrapper_commands["MPIF77"],
                "MPIF90": compiler_wrapper_commands["MPIF90"],
            }
        )

        # Ensure that the directory containing the compiler wrappers is in the
        # PATH. Spack packages add `prefix.bin` to their dependents' paths,
        # but because of the intel directory hierarchy that is insufficient.
        env.prepend_path("PATH", os.path.dirname(wrapper_vars["MPICC"]))

        for key, value in wrapper_vars.items():
            env.set(key, value)

        debug_print("adding to build env:", wrapper_vars)

    # ---------------------------------------------------------------------
    # General support for child packages
    # ---------------------------------------------------------------------
    @property
    def headers(self):
        result = HeaderList([])
        if "+mpi" in self.spec or self.provides("mpi"):
            result += find_headers(
                ["mpi"], root=self.component_include_dir("mpi"), recursive=False
            )
        if "+mkl" in self.spec or self.provides("mkl"):
            result += find_headers(
                ["mkl_cblas", "mkl_lapacke"],
                root=self.component_include_dir("mkl"),
                recursive=False,
            )
        if "+tbb" in self.spec or self.provides("tbb"):
            result += self.tbb_headers

        debug_print(result)
        return result

    @property
    def libs(self):
        result = LibraryList([])
        if "+tbb" in self.spec or self.provides("tbb"):
            result = self.tbb_libs + result
        if "+mkl" in self.spec or self.provides("blas"):
            result = self.blas_libs + result
        if "+mkl" in self.spec or self.provides("lapack"):
            result = self.lapack_libs + result
        if "+mpi" in self.spec or self.provides("mpi"):
            # If prefix is too general, recursive searches may get files from
            # supported but inappropriate sub-architectures like 'mic'.
            libnames = ["libmpifort", "libmpi"]
            if "cxx" in self.spec.last_query.extra_parameters:
                libnames = ["libmpicxx"] + libnames
            result = (
                find_libraries(
                    libnames, root=self.component_lib_dir("mpi"), shared=True, recursive=True
                )
                + result
            )
            # Intel MPI since 2019 depends on libfabric which is not in the
            # lib directory but in a directory of its own which should be
            # included in the rpath
            if self.version_yearlike >= Version("2019"):
                d = ancestor(self.component_lib_dir("mpi"))
                if "+external-libfabric" in self.spec:
                    result += self.spec["libfabric"].libs
                else:
                    result += find_libraries(["libfabric"], os.path.join(d, "libfabric", "lib"))

        if "^mpi" in self.spec.root and ("+mkl" in self.spec or self.provides("scalapack")):
            result = self.scalapack_libs + result

        debug_print(result)
        return result

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source parallel_studio_xe_2017/bin/psxevars.sh intel64
           [and likewise for MKL, MPI, and other components]
        """
        f = self.file_to_source
        tty.debug("sourcing " + f)

        # All Intel packages expect at least the architecture as argument.
        # Some accept more args, but those are not (yet?) handled here.
        args = (_expand_fields("{arch}"),)

        # On Mac, the platform is *also required*, at least as of 2018.
        # I am not sure about earlier versions.
        # if sys.platform == 'darwin':
        #     args = ()

        env.extend(EnvironmentModifications.from_sourcing_file(f, *args))

        if self.spec.name in ("intel", "intel-parallel-studio"):
            # this package provides compilers
            # TODO: fix check above when compilers are dependencies
            env.set("CC", self.prefix.bin.icc)
            env.set("CXX", self.prefix.bin.icpc)
            env.set("FC", self.prefix.bin.ifort)
            env.set("F77", self.prefix.bin.ifort)
            env.set("F90", self.prefix.bin.ifort)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # NB: This function is overwritten by 'mpi' provider packages:
        #
        # var/spack/repos/builtin/packages/intel-mpi/package.py
        # var/spack/repos/builtin/packages/intel-parallel-studio/package.py
        #
        # They call _setup_dependent_env_callback() as well, but with the
        # dictionary kwarg compilers_of_client{} present and populated.

        # Handle everything in a callback version.
        self._setup_dependent_env_callback(env, dependent_spec)

    def _setup_dependent_env_callback(self, env, dependent_spec, compilers_of_client={}):
        # Expected to be called from a client's
        # setup_dependent_build_environment(),
        # with args extended to convey the client's compilers as needed.

        if "+mkl" in self.spec or self.provides("mkl"):
            # Spack's env philosophy demands that we replicate some of the
            # settings normally handled by file_to_source ...
            #
            # TODO: Why is setup_run_environment()
            # [which uses file_to_source()]
            # not called as a matter of course upon entering the current
            # function? (guarding against multiple calls notwithstanding)
            #
            # Use a local dict to facilitate debug_print():
            env_mods = {
                "MKLROOT": self.normalize_path("mkl"),
                "SPACK_COMPILER_EXTRA_RPATHS": self.component_lib_dir("mkl"),
                "CMAKE_PREFIX_PATH": self.normalize_path("mkl"),
                "CMAKE_LIBRARY_PATH": self.component_lib_dir("mkl"),
                "CMAKE_INCLUDE_PATH": self.component_include_dir("mkl"),
                "PKG_CONFIG_PATH": os.path.join(self.normalize_path("mkl"), "bin", "pkgconfig"),
            }

            env.set("MKLROOT", env_mods["MKLROOT"])
            env.append_path("SPACK_COMPILER_EXTRA_RPATHS", env_mods["SPACK_COMPILER_EXTRA_RPATHS"])
            env.append_path("CMAKE_PREFIX_PATH", env_mods["CMAKE_PREFIX_PATH"])
            env.append_path("CMAKE_LIBRARY_PATH", env_mods["CMAKE_LIBRARY_PATH"])
            env.append_path("CMAKE_INCLUDE_PATH", env_mods["CMAKE_INCLUDE_PATH"])
            env.append_path("PKG_CONFIG_PATH", env_mods["PKG_CONFIG_PATH"])

            debug_print("adding/modifying build env:", env_mods)

        if "+mpi" in self.spec or self.provides("mpi"):
            if compilers_of_client:
                self.mpi_setup_dependent_build_environment(
                    env, dependent_spec, compilers_of_client
                )
                # We could forego this nonce function and inline its code here,
                # but (a) it sisters mpi_compiler_wrappers() [needed twice]
                # which performs dizzyingly similar but necessarily different
                # actions, and (b) function code leaves a bit more breathing
                # room within the suffocating corset of flake8 line length.
            else:
                raise InstallError("compilers_of_client arg required for MPI")

    def setup_dependent_package(self, module, dep_spec):
        # https://spack.readthedocs.io/en/latest/spack.html#spack.package_base.PackageBase.setup_dependent_package
        # Reminder: "module" refers to Python module.
        # Called before the install() method of dependents.

        if "+mpi" in self.spec or self.provides("mpi"):
            compiler_wrapper_commands = self.mpi_compiler_wrappers
            self.spec.mpicc = compiler_wrapper_commands["MPICC"]
            self.spec.mpicxx = compiler_wrapper_commands["MPICXX"]
            self.spec.mpif77 = compiler_wrapper_commands["MPIF77"]
            self.spec.mpifc = compiler_wrapper_commands["MPIFC"]
            debug_print(
                ("spec '%s' received .mpi* properties:" % self.spec), compiler_wrapper_commands
            )

    # ---------------------------------------------------------------------
    # Specifics for installation phase
    # ---------------------------------------------------------------------
    @property
    def global_license_file(self):
        """Returns the path where a Spack-global license file should be stored.

        All Intel software shares the same license, so we store it in a
        common 'intel' directory."""
        return os.path.join(self.global_license_dir, "intel", "license.lic")

    @property
    def _determine_license_type(self):
        """Provide appropriate license tokens for the installer (silent.cfg)."""
        # See:
        #   ./README-intel.rst, section "Details for licensing tokens".
        #   ./build_systems/README-intel.rst, section "Licenses"
        #
        # Ideally, we just tell the installer to look around on the system.
        # Thankfully, we neither need to care nor emulate where it looks:
        license_type = {"ACTIVATION_TYPE": "exist_lic"}

        # However (and only), if the spack-internal Intel license file has been
        # populated beyond its templated explanatory comments, proffer it to
        # the installer instead:
        f = self.global_license_file
        if os.path.isfile(f):
            # The file will have been created upon self.license_required AND
            # self.license_files having been populated, so the "if" is usually
            # true by the time the present function runs; ../hooks/licensing.py
            with open(f) as fh:
                if re.search(r"^[ \t]*[^" + self.license_comment + "\n]", fh.read(), re.MULTILINE):
                    license_type = {
                        "ACTIVATION_TYPE": "license_file",
                        "ACTIVATION_LICENSE_FILE": f,
                    }

        debug_print(license_type)
        return license_type

    @spack.builder.run_before("install")
    def configure(self):
        """Generates the silent.cfg file to pass to installer.sh.

        See https://software.intel.com/en-us/articles/configuration-file-format
        """
        prefix = self.prefix
        # Both tokens AND values of the configuration file are validated during
        # the run of the underlying binary installer. Any unknown token or
        # unacceptable value will cause that installer to fail.  Notably, this
        # applies to trying to specify a license for a product that does not
        # require one.
        #
        # Fortunately, the validator is a script from a solid code base that is
        # only lightly adapted to the token vocabulary of each product and
        # release.  Let's get that script so we can preempt its objections.
        #
        # Rather than running the script on a trial file and dissecting its
        # pronouncements, let's brazenly skim it for supported tokens and build
        # our configuration accordingly. We can do this because the tokens are
        # quite long and specific.

        validator_code = open("pset/check.awk", "r").read()
        # Let's go a little further and distill the tokens (plus some noise).
        tokenlike_words = set(re.findall(r"[A-Z_]{4,}", validator_code))

        # NB: .cfg files generated with the "--duplicate filename" option have
        # the COMPONENTS string begin with a separator - do not worry about it.
        components_joined = ";".join(self._filtered_components)
        nonrpm_db_dir = os.path.join(prefix, "nonrpm-db")

        config_draft = {
            # Basics first - these should be accepted in all products.
            "ACCEPT_EULA": "accept",
            "PSET_MODE": "install",
            "CONTINUE_WITH_OPTIONAL_ERROR": "yes",
            "CONTINUE_WITH_INSTALLDIR_OVERWRITE": "yes",
            "SIGNING_ENABLED": "no",
            # Highly variable package specifics:
            "PSET_INSTALL_DIR": prefix,
            "NONRPM_DB_DIR": nonrpm_db_dir,
            "COMPONENTS": components_joined,
            # Conditional tokens; the first is supported post-2015 only.
            # Ignore ia32; most recent products don't even provide it.
            "ARCH_SELECTED": "INTEL64",  # was: 'ALL'
            # 'ism' component -- see uninstall_ism(); also varies by release.
            "PHONEHOME_SEND_USAGE_DATA": "no",
            # Ah, as of 2018.2, that somewhat loaded term got replaced by one
            # in business-speak. We uphold our preference, both out of general
            # principles and for technical reasons like overhead and non-routed
            # compute nodes.
            "INTEL_SW_IMPROVEMENT_PROGRAM_CONSENT": "no",
        }
        # Deal with licensing only if truly needed.
        # NB: Token was 'ACTIVATION' pre ~2013, so basically irrelevant here.
        if "ACTIVATION_TYPE" in tokenlike_words:
            config_draft.update(self._determine_license_type)

        # Write sorted *by token* so the file looks less like a hash dump.
        f = open("silent.cfg", "w")
        for token, value in sorted(config_draft.items()):
            if token in tokenlike_words:
                f.write("%s=%s\n" % (token, value))
        f.close()

    def install(self, spec, prefix):
        """Runs Intel's install.sh installation script. Afterwards, save the
        installer config and logs to <prefix>/.spack
        """
        # prepare
        tmpdir = tempfile.mkdtemp(prefix="spack-intel-")

        install_script = Executable("./install.sh")
        install_script.add_default_env("TMPDIR", tmpdir)

        # Need to set HOME to avoid using ~/intel
        install_script.add_default_env("HOME", prefix)

        # perform
        install_script("--silent", "silent.cfg")

        # preserve config and logs
        dst = os.path.join(self.prefix, ".spack")
        install("silent.cfg", dst)
        for f in glob.glob("%s/intel*log" % tmpdir):
            install(f, dst)

    @spack.builder.run_after("install")
    def validate_install(self):
        # Sometimes the installer exits with an error but doesn't pass a
        # non-zero exit code to spack. Check for the existence of a 'bin'
        # directory to catch this error condition.
        if not os.path.exists(self.prefix.bin):
            raise InstallError("The installer has failed to install anything.")

    @spack.builder.run_after("install")
    def configure_rpath(self):
        if "+rpath" not in self.spec:
            return

        # https://software.intel.com/en-us/cpp-compiler-18.0-developer-guide-and-reference-using-configuration-files
        compilers_bin_dir = self.component_bin_dir("compiler")
        compilers_lib_dir = self.component_lib_dir("compiler")

        for compiler_name in "icc icpc ifort".split():
            f = os.path.join(compilers_bin_dir, compiler_name)
            if not os.path.isfile(f):
                raise InstallError("Cannot find compiler command to configure rpath:\n\t" + f)

            compiler_cfg = os.path.abspath(f + ".cfg")
            with open(compiler_cfg, "w") as fh:
                fh.write("-Xlinker -rpath={0}\n".format(compilers_lib_dir))

    @spack.builder.run_after("install")
    def configure_auto_dispatch(self):
        if self._has_compilers:
            if "auto_dispatch=none" in self.spec:
                return

            compilers_bin_dir = self.component_bin_dir("compiler")

            for compiler_name in "icc icpc ifort".split():
                f = os.path.join(compilers_bin_dir, compiler_name)
                if not os.path.isfile(f):
                    raise InstallError(
                        "Cannot find compiler command to configure " "auto_dispatch:\n\t" + f
                    )

                ad = []
                for x in IntelPackage.auto_dispatch_options:
                    if "auto_dispatch={0}".format(x) in self.spec:
                        ad.append(x)

                compiler_cfg = os.path.abspath(f + ".cfg")
                with open(compiler_cfg, "a") as fh:
                    fh.write("-ax{0}\n".format(",".join(ad)))

    @spack.builder.run_after("install")
    def filter_compiler_wrappers(self):
        if ("+mpi" in self.spec or self.provides("mpi")) and "~newdtags" in self.spec:
            bin_dir = self.component_bin_dir("mpi")
            for f in "mpif77 mpif90 mpigcc mpigxx mpiicc mpiicpc " "mpiifort".split():
                f = os.path.join(bin_dir, f)
                filter_file("-Xlinker --enable-new-dtags", " ", f, string=True)

    @spack.builder.run_after("install")
    def uninstall_ism(self):
        # The "Intel(R) Software Improvement Program" [ahem] gets installed,
        # apparently regardless of PHONEHOME_SEND_USAGE_DATA.
        #
        # https://software.intel.com/en-us/articles/software-improvement-program
        # https://software.intel.com/en-us/forums/intel-c-compiler/topic/506959
        # Hubert H. (Intel)  Mon, 03/10/2014 - 03:02 wrote:
        #  "... you can also uninstall the Intel(R) Software Manager
        #  completely: <installdir>/intel/ism/uninstall.sh"

        f = os.path.join(self.normalize_path("ism"), "uninstall.sh")
        if os.path.isfile(f):
            tty.warn('Uninstalling "Intel Software Improvement Program"' "component")
            uninstall = Executable(f)
            uninstall("--silent")

        # TODO? also try
        #   ~/intel/ism/uninstall --silent

        debug_print(os.getcwd())
        return

    @property
    def base_lib_dir(self):
        """Provide the library directory located in the base of Intel installation."""
        d = self.normalize_path("")
        d = os.path.join(d, "lib")

        debug_print(d)
        return d

    @spack.builder.run_after("install")
    def modify_LLVMgold_rpath(self):
        """Add libimf.so and other required libraries to the RUNPATH of LLVMgold.so.

        These are needed explicitly at dependent link time when
        `ld -plugin LLVMgold.so` is called by the compiler.
        """
        if self._has_compilers:
            LLVMgold_libs = find_libraries(
                "LLVMgold", self.base_lib_dir, shared=True, recursive=True
            )
            # Ignore ia32 entries as they mostly ignore throughout the rest
            # of the file.
            # The first entry in rpath preserves the original, the seconds entry
            # is the location of libimf.so. If this relative location is changed
            # in compiler releases, then we need to search for libimf.so instead
            # of this static path.
            for lib in LLVMgold_libs:
                if not self.spec.satisfies("^patchelf"):
                    raise spack.error.SpackError(
                        "Attempting to patch RPATH in LLVMgold.so."
                        + "`patchelf` dependency should be set in package.py"
                    )
                patchelf = Executable("patchelf")
                rpath = ":".join(
                    [
                        patchelf("--print-rpath", lib, output=str).strip(),
                        "$ORIGIN/../compiler/lib/intel64_lin",
                    ]
                )
                patchelf("--set-rpath", rpath, lib)
