#!/bin/sh

# _spack_env_set VARNAME VALUE
#
# Set the VARNAME variable to VALUE.
_spack_env_set() {}

# _spack_env_unset VARNAME
#
# Unset VARNAME in the environment.
_spack_env_unset() {}

# _spack_env_append_flags VARNAME FLAG SEP
#
# Append FLAG to the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_append() {}

# _spack_env_prepend_flags VARNAME FLAG SEP
#
# Prepend FLAG to the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_prepend() {}

# _spack_env_remove_flags VARNAME FLAG SEP
#
# Remove FLAG from the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_remove() {}

# _spack_env_prune_duplicate_paths VARNAME SEP
#
# Remove duplicate elements from the list in variable
# VARNAME, preserving precedence.
#
# The list in VARNAME is separated by the SEP character.
_spack_env_prune_duplicates() {}