#!/bin/sh
#
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This script tests that Spack's tab completion scripts work.
#
# The tests are portable to bash, zsh, and bourne shell, and can be run
# in any of these shells.
#

export QA_DIR=$(dirname "$0")
export SHARE_DIR=$(cd "$QA_DIR/.." && pwd)
export SPACK_ROOT=$(cd "$QA_DIR/../../.." && pwd)

. "$QA_DIR/test-framework.sh"

# Fail on undefined variables
set -u

# Source setup-env.sh before tests
. "$SHARE_DIR/setup-env.sh"
. "$SHARE_DIR/spack-completion.$_sp_shell"

title "Testing spack-completion.$_sp_shell with $_sp_shell"

# Spack command is now available
succeeds which spack

title 'Testing all subcommands'
# read line into an array portably
READ="read -ra line"
if [ -n "${ZSH_VERSION:-}" ]; then
  READ=(read -rA line)
fi
while IFS=' ' $READ
do
    # Test that completion with no args works
    succeeds _spack_completions "${line[@]}" ''

    # Test that completion with flags works
    # all commands but spack pkg grep have -h; all have --help
    contains '--help' _spack_completions "${line[@]}" -
done <<- EOF
    $(spack commands --aliases --format=subcommands)
EOF

title 'Testing for correct output'
contains 'compiler' _spack_completions spack ''
contains 'install' _spack_completions spack inst
contains 'find' _spack_completions spack help ''
contains 'hdf5' _spack_completions spack list ''
contains 'py-numpy' _spack_completions spack list py-
contains 'mpi' _spack_completions spack providers ''
contains 'builtin' _spack_completions spack repo remove ''
contains 'packages' _spack_completions spack config edit ''
contains 'python' _spack_completions spack extensions ''
contains 'hdf5' _spack_completions spack -d install --jobs 8 ''
contains 'hdf5' _spack_completions spack install -v ''

title 'Testing alias handling'
contains 'concretize' _spack_completions spack c
contains 'concretise' _spack_completions spack c
contains 'concretize' _spack_completions spack conc
does_not_contain 'concretise' _spack_completions spack conc

does_not_contain 'concretize' _spack_completions spack isnotacommand
does_not_contain 'concretize' _spack_completions spack env isnotacommand

# XFAIL: Fails for Python 2.6 because pkg_resources not found?
#contains 'compilers.py' _spack_completions spack unit-test ''

_test_debug_functions() {
    title 'Testing debugging functions'

    if [ -n "${ZSH_VERSION:-}" ]; then
        emulate -L sh
    fi

    # Test whether `spack install --verb[] spec` completes to `spack install --verbose spec`
    COMP_LINE='spack install --verb spec'
    COMP_POINT=20
    COMP_WORDS=(spack install --verb spec)
    COMP_CWORD=2
    COMP_KEY=9
    COMP_TYPE=64
    _bash_completion_spack
    contains "--verbose" echo "${COMPREPLY[@]}"

    # This is a particularly tricky case that involves the following situation:
    #     `spack -d [] install `
    # Here, [] represents the cursor, which is in the middle of the line.
    # We should tab-complete optional flags for `spack`, not optional flags for
    # `spack install` or package names.
    COMP_LINE='spack -d  install '
    COMP_POINT=9
    COMP_WORDS=(spack -d install)
    COMP_CWORD=2
    COMP_KEY=9
    COMP_TYPE=64

    _bash_completion_spack
    contains "--all-help" echo "${COMPREPLY[@]}"

    contains "['spack', '-d', 'install', '']" _pretty_print COMP_WORDS[@]

    # Set the rest of the intermediate variables manually
    COMP_WORDS_NO_FLAGS=(spack install)
    COMP_CWORD_NO_FLAGS=1
    subfunction=_spack
    cur=

    list_options=true
    contains "'True'" _test_vars
    list_options=false
    contains "'False'" _test_vars
}
_test_debug_functions
