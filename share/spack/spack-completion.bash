# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# NOTE: spack-completion.bash is auto-generated by:
#
#   $ spack commands --aliases --format=bash
#       --header=bash/spack-completion.in --update=spack-completion.bash
#
# Please do not manually modify this file.


# The following global variables are set by Bash programmable completion:
#
#     COMP_CWORD:      An index into ${COMP_WORDS} of the word containing the
#                      current cursor position
#     COMP_KEY:        The key (or final key of a key sequence) used to invoke
#                      the current completion function
#     COMP_LINE:       The current command line
#     COMP_POINT:      The index of the current cursor position relative to the
#                      beginning of the current command
#     COMP_TYPE:       Set to an integer value corresponding to the type of
#                      completion attempted that caused a completion function
#                      to be called
#     COMP_WORDBREAKS: The set of characters that the readline library treats
#                      as word separators when performing word completion
#     COMP_WORDS:      An array variable consisting of the individual words in
#                      the current command line
#
# The following global variable is used by Bash programmable completion:
#
#     COMPREPLY:       An array variable from which bash reads the possible
#                      completions generated by a shell function invoked by the
#                      programmable completion facility
#
# See `man bash` for more details.

# Bash programmable completion for Spack
_bash_completion_spack() {
    # In all following examples, let the cursor be denoted by brackets, i.e. []

    # For our purposes, flags should not affect tab completion. For instance,
    # `spack install []` and `spack -d install --jobs 8 []` should both give the same
    # possible completions. Therefore, we need to ignore any flags in COMP_WORDS.
    local COMP_WORDS_NO_FLAGS=()
    local index=0
    while [[ "$index" -lt "$COMP_CWORD" ]]
    do
        if [[ "${COMP_WORDS[$index]}" == [a-z]* ]]
        then
            COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$index]}")
        fi
        let index++
    done

    # Options will be listed by a subfunction named after non-flag arguments.
    # For example, `spack -d install []` will call _spack_install
    # and `spack compiler add []` will call _spack_compiler_add
    local subfunction=$(IFS='_'; echo "_${COMP_WORDS_NO_FLAGS[*]}")

    # Translate dashes to underscores, as dashes are not permitted in
    # compatibility mode. See https://github.com/spack/spack/pull/4079
    subfunction=${subfunction//-/_}

    # However, the word containing the current cursor position needs to be
    # added regardless of whether or not it is a flag. This allows us to
    # complete something like `spack install --keep-st[]`
    COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$COMP_CWORD]}")

    # Since we have removed all words after COMP_CWORD, we can safely assume
    # that COMP_CWORD_NO_FLAGS is simply the index of the last element
    local COMP_CWORD_NO_FLAGS=$((${#COMP_WORDS_NO_FLAGS[@]} - 1))

    # There is no guarantee that the cursor is at the end of the command line
    # when tab completion is envoked. For example, in the following situation:
    #     `spack -d [] install`
    # if the user presses the TAB key, a list of valid flags should be listed.
    # Note that we cannot simply ignore everything after the cursor. In the
    # previous scenario, the user should expect to see a list of flags, but
    # not of other subcommands. Obviously, `spack -d list install` would be
    # invalid syntax. To accomplish this, we use the variable list_options
    # which is true if the current word starts with '-' or if the cursor is
    # not at the end of the line.
    local list_options=false
    if [[ "${COMP_WORDS[$COMP_CWORD]}" == -* || "$COMP_POINT" -ne "${#COMP_LINE}" ]]
    then
        list_options=true
    fi

    # In general, when envoking tab completion, the user is not expecting to
    # see optional flags mixed in with subcommands or package names. Tab
    # completion is used by those who are either lazy or just bad at spelling.
    # If someone doesn't remember what flag to use, seeing single letter flags
    # in their results won't help them, and they should instead consult the
    # documentation. However, if the user explicitly declares that they are
    # looking for a flag, we can certainly help them out.
    #     `spack install -[]`
    # and
    #     `spack install --[]`
    # should list all flags and long flags, respectively. Furthermore, if a
    # subcommand has no non-flag completions, such as `spack arch []`, it
    # should list flag completions.

    local cur=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS]}

    # If the cursor is in the middle of the line, like:
    #     `spack -d [] install`
    # COMP_WORDS will not contain the empty character, so we have to add it.
    if [[ "${COMP_LINE:$COMP_POINT:1}" == " " ]]
    then
        cur=""
    fi

    # Uncomment this line to enable logging
    #_test_vars >> temp

    # Make sure function exists before calling it
    if [[ "$(type -t $subfunction)" == "function" ]]
    then
        $subfunction
        COMPREPLY=($(compgen -W "$SPACK_COMPREPLY" -- "$cur"))
    fi
}

