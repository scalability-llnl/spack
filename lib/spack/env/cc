#!/bin/bash
#
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Spack compiler wrapper script.
#
# Compiler commands go through this compiler wrapper in Spack builds.
# The compiler wrapper is a thin layer around the standard compilers.
# It enables several key pieces of functionality:
#
# 1. It allows Spack to swap compilers into and out of builds easily.
# 2. It adds several options to the compile line so that spack
#    packages can find their dependencies at build time and run time:
#      -I and/or -isystem arguments for dependency /include directories.
#      -L                 arguments for dependency /lib directories.
#      -Wl,-rpath         arguments for dependency /lib directories.
#

# This is an array of environment variables that need to be set before
# the script runs. They are set by routines in spack.build_environment
# as part of the package installation process.
parameters=(
    SPACK_ENV_PATH
    SPACK_DEBUG_LOG_DIR
    SPACK_DEBUG_LOG_ID
    SPACK_COMPILER_SPEC
    SPACK_CC_RPATH_ARG
    SPACK_CXX_RPATH_ARG
    SPACK_F77_RPATH_ARG
    SPACK_FC_RPATH_ARG
    SPACK_TARGET_ARGS
    SPACK_DTAGS_TO_ADD
    SPACK_DTAGS_TO_STRIP
    SPACK_LINKER_ARG
    SPACK_SHORT_SPEC
    SPACK_SYSTEM_DIRS
)

# The compiler input variables are checked for sanity later:
#   SPACK_CC, SPACK_CXX, SPACK_F77, SPACK_FC
# The default compiler flags are passed from these variables:
#   SPACK_CFLAGS, SPACK_CXXFLAGS, SPACK_FFLAGS,
#   SPACK_LDFLAGS, SPACK_LDLIBS
# Debug env var is optional; set to "TRUE" for debug logging:
#   SPACK_DEBUG
# Test command is used to unit test the compiler script.
#   SPACK_TEST_COMMAND

# die()
# Prints a message and exits with error 1.
function die {
    echo "$@"
    exit 1
}

# read input parameters into proper bash arrays.
# SYSTEM_DIRS is delimited by :
IFS=':' read -ra SPACK_SYSTEM_DIRS <<< "${SPACK_SYSTEM_DIRS}"

# SPACK_<LANG>FLAGS and SPACK_LDLIBS are split by ' '
IFS=' ' read -ra SPACK_FFLAGS   <<< "$SPACK_FFLAGS"
IFS=' ' read -ra SPACK_CPPFLAGS <<< "$SPACK_CPPFLAGS"
IFS=' ' read -ra SPACK_CFLAGS   <<< "$SPACK_CFLAGS"
IFS=' ' read -ra SPACK_CXXFLAGS <<< "$SPACK_CXXFLAGS"
IFS=' ' read -ra SPACK_LDFLAGS  <<< "$SPACK_LDFLAGS"
IFS=' ' read -ra SPACK_LDLIBS   <<< "$SPACK_LDLIBS"

# test whether a path is a system directory
function system_dir {
    path="$1"
    for sd in "${SPACK_SYSTEM_DIRS[@]}"; do
        if [ "${path}" == "${sd}" ] || [ "${path}" == "${sd}/" ]; then
            # success if path starts with a system prefix
            return 0
        fi
    done
    return 1  # fail if path starts no system prefix
}

for param in "${parameters[@]}"; do
    if [[ -z ${!param+x} ]]; then
        die "Spack compiler must be run from Spack! Input '$param' is missing."
    fi
done

# Figure out the type of compiler, the language, and the mode so that
# the compiler script knows what to do.
#
# Possible languages are C, C++, Fortran 77, and Fortran 90.
# 'command' is set based on the input command to $SPACK_[CC|CXX|F77|F90]
#
# 'mode' is set to one of:
#    vcheck  version check
#    cpp     preprocess
#    cc      compile
#    as      assemble
#    ld      link
#    ccld    compile & link

