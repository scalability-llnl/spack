#!/bin/sh


_value_in_varname () {
    VARNAME="$1"
    VALUE="$2"
    SEP="$3"

    if eval "[ -n \"\${${VARNAME}}\" ]"; then
        if eval "[ \"\${${VARNAME}}\" == \"$VALUE\" ] ||
            [ \"\${${VARNAME}}\" == ^\"$VALUE$SEP\"* ] ||
            [ \"\${${VARNAME}}\" == *\"$SEP$VALUE$SEP\"* ] ||
            [ \"\${${VARNAME}}\" == *\"$SEP$VALUE\" ]"; then
            return 0
        fi
    fi
    return 1
}

# _spack_env_set VARNAME VALUE
#
# Set the VARNAME variable to VALUE.
_spack_env_set() {
    VARNAME="$1"
    VALUE="$2"

    export $VARNAME="$VALUE"
}

# _spack_env_unset VARNAME
#
# Unset VARNAME in the environment.
_spack_env_unset() {
    VARNAME="$1"

    unset "$VARNAME"
}

# _spack_env_append VARNAME VALUE SEP
#
# Append VALUE to the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_append() {
    VARNAME="$1"
    VALUE="$2"
    SEP="$3"

    if eval "[ -n \"\${${VARNAME}}\" ]"; then
        if [ "$(_value_in_varname $VARNAME $VALUE)" == 1 ] ; then
            eval "export $VARNAME=\${${VARNAME}}$SEP$VALUE"
        fi
    else
        export $VARNAME="$VALUE"
    fi
}

# _spack_env_prepend VARNAME VALUE SEP
#
# Prepend VALUE to the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_prepend() { # if not exporting then use lowercase
    VARNAME="$1"
    VALUE="$2"
    SEP="$3" # how to set if no $3

   if eval "[ -n \"\${${VARNAME}}\" ]"; then
        if [ "$(_value_in_varname $VARNAME $VALUE)" == 1 ] ; then
            eval "export $VARNAME=$VALUE$SEP\${${VARNAME}}"
        fi
    else
        export $VARNAME="$VALUE"
    fi
}

# _spack_env_remove VARNAME VALUE SEP
#
# Remove VALUE from the flag list in variable VARNAME.
# The list in VARNAME is separated by the SEP character.
_spack_env_remove() { # look into sed
    VARNAME="$1"
    VALUE="$2"
    SEP="$3"

    VARNAME_VALUE=\${${VARNAME}}


    eval "echo \"${VARNAME_VALUE[@]/other*/}\""
    eval echo "${VARNAME/\$VALUE}"

    if [ $VARNAME == *"$VALUE"* ]; then
        ${${VARNAME}} = ""

    else
        echo "Find a way to remove the VALUE"
        # ${${VARNAME}} = ${VARNAME/${VALUE}/""}
    fi
}

# _spack_env_prune_duplicate VARNAME SEP
#
# Remove duplicate elements from the list in variable
# VARNAME, preserving precedence.
#
# The list in VARNAME is separated by the SEP character.
_spack_env_prune_duplicates() {
    echo
}