# Helper functions for subcommands
# Results of each query are cached via environment variables

_subcommands() {
    if [[ -z "${SPACK_SUBCOMMANDS:-}" ]]
    then
        SPACK_SUBCOMMANDS="$(spack commands)"
    fi
    SPACK_COMPREPLY="$SPACK_SUBCOMMANDS"
}

_all_packages() {
    if [[ -z "${SPACK_ALL_PACKAGES:-}" ]]
    then
        SPACK_ALL_PACKAGES="$(spack list)"
    fi
    SPACK_COMPREPLY="$SPACK_ALL_PACKAGES"
}

_all_resource_hashes() {
    if [[ -z "${SPACK_ALL_RESOURCES_HASHES:-}" ]]
    then
        SPACK_ALL_RESOURCE_HASHES="$(spack resource list --only-hashes)"
    fi
    SPACK_COMPREPLY="$SPACK_ALL_RESOURCE_HASHES"
}

_installed_packages() {
    if [[ -z "${SPACK_INSTALLED_PACKAGES:-}" ]]
    then
        SPACK_INSTALLED_PACKAGES="$(spack --color=never find --no-groups)"
    fi
    SPACK_COMPREPLY="$SPACK_INSTALLED_PACKAGES"
}

_installed_compilers() {
    if [[ -z "${SPACK_INSTALLED_COMPILERS:-}" ]]
    then
        SPACK_INSTALLED_COMPILERS="$(spack compilers | egrep -v "^(-|=)")"
    fi
    SPACK_COMPREPLY="$SPACK_INSTALLED_COMPILERS"
}

_providers() {
    if [[ -z "${SPACK_PROVIDERS:-}" ]]
    then
        SPACK_PROVIDERS="$(spack providers)"
    fi
    SPACK_COMPREPLY="$SPACK_PROVIDERS"
}

_mirrors() {
    if [[ -z "${SPACK_MIRRORS:-}" ]]
    then
        SPACK_MIRRORS="$(spack mirror list | awk '{print $1}')"
    fi
    SPACK_COMPREPLY="$SPACK_MIRRORS"
}

_repos() {
    if [[ -z "${SPACK_REPOS:-}" ]]
    then
        SPACK_REPOS="$(spack repo list | awk '{print $1}')"
    fi
    SPACK_COMPREPLY="$SPACK_REPOS"
}

_tests() {
    if [[ -z "${SPACK_TESTS:-}" ]]
    then
        SPACK_TESTS="$(spack test -l)"
    fi
    SPACK_COMPREPLY="$SPACK_TESTS"
}

_environments() {
    if [[ -z "${SPACK_ENVIRONMENTS:-}" ]]
    then
        SPACK_ENVIRONMENTS="$(spack env list)"
    fi
    SPACK_COMPREPLY="$SPACK_ENVIRONMENTS"
}

_keys() {
    if [[ -z "${SPACK_KEYS:-}" ]]
    then
        SPACK_KEYS="$(spack gpg list)"
    fi
    SPACK_COMPREPLY="$SPACK_KEYS"
}

_config_sections() {
    if [[ -z "${SPACK_CONFIG_SECTIONS:-}" ]]
    then
        SPACK_CONFIG_SECTIONS="$(spack config list)"
    fi
    SPACK_COMPREPLY="$SPACK_CONFIG_SECTIONS"
}

_extensions() {
    if [[ -z "${SPACK_EXTENSIONS:-}" ]]
    then
        SPACK_EXTENSIONS="$(spack extensions)"
    fi
    SPACK_COMPREPLY="$SPACK_EXTENSIONS"
}

