#!/bin/sh

# separator_exists sep
#
# Fails if separator argument was not supplied
separator_exists() {
    if [ -z "$1" ]; then
        echo "Missing argument: separator"
        exit 1
    fi
}

# _value_not_in_varname varname value sep
#
# Return whether the variable value is found in varname
_value_not_in_varname () {
    varname="$1"
    value="$2"
    sep="$3"

    eval "var=\"\${${varname}}\""

    echo "here $var"
    if eval "[ \"yes another one\" =~ \"*another*\" ]"; then
        echo "it's here"
    else
        echo "not here"
    fi

    if eval "[ \"\${${varname}}\" == \"$value\" ] ||
        [ \"\${${varname}}\" == ^\"$value$sep\"* ] ||
        [ \"\${${varname}}\" == *\"$sep$value$sep\"* ] ||
        [ \"\${${varname}}\" == *\"$sep$value\" ]"; then
            echo "1"
            false
    fi
    echo "0"
    true
}

# _spack_env_varname_is_empty varname
#
# Return whether the variable varname is unset or set to the empty string.
_spack_env_varname_is_empty() {
    eval "test -z \"\${$1}\""
}

# _spack_env_set varname value
#
# Set the varname variable to value.
_spack_env_set() {
    varname="$1"
    value="$2"

    export $varname="$value"
}

# _spack_env_unset varname
#
# Unset varname in the environment.
_spack_env_unset() {
    varname="$1"

    unset "$varname"
}

# _spack_env_append varname value sep
#
# Append value to the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_append() {
    varname="$1"
    value="$2"
    sep="$3"

    $(separator_exists $sep)

    if _spack_env_varname_is_empty "$varname"; then
        eval "$varname=\"\${value}\""
    else
        echo "in else"
        echo "$(_value_not_in_varname $varname $value $sep)"
        if [ "$(_value_not_in_varname $varname $value $sep)" ] ; then
            echo "setting"
            eval "export $varname=\${${varname}}$sep$value"
        fi
    fi
}

# _spack_env_prepend varname value sep
#
# Prepend value to the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_prepend() { # if not exporting then use lowercase
    varname="$1"
    value="$2"
    sep="$3"

    $(separator_exists $sep)

   if _spack_env_varname_is_empty "$varname"; then
        eval "$varname=\"\${value}\""
    else
        if [ "$(_value_not_in_varname $varname $value $sep)" ] ; then
            eval "export $varname=$value$sep\${${varname}}"
        fi
    fi
}

# _spack_env_remove varname value sep
#
# Remove value from the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_remove() { # look into sed
    varname="$1"
    value="$2"
    sep="$3"

    $(separator_exists $sep)

    eval "varname_value=\"\${${varname}}\""

    # if varname's only value is $value
    if eval "[ \"$varname_value\" == \"$value\" ]"; then
        export $varname=""
    else
        # if value is at the beginning or middle  of the string
        if [ "$varname_value" == ^"$value$sep"* ] ||
            [ "$varname_value" == *"$sep$value$sep"* ]; then
            eval "export $varname=\"${varname_value[@]/$value$sep/}\""
        # if value is at the end of the string
        elif [ "$varname_value" == *"$sep$value" ]; then
            eval "export $varname=\"${varname_value[@]/$sep$value/}\""
    fi
}

# _spack_env_prune_duplicate varname sep
#
# Remove duplicate elements from the list in variable
# varname, preserving precedence.
#
# The list in varname is separated by the sep character.
_spack_env_prune_duplicates() {
    echo
}