command=$(basename "$0")
comp="CC"
case "$command" in
    cpp)
        mode=cpp
        ;;
    cc|c89|c99|gcc|clang|armclang|icc|icx|pgcc|nvc|xlc|xlc_r|fcc)
        command="$SPACK_CC"
        language="C"
        comp="CC"
        lang_flags=C
        ;;
    c++|CC|g++|clang++|armclang++|icpc|icpx|pgc++|nvc++|xlc++|xlc++_r|FCC)
        command="$SPACK_CXX"
        language="C++"
        comp="CXX"
        lang_flags=CXX
        ;;
    ftn|f90|fc|f95|gfortran|flang|armflang|ifort|ifx|pgfortran|nvfortran|xlf90|xlf90_r|nagfor|frt)
        command="$SPACK_FC"
        language="Fortran 90"
        comp="FC"
        lang_flags=F
        ;;
    f77|xlf|xlf_r|pgf77)
        command="$SPACK_F77"
        language="Fortran 77"
        comp="F77"
        lang_flags=F
        ;;
    ld)
        mode=ld
        ;;
    *)
        die "Unknown compiler: $command"
        ;;
esac

# If any of the arguments below are present, then the mode is vcheck.
# In vcheck mode, nothing is added in terms of extra search paths or
# libraries.
if [[ -z $mode ]] || [[ $mode == ld ]]; then
    for arg in "$@"; do
        case $arg in
            -v|-V|--version|-dumpversion)
                mode=vcheck
                break
                ;;
        esac
    done
fi

# Finish setting up the mode.
if [[ -z $mode ]]; then
    mode=ccld
    for arg in "$@"; do
        if [[ $arg == -E ]]; then
            mode=cpp
            break
        elif [[ $arg == -S ]]; then
            mode=as
            break
        elif [[ $arg == -c ]]; then
            mode=cc
            break
        fi
    done
fi

# This is needed to ensure we set RPATH instead of RUNPATH
# (or the opposite, depending on the configuration in config.yaml)
#
# Documentation on this mechanism is lacking at best. A few sources
# of information are (note that some of them take explicitly the
# opposite stance that Spack does):
#
# http://blog.qt.io/blog/2011/10/28/rpath-and-runpath/
# https://wiki.debian.org/RpathIssue
#
# The only discussion I could find on enabling new dynamic tags by
# default on ld is the following:
#
# https://sourceware.org/ml/binutils/2013-01/msg00307.html
#
dtags_to_add="${SPACK_DTAGS_TO_ADD}"
dtags_to_strip="${SPACK_DTAGS_TO_STRIP}"
linker_arg="${SPACK_LINKER_ARG}"

# Set up rpath variable according to language.
eval rpath=\$SPACK_${comp}_RPATH_ARG

# Dump the mode and exit if the command is dump-mode.
if [[ $SPACK_TEST_COMMAND == dump-mode ]]; then
    echo "$mode"
    exit
fi

# Check that at least one of the real commands was actually selected,
# otherwise we don't know what to execute.
if [[ -z $command ]]; then
    die "ERROR: Compiler '$SPACK_COMPILER_SPEC' does not support compiling $language programs."
fi

#
# Filter '.' and Spack environment directories out of PATH so that
# this script doesn't just call itself
#
IFS=':' read -ra env_path <<< "$PATH"
IFS=':' read -ra spack_env_dirs <<< "$SPACK_ENV_PATH"
spack_env_dirs+=("" ".")
export PATH=""
for dir in "${env_path[@]}"; do
    addpath=true
    for env_dir in "${spack_env_dirs[@]}"; do
        if [[ "$dir" == "$env_dir" ]]; then
            addpath=false
            break
        fi
    done
    if $addpath; then
        export PATH="${PATH:+$PATH:}$dir"
    fi
done

if [[ $mode == vcheck ]]; then
    exec "${command}" "$@"