# Testing functions

# Function for unit testing tab completion
# Syntax: _spack_completions spack install py-
_spack_completions() {
    local COMP_CWORD COMP_KEY COMP_LINE COMP_POINT COMP_TYPE COMP_WORDS COMPREPLY

    # Set each variable the way bash would
    COMP_LINE="$*"
    COMP_POINT=${#COMP_LINE}
    COMP_WORDS=("$@")
    if [[ ${COMP_LINE: -1} == ' ' ]]
    then
        COMP_WORDS+=('')
    fi
    COMP_CWORD=$((${#COMP_WORDS[@]} - 1))
    COMP_KEY=9    # ASCII 09: Horizontal Tab
    COMP_TYPE=64  # ASCII 64: '@', to list completions if the word is not unmodified

    # Run Spack's tab completion function
    _bash_completion_spack

    # Return the result
    echo "${COMPREPLY[@]:-}"
}

# Log the environment variables used
# Syntax: _test_vars >> temp
_test_vars() {
    echo "-----------------------------------------------------"
    echo "Variables set by bash:"
    echo
    echo "COMP_LINE:                '$COMP_LINE'"
    echo "# COMP_LINE:              '${#COMP_LINE}'"
    echo "COMP_WORDS:               $(_pretty_print COMP_WORDS[@])"
    echo "# COMP_WORDS:             '${#COMP_WORDS[@]}'"
    echo "COMP_CWORD:               '$COMP_CWORD'"
    echo "COMP_KEY:                 '$COMP_KEY'"
    echo "COMP_POINT:               '$COMP_POINT'"
    echo "COMP_TYPE:                '$COMP_TYPE'"
    echo "COMP_WORDBREAKS:          '$COMP_WORDBREAKS'"
    echo
    echo "Intermediate variables:"
    echo
    echo "COMP_WORDS_NO_FLAGS:      $(_pretty_print COMP_WORDS_NO_FLAGS[@])"
    echo "# COMP_WORDS_NO_FLAGS:    '${#COMP_WORDS_NO_FLAGS[@]}'"
    echo "COMP_CWORD_NO_FLAGS:      '$COMP_CWORD_NO_FLAGS'"
    echo
    echo "Subfunction:              '$subfunction'"
    if $list_options
    then
        echo "List options:             'True'"
    else
        echo "List options:             'False'"
    fi
    echo "Current word:             '$cur'"
}

# Pretty-prints one or more arrays
# Syntax: _pretty_print array1[@] ...
_pretty_print() {
    for arg in $@
    do
        local array=("${!arg}")
        printf "$arg: ["
        printf   "'%s'" "${array[0]}"
        printf ", '%s'" "${array[@]:1}"
        echo "]"
    done
}

complete -o bashdefault -o default -F _bash_completion_spack spack

# Spack commands
#
# Everything below here is auto-generated.

_spack() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -H --all-help --color -C --config-scope -d --debug --timestamp --pdb -e --env -D --env-dir -E --no-env --use-env-repo -k --insecure -l --enable-locks -L --disable-locks -m --mock -p --profile --sorted-profile --lines -v --verbose --stacktrace -V --version --print-shell-vars"
    else
        SPACK_COMPREPLY="activate add arch blame bootstrap build build-env buildcache cd checksum ci clean clone commands compiler compilers concretize config configure containerize create deactivate debug dependencies dependents deprecate dev-build diy docs edit env extensions fetch find flake8 gc gpg graph help info install license list load location log-parse maintainers mirror module patch pkg providers pydoc python reindex remove rm repo resource restage setup spec stage test uninstall unload upload-s3 url verify versions view"
    fi
}

_spack_activate() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -f --force -v --view"
    else
        _installed_packages
    fi
}

_spack_add() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -l --list-name"
    else
        _all_packages
    fi
}

_spack_arch() {
    SPACK_COMPREPLY="-h --help --known-targets -p --platform -o --operating-system -t --target -f --frontend -b --backend"
}

_spack_blame() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -t --time -p --percent -g --git"
    else
        _all_packages
    fi
}

