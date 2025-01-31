#!/bin/sh

# _separator_exists sep
#
# Fails if separator argument was not supplied
_separator_exists() {
    if [ -z "$1" ]; then
        echo "Missing argument: separator"
        exit 1
    fi
}

# _value_in_varname varname value sep
#
# Return whether the variable value is found in varname
_value_in_varname () {
    varname="$1"
    value="$2"
    sep="$3"

    eval "var=\"\${${varname}}\""

    if  [ "${var#*$value}" != "$var" ]; then
            value_in_varname=0
    fi

    return $value_in_varname
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

    $(_separator_exists $sep)

    if _spack_env_var_empty "$varname"; then
        eval "$varname=\"\${value}\""
    else
        $(_value_in_varname $varname $value $sep)
        if [ $? -eq 1 ] ; then
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

    $(_separator_exists $sep)

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
_spack_env_remove() {
    varname="$1"
    value="$2"
    sep="$3"

    $(_separator_exists $sep)

    eval "varname_value=\"\${${varname}}\""

    if [ "$varname_value" == "$value" ]; then
        export $varname=""
    elif [ "${varname_value##$value$sep}" != "${varname_value}" ]; then
        export $varname=${varname_value##$value$sep}
    elif [ "${varname_value%%$sep$value}" != "${varname_value}" ]; then
        export $varname=${varname_value%%$sep$value}
    else
        eval "export $varname=\"${varname_value[@]/$value$sep/}\""
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