fi

# Darwin's linker has a -r argument that merges object files together.
# It doesn't work with -rpath.
# This variable controls whether they are added.
add_rpaths=true
if [[ ($mode == ld || $mode == ccld) && "$SPACK_SHORT_SPEC" =~ "darwin" ]];
then
    for arg in "$@"; do
        if [[ ($arg == -r && $mode == ld) ||
              ($arg == -r && $mode == ccld) ||
              ($arg == -Wl,-r && $mode == ccld) ]]; then
            add_rpaths=false
            break
        fi
    done
fi

# Save original command for debug logging
input_command="$*"

#
# Parse the command line arguments.
#
# We extract -L, -I, -isystem and -Wl,-rpath arguments from the
# command line and recombine them with Spack arguments later.  We
# parse these out so that we can make sure that system paths come
# last, that package arguments come first, and that Spack arguments
# are injected properly.
#
# All other arguments, including -l arguments, are treated as
# 'other_args' and left in their original order.  This ensures that
# --start-group, --end-group, and other order-sensitive flags continue to
# work as the caller expects.
#
# The libs variable is initialized here for completeness, and it is also
# used later to inject flags supplied via `ldlibs` on the command
# line. These come into the wrappers via SPACK_LDLIBS.
#
includes=()
libdirs=()
rpaths=()
system_includes=()
system_libdirs=()
system_rpaths=()
libs=()
other_args=()
isystem_system_includes=()
isystem_includes=()

while [ $# -ne 0 ]; do

    # an RPATH to be added after the case statement.
    rp=""

    # Multiple consecutive spaces in the command line can
    # result in blank arguments
    if [ -z "$1" ]; then
        shift
        continue
    fi

    case "$1" in
        -isystem*)
            arg="${1#-isystem}"
            isystem_was_used=true
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if system_dir "$arg"; then
                isystem_system_includes+=("$arg")
            else
                isystem_includes+=("$arg")
            fi
            ;;
        -I*)
            arg="${1#-I}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if system_dir "$arg"; then
                system_includes+=("$arg")
            else
                includes+=("$arg")
            fi
            ;;
        -L*)
            arg="${1#-L}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if system_dir "$arg"; then
                system_libdirs+=("$arg")
            else
                libdirs+=("$arg")
            fi
            ;;
        -l*)
            # -loopopt=0 is passed to the linker erroneously in
            # autoconf <= 2.69. Filter it out.
            # TODO: generalize filtering of args with an env var, so that
            # TODO: we do not have to special case this here.
            if [ "$mode" = "ld" ] && [ "$1" != "${1#-loopopt}" ]; then
                shift
                continue
            fi
            arg="${1#-l}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            other_args+=("-l$arg")
            ;;
        -Wl,*)
            arg="${1#-Wl,}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if [[ "$arg" = -rpath=* ]]; then
                rp="${arg#-rpath=}"
            elif [[ "$arg" = --rpath=* ]]; then
                rp="${arg#--rpath=}"
            elif [[ "$arg" = -rpath,* ]]; then
                rp="${arg#-rpath,}"
            elif [[ "$arg" = --rpath,* ]]; then
                rp="${arg#--rpath,}"
            elif [[ "$arg" =~ ^-?-rpath$ ]]; then
                shift; arg="$1"
                if [[ "$arg" != -Wl,* ]]; then
                    die "-Wl,-rpath was not followed by -Wl,*"
                fi
                rp="${arg#-Wl,}"
            elif [[ "$arg" = "$dtags_to_strip" ]] ; then
                :  # We want to remove explicitly this flag
            else
                other_args+=("-Wl,$arg")
            fi
            ;;
        -Xlinker,*)
            arg="${1#-Xlinker,}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if [[ "$arg" = -rpath=* ]]; then
                rp="${arg#-rpath=}"
            elif [[ "$arg" = --rpath=* ]]; then
                rp="${arg#--rpath=}"
            elif [[ "$arg" = -rpath  ]] || [[ "$arg" = --rpath ]]; then
                shift; arg="$1"
                if [[ "$arg" != -Xlinker,* ]]; then
                    die "-Xlinker,-rpath was not followed by -Xlinker,*"
                fi
                rp="${arg#-Xlinker,}"
            else
                other_args+=("-Xlinker,$arg")
            fi
            ;;
        -Xlinker)
            if [[ "$2" == "-rpath" ]]; then
                if [[ "$3" != "-Xlinker" ]]; then
                    die "-Xlinker,-rpath was not followed by -Xlinker,*"
                fi
                shift 3;
                rp="$1"
            elif [[ "$2" = "$dtags_to_strip" ]] ; then
                shift  # We want to remove explicitly this flag
            else
                other_args+=("$1")
            fi
            ;;
        *)
            if [[ "$1" = "$dtags_to_strip" ]] ; then
                :  # We want to remove explicitly this flag
            else
                other_args+=("$1")
            fi
            ;;
    esac

    # test rpaths against system directories in one place.
    if [ -n "$rp" ]; then
        if system_dir "$rp"; then
            system_rpaths+=("$rp")
        else
            rpaths+=("$rp")
        fi
    fi
    shift