_spack_bootstrap() {
    SPACK_COMPREPLY="-h --help -j --jobs --keep-prefix --keep-stage -n --no-checksum -v --verbose --use-cache --no-cache --cache-only --clean --dirty"
}

_spack_build() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -v --verbose"
    else
        _all_packages
    fi
}

_spack_build_env() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --clean --dirty --dump --pickle"
    else
        _all_packages
    fi
}

_spack_buildcache() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="create install list keys preview check download get-buildcache-name save-yaml copy update-index"
    fi
}

_spack_buildcache_create() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -r --rel -f --force -u --unsigned -a --allow-root -k --key -d --directory -m --mirror-name --mirror-url --no-rebuild-index -y --spec-yaml --only"
    else
        _all_packages
    fi
}

_spack_buildcache_install() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -f --force -m --multiple -a --allow-root -u --unsigned -o --otherarch"
    else
        _all_packages
    fi
}

_spack_buildcache_list() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -l --long -L --very-long -v --variants -f --force -a --allarch"
    else
        _all_packages
    fi
}

_spack_buildcache_keys() {
    SPACK_COMPREPLY="-h --help -i --install -t --trust -f --force"
}

_spack_buildcache_preview() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _installed_packages
    fi
}

_spack_buildcache_check() {
    SPACK_COMPREPLY="-h --help -m --mirror-url -o --output-file --scope -s --spec -y --spec-yaml --rebuild-on-error"
}

_spack_buildcache_download() {
    SPACK_COMPREPLY="-h --help -s --spec -y --spec-yaml -p --path -c --require-cdashid"
}

_spack_buildcache_get_buildcache_name() {
    SPACK_COMPREPLY="-h --help -s --spec -y --spec-yaml"
}

_spack_buildcache_save_yaml() {
    SPACK_COMPREPLY="-h --help --root-spec --root-spec-yaml -s --specs -y --yaml-dir"
}

_spack_buildcache_copy() {
    SPACK_COMPREPLY="-h --help --base-dir --spec-yaml --destination-url"
}

_spack_buildcache_update_index() {
    SPACK_COMPREPLY="-h --help -d --mirror-url"
}

_spack_cd() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -m --module-dir -r --spack-root -i --install-dir -p --package-dir -P --packages -s --stage-dir -S --stages -b --build-dir -e --env"
    else
        _all_packages
    fi
}

_spack_checksum() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --keep-stage"
    else
        _all_packages
    fi
}

_spack_ci() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="start generate pushyaml rebuild"
    fi
}

_spack_ci_start() {
    SPACK_COMPREPLY="-h --help --output-file --copy-to --spack-repo --spack-ref --downstream-repo --branch-name --commit-sha"
}

_spack_ci_generate() {
    SPACK_COMPREPLY="-h --help --output-file --copy-to --spack-repo --spack-ref"
}

_spack_ci_pushyaml() {
    SPACK_COMPREPLY="-h --help --downstream-repo --branch-name --commit-sha"
}

_spack_ci_rebuild() {
    SPACK_COMPREPLY="-h --help"
}

_spack_clean() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -s --stage -d --downloads -m --misc-cache -p --python-cache -a --all"
    else
        _all_packages
    fi
}

_spack_clone() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -r --remote"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_commands() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --update-completion -a --aliases --format --header --update"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_compiler() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="find add remove rm list info"
    fi
}

_spack_compiler_find() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_compiler_add() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_compiler_remove() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -a --all --scope"
    else
        _installed_compilers
    fi
}

_spack_compiler_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -a --all --scope"
    else
        _installed_compilers
    fi
}

_spack_compiler_list() {
    SPACK_COMPREPLY="-h --help --scope"
}

_spack_compiler_info() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        _installed_compilers
    fi
}

_spack_compilers() {
    SPACK_COMPREPLY="-h --help --scope"
}

_spack_concretize() {
    SPACK_COMPREPLY="-h --help -f --force"
}

_spack_config() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        SPACK_COMPREPLY="get blame edit list"
    fi
}

