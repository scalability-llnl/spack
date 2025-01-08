#!/bin/sh

# _spack_env_set VARNAME VALUE
#
# Set the VARNAME variable to VALUE.
_spack_env_set() {
    VARNAME = $1
    VALUE = $2

    export ${${VARNAME}}=${VALUE}
}

# _spack_env_unset VARNAME
#
# Unset VARNAME in the environment.
_spack_env_unset() {
    VARNAME = $1

    export ${${VARNAME}}=""
}

# _spack_env_append VARNAME VALUE SEP
#
# Append VALUE to the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_append() {
    VARNAME = $1
    VALUE = $2
    SEP = $3

    export ${${VARNAME}}=${${VARNAME}}${SEP}${VALUE}
}

# _spack_env_prepend VARNAME VALUE SEP
#
# Prepend VALUE to the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_prepend() {
    VARNAME = $1
    VALUE = $2
    SEP = $3

    export ${${VARNAME}}=${VALUE}${SEP}${${VARNAME}}
    # Should the result be a string? Might need quotes
}

# _spack_env_remove VARNAME VALUE SEP
#
# Remove VALUE from the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_remove() {
    VARNAME = $1
    VALUE = $2
    SEP = $3

    if [ ${${VARNAME}} == ${VALUE} ];
    then
        ${${VARNAME}} = ""

    else
        echo "Find a way to remove the VALUE"
    fi
}

# _spack_env_prune_duplicate VARNAME SEP
#
# Remove duplicate elements from the list in variable
# VARNAME, preserving precedence.
#
# The list in VARNAME is separated by the SEP character.
_spack_env_prune_duplicates() {}