done

#
# Add flags from Spack's cppflags, cflags, cxxflags, fcflags, fflags, and
# ldflags. We stick to the order that gmake puts the flags in by default.
#
# See the gmake manual on implicit rules for details:
# https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html
#
flags=()

# Fortran flags come before CPPFLAGS
case "$mode" in
    cc|ccld)
        case $lang_flags in
            F)
                flags=("${flags[@]}" "${SPACK_FFLAGS[@]}") ;;
        esac
        ;;
esac

# C preprocessor flags come before any C/CXX flags
case "$mode" in
    cpp|as|cc|ccld)
        flags=("${flags[@]}" "${SPACK_CPPFLAGS[@]}") ;;
esac


# Add C and C++ flags
case "$mode" in
    cc|ccld)
        case $lang_flags in
            C)
                flags=("${flags[@]}" "${SPACK_CFLAGS[@]}") ;;
            CXX)
                flags=("${flags[@]}" "${SPACK_CXXFLAGS[@]}") ;;
        esac
        flags=(${SPACK_TARGET_ARGS[@]} "${flags[@]}")
        ;;
esac

# Linker flags
case "$mode" in
    ld|ccld)
        flags=("${flags[@]}" "${SPACK_LDFLAGS[@]}") ;;
esac

# On macOS insert headerpad_max_install_names linker flag
if [[ ($mode == ld || $mode == ccld) && "$SPACK_SHORT_SPEC" =~ "darwin" ]];
then
    case "$mode" in
        ld)
            flags=("${flags[@]}" -headerpad_max_install_names) ;;
        ccld)
            flags=("${flags[@]}" "-Wl,-headerpad_max_install_names") ;;
    esac
fi

IFS=':' read -ra rpath_dirs <<< "$SPACK_RPATH_DIRS"
if [[ $mode == ccld || $mode == ld ]]; then

    if [[ "$add_rpaths" != "false" ]] ; then
        # Append RPATH directories. Note that in the case of the
        # top-level package these directories may not exist yet. For dependencies
        # it is assumed that paths have already been confirmed.
        rpaths=("${rpaths[@]}" "${rpath_dirs[@]}")
    fi

fi

IFS=':' read -ra link_dirs <<< "$SPACK_LINK_DIRS"
if [[ $mode == ccld || $mode == ld ]]; then
    libdirs=("${libdirs[@]}" "${link_dirs[@]}")
fi