_spack_config_get() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _config_sections
    fi
}

_spack_config_blame() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _config_sections
    fi
}

_spack_config_edit() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --print-file"
    else
        _config_sections
    fi
}

_spack_config_list() {
    SPACK_COMPREPLY="-h --help"
}

_spack_configure() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -v --verbose"
    else
        _all_packages
    fi
}

_spack_containerize() {
    SPACK_COMPREPLY="-h --help"
}

_spack_create() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --keep-stage -n --name -t --template -r --repo -N --namespace -f --force --skip-editor"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_deactivate() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -f --force -v --view -a --all"
    else
        _installed_packages
    fi
}

_spack_debug() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="create-db-tarball"
    fi
}

_spack_debug_create_db_tarball() {
    SPACK_COMPREPLY="-h --help"
}

_spack_dependencies() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -i --installed -t --transitive --deptype -V --no-expand-virtuals"
    else
        _all_packages
    fi
}

_spack_dependents() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -i --installed -t --transitive"
    else
        _all_packages
    fi
}

_spack_deprecate() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -y --yes-to-all -d --dependencies -D --no-dependencies -i --install-deprecator -I --no-install-deprecator -l --link-type"
    else
        _all_packages
    fi
}

_spack_dev_build() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -j --jobs -d --source-path -i --ignore-dependencies -n --no-checksum --keep-prefix --skip-patch -q --quiet -u --until --clean --dirty"
    else
        _all_packages
    fi
}

_spack_diy() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -j --jobs -d --source-path -i --ignore-dependencies -n --no-checksum --keep-prefix --skip-patch -q --quiet -u --until --clean --dirty"
    else
        _all_packages
    fi
}

_spack_docs() {
    SPACK_COMPREPLY="-h --help"
}

_spack_edit() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -b --build-system -c --command -d --docs -t --test -m --module -r --repo -N --namespace"
    else
        _all_packages
    fi
}

_spack_env() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="activate deactivate create remove rm list ls status st loads view"
    fi
}

_spack_env_activate() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --sh --csh -v --with-view -V --without-view -d --dir -p --prompt"
    else
        _environments
    fi
}

_spack_env_deactivate() {
    SPACK_COMPREPLY="-h --help --sh --csh"
}

_spack_env_create() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -d --dir --without-view --with-view"
    else
        _environments
    fi
}

_spack_env_remove() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -y --yes-to-all"
    else
        _environments
    fi
}

_spack_env_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -y --yes-to-all"
    else
        _environments
    fi
}

_spack_env_list() {
    SPACK_COMPREPLY="-h --help"
}

_spack_env_ls() {
    SPACK_COMPREPLY="-h --help"
}

_spack_env_status() {
    SPACK_COMPREPLY="-h --help"
}

_spack_env_st() {
    SPACK_COMPREPLY="-h --help"
}

_spack_env_loads() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -m --module-type --input-only -p --prefix -x --exclude -r --dependencies"
    else
        _environments
    fi
}

_spack_env_view() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_extensions() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -l --long -L --very-long -d --deps -p --paths -s --show -v --view"
    else
        _extensions
    fi
}

_spack_fetch() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -n --no-checksum -m --missing -D --dependencies"
    else
        _all_packages
    fi
}

_spack_find() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --format --json -d --deps -p --paths --groups --no-groups -l --long -L --very-long -t --tags -c --show-concretized -f --show-flags --show-full-compiler -x --explicit -X --implicit -u --unknown -m --missing -v --variants --loaded -M --only-missing --deprecated --only-deprecated -N --namespace --start-date --end-date"
    else
        _installed_packages
    fi
}

_spack_flake8() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -b --base -k --keep-temp -a --all -o --output -r --root-relative -U --no-untracked"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_gc() {
    SPACK_COMPREPLY="-h --help -y --yes-to-all"
}

_spack_gpg() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="verify trust untrust sign create list init export"
    fi
}

_spack_gpg_verify() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _installed_packages
    fi
}

_spack_gpg_trust() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_gpg_untrust() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --signing"
    else
        _keys
    fi
}

_spack_gpg_sign() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --output --key --clearsign"
    else
        _installed_packages
    fi
}

