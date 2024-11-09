SPACK ?= {{ spack_script }} -c config:install_status:false
SPACK_INSTALL_FLAGS ?=

# This variable can be used to add post install hooks
{{ pkg_ids_variable }} := {{ pkg_ids }}

.PHONY: {{ all_target }} {{ clean_target }}

{{ all_target }}: {{ env_target }}

{{ env_target }}: {{ root_install_targets }} | {{ dirs_target }}
	@touch $@

{{ dirs_target }}:
	@mkdir -p {{ install_target }} {{ install_deps_target }}

{% if phony_convenience_targets %}
.PHONY: {{ phony_convenience_targets }}
{% endif %}

# The spack install commands are of the form:
# spack -e my_env --only=package --only=concrete /hash
# This is an involved way of expressing that Spack should only install
# an individual concrete spec from the environment without deps.
{{ install_target }}/%: | {{ dirs_target }}
	{{ jobserver_support }}$(SPACK) -e '{{ environment }}' install $(SPACK_BUILDCACHE_FLAG) $(SPACK_INSTALL_FLAGS) --only-concrete --only=package /$(HASH) # $(SPEC)
	@touch $@

{{ install_deps_target }}/%: | {{ dirs_target }}
	@touch $@

# Set a human-readable SPEC variable for each target that has a hash
{% for (parent, _, hash, name, build_cache) in adjacency_list -%}
{{ any_hash_target }}/{{ parent }}: HASH = {{ hash }}
{{ any_hash_target }}/{{ parent }}: SPEC = {{ name }}
{{ any_hash_target }}/{{ parent }}: SPACK_BUILDCACHE_FLAG = {{ build_cache }}
{% endfor %}

# The Spack DAG expressed in targets:
{% for (parent, prereqs, _, _, _) in adjacency_list -%}
{{ install_target }}/{{ parent }}: {{ install_deps_target }}/{{ parent }}
{{ install_deps_target }}/{{ parent }}: {{ prereqs }}
{% if phony_convenience_targets %}
install/{{ parent }}: {{ install_target }}/{{ parent }}
install-deps/{{ parent }}: {{ install_deps_target }}/{{ parent }}
{% endif %}
{% endfor %}

{{ clean_target }}:
	rm -rf {{ env_target }} {{ all_install_related_targets }}