# add RPATHs if we're in in any linking mode
case "$mode" in
    ld|ccld)
        # Set extra RPATHs
        IFS=':' read -ra extra_rpaths <<< "$SPACK_COMPILER_EXTRA_RPATHS"
        libdirs+=("${extra_rpaths[@]}")
        if [[ "$add_rpaths" != "false" ]] ; then
            rpaths+=("${extra_rpaths[@]}")
        fi

        # Set implicit RPATHs
        IFS=':' read -ra implicit_rpaths <<< "$SPACK_COMPILER_IMPLICIT_RPATHS"
        if [[ "$add_rpaths" != "false" ]] ; then
            rpaths+=("${implicit_rpaths[@]}")
        fi

        # Add SPACK_LDLIBS to args
        for lib in "${SPACK_LDLIBS[@]}"; do
            libs+=("${lib#-l}")
        done
        ;;
esac

#
# Finally, reassemble the command line.
#

# Includes and system includes first
args=()

# flags assembled earlier
args+=("${flags[@]}")

# Insert include directories just prior to any system include directories

for dir in "${includes[@]}";         do args+=("-I$dir"); done
for dir in "${isystem_includes[@]}";         do args+=("-isystem" "$dir"); done

IFS=':' read -ra spack_include_dirs <<< "$SPACK_INCLUDE_DIRS"
if [[ $mode == cpp || $mode == cc || $mode == as || $mode == ccld ]]; then
    if [[ "$isystem_was_used" == "true" ]] ; then
        for dir in "${spack_include_dirs[@]}";  do args+=("-isystem" "$dir"); done
    else
        for dir in "${spack_include_dirs[@]}";  do args+=("-I$dir"); done
    fi
fi

for dir in "${system_includes[@]}";  do args+=("-I$dir"); done
for dir in "${isystem_system_includes[@]}";  do args+=("-isystem" "$dir"); done

# Library search paths
for dir in "${libdirs[@]}";          do args+=("-L$dir"); done
for dir in "${system_libdirs[@]}";   do args+=("-L$dir"); done

# RPATHs arguments
case "$mode" in
    ccld)
        if [ -n "$dtags_to_add" ] ; then args+=("$linker_arg$dtags_to_add") ; fi
        for dir in "${rpaths[@]}";        do args+=("$rpath$dir"); done
        for dir in "${system_rpaths[@]}"; do args+=("$rpath$dir"); done
        ;;
    ld)
        if [ -n "$dtags_to_add" ] ; then args+=("$dtags_to_add") ; fi
        for dir in "${rpaths[@]}";        do args+=("-rpath" "$dir"); done
        for dir in "${system_rpaths[@]}"; do args+=("-rpath" "$dir"); done
        ;;
esac

# Other arguments from the input command
args+=("${other_args[@]}")

# Inject SPACK_LDLIBS, if supplied
for lib in "${libs[@]}"; do
    args+=("-l$lib");
done

full_command=("$command" "${args[@]}")

# prepend the ccache binary if we're using ccache
if [ -n "$SPACK_CCACHE_BINARY" ]; then
    case "$lang_flags" in
        C|CXX)  # ccache only supports C languages
            full_command=("${SPACK_CCACHE_BINARY}" "${full_command[@]}")
            # workaround for stage being a temp folder
            # see #3761#issuecomment-294352232
            export CCACHE_NOHASHDIR=yes
            ;;
    esac
fi

# dump the full command if the caller supplies SPACK_TEST_COMMAND=dump-args
if [[ $SPACK_TEST_COMMAND == dump-args ]]; then
    IFS="
" && echo "${full_command[*]}"
    exit
elif [[ -n $SPACK_TEST_COMMAND ]]; then
    die "ERROR: Unknown test command"
fi

#
# Write the input and output commands to debug logs if it's asked for.
#
if [[ $SPACK_DEBUG == TRUE ]]; then
    input_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_DEBUG_LOG_ID.in.log"
    output_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_DEBUG_LOG_ID.out.log"
    echo "[$mode] $command $input_command" >> "$input_log"
    echo "[$mode] ${full_command[*]}" >> "$output_log"
fi

exec "${full_command[@]}"