_spack_gpg_create() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --comment --expires --export"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_gpg_list() {
    SPACK_COMPREPLY="-h --help --trusted --signing"
}

_spack_gpg_init() {
    SPACK_COMPREPLY="-h --help --from"
}

_spack_gpg_export() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _keys
    fi
}

_spack_graph() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -a --ascii -d --dot -s --static -i --installed --deptype"
    else
        _all_packages
    fi
}

_spack_help() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -a --all --spec"
    else
        _subcommands
    fi
}

_spack_info() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_packages
    fi
}

_spack_install() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --only -u --until -j --jobs --overwrite --keep-prefix --keep-stage --dont-restage --use-cache --no-cache --cache-only --no-check-signature --show-log-on-error --source -n --no-checksum -v --verbose --fake --only-concrete -f --file --clean --dirty --test --run-tests --log-format --log-file --help-cdash --cdash-upload-url --cdash-build --cdash-site --cdash-track --cdash-buildstamp -y --yes-to-all"
    else
        _all_packages
    fi
}

_spack_license() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="list-files verify"
    fi
}

_spack_license_list_files() {
    SPACK_COMPREPLY="-h --help"
}

_spack_license_verify() {
    SPACK_COMPREPLY="-h --help --root"
}

_spack_list() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -d --search-description --format --update -t --tags"
    else
        _all_packages
    fi
}

_spack_load() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -r --dependencies --sh --csh --only"
    else
        _installed_packages
    fi
}

_spack_location() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -m --module-dir -r --spack-root -i --install-dir -p --package-dir -P --packages -s --stage-dir -S --stages -b --build-dir -e --env"
    else
        _all_packages
    fi
}

_spack_log_parse() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --show -c --context -p --profile -w --width -j --jobs"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_maintainers() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --maintained --unmaintained -a --all --by-user"
    else
        _all_packages
    fi
}

_spack_mirror() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -n --no-checksum"
    else
        SPACK_COMPREPLY="create add remove rm set-url list"
    fi
}

_spack_mirror_create() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -d --directory -a --all -f --file --skip-unstable-versions -D --dependencies -n --versions-per-spec"
    else
        _all_packages
    fi
}

_spack_mirror_add() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        _mirrors
    fi
}

_spack_mirror_remove() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        _mirrors
    fi
}

_spack_mirror_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        _mirrors
    fi
}

_spack_mirror_set_url() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --push --scope"
    else
        _mirrors
    fi
}

_spack_mirror_list() {
    SPACK_COMPREPLY="-h --help --scope"
}

_spack_module() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="lmod tcl"
    fi
}

_spack_module_lmod() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="refresh find rm loads setdefault"
    fi
}

_spack_module_lmod_refresh() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --delete-tree --upstream-modules -y --yes-to-all"
    else
        _installed_packages
    fi
}

_spack_module_lmod_find() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --full-path -r --dependencies"
    else
        _installed_packages
    fi
}

_spack_module_lmod_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -y --yes-to-all"
    else
        _installed_packages
    fi
}

_spack_module_lmod_loads() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --input-only -p --prefix -x --exclude -r --dependencies"
    else
        _installed_packages
    fi
}

_spack_module_lmod_setdefault() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _installed_packages
    fi
}

_spack_module_tcl() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="refresh find rm loads"
    fi
}

_spack_module_tcl_refresh() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --delete-tree --upstream-modules -y --yes-to-all"
    else
        _installed_packages
    fi
}

_spack_module_tcl_find() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --full-path -r --dependencies"
    else
        _installed_packages
    fi
}

_spack_module_tcl_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -y --yes-to-all"
    else
        _installed_packages
    fi
}

_spack_module_tcl_loads() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --input-only -p --prefix -x --exclude -r --dependencies"
    else
        _installed_packages
    fi
}

_spack_patch() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -n --no-checksum"
    else
        _all_packages
    fi
}

_spack_pkg() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="add list diff added changed removed"
    fi
}

_spack_pkg_add() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_packages
    fi
}

_spack_pkg_list() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_pkg_diff() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_pkg_added() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_pkg_changed() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -t --type"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_pkg_removed() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_providers() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _providers
    fi
}

_spack_pydoc() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_python() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -V --version -c -m"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_reindex() {
    SPACK_COMPREPLY="-h --help"
}

_spack_remove() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -a --all -l --list-name -f --force"
    else
        _all_packages
    fi
}

_spack_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -a --all -l --list-name -f --force"
    else
        _all_packages
    fi
}

_spack_repo() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="create list add remove rm"
    fi
}

_spack_repo_create() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _repos
    fi
}

_spack_repo_list() {
    SPACK_COMPREPLY="-h --help --scope"
}

_spack_repo_add() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_repo_remove() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        _repos
    fi
}

_spack_repo_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --scope"
    else
        _repos
    fi
}

_spack_resource() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="list show"
    fi
}

_spack_resource_list() {
    SPACK_COMPREPLY="-h --help --only-hashes"
}

_spack_resource_show() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_resource_hashes
    fi
}

_spack_restage() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_packages
    fi
}

_spack_setup() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -i --ignore-dependencies -n --no-checksum -v --verbose --clean --dirty"
    else
        _all_packages
    fi
}

_spack_spec() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -l --long -L --very-long -I --install-status -y --yaml -j --json -c --cover -N --namespaces -t --types"
    else
        _all_packages
    fi
}

_spack_stage() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -n --no-checksum -p --path"
    else
        _all_packages
    fi
}

_spack_test() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -H --pytest-help -l --list -L --list-long -N --list-names --extension -s -k --showlocals"
    else
        _tests
    fi
}

_spack_uninstall() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -f --force -R --dependents -y --yes-to-all -a --all"
    else
        _installed_packages
    fi
}

_spack_unload() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --sh --csh -a --all"
    else
        _installed_packages
    fi
}

_spack_upload_s3() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="spec index"
    fi
}

_spack_upload_s3_spec() {
    SPACK_COMPREPLY="-h --help -s --spec -y --spec-yaml -b --base-dir -e --endpoint-url"
}

_spack_upload_s3_index() {
    SPACK_COMPREPLY="-h --help -e --endpoint-url"
}

_spack_url() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        SPACK_COMPREPLY="parse list summary stats"
    fi
}

_spack_url_parse() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -s --spider"
    else
        SPACK_COMPREPLY=""
    fi
}

_spack_url_list() {
    SPACK_COMPREPLY="-h --help -c --color -e --extrapolation -n --incorrect-name -N --correct-name -v --incorrect-version -V --correct-version"
}

_spack_url_summary() {
    SPACK_COMPREPLY="-h --help"
}

_spack_url_stats() {
    SPACK_COMPREPLY="-h --help"
}

_spack_verify() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -l --local -j --json -a --all -s --specs -f --files"
    else
        _all_packages
    fi
}

_spack_versions() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -s --safe-only"
    else
        _all_packages
    fi
}

_spack_view() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help -v --verbose -e --exclude -d --dependencies"
    else
        SPACK_COMPREPLY="symlink add soft hardlink hard remove rm statlink status check"
    fi
}

_spack_view_symlink() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --projection-file -i --ignore-conflicts"
    else
        _all_packages
    fi
}

_spack_view_add() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --projection-file -i --ignore-conflicts"
    else
        _all_packages
    fi
}

_spack_view_soft() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --projection-file -i --ignore-conflicts"
    else
        _all_packages
    fi
}

_spack_view_hardlink() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --projection-file -i --ignore-conflicts"
    else
        _all_packages
    fi
}

_spack_view_hard() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --projection-file -i --ignore-conflicts"
    else
        _all_packages
    fi
}

_spack_view_remove() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --no-remove-dependents -a --all"
    else
        _all_packages
    fi
}

_spack_view_rm() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help --no-remove-dependents -a --all"
    else
        _all_packages
    fi
}

_spack_view_statlink() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_packages
    fi
}

_spack_view_status() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_packages
    fi
}

_spack_view_check() {
    if $list_options
    then
        SPACK_COMPREPLY="-h --help"
    else
        _all_packages
    fi
}
