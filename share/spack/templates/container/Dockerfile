{% if bootstrap.image %}
{{ bootstrap.recipe }}
{% endif %}
# Build stage with Spack pre-installed and ready to be used
FROM {{ build.image }} as builder

{% if os_packages_build %}
# Install OS packages needed to build the software
RUN {% if os_package_update %}{{ os_packages_build.update }} \
 && {% endif %}{{ os_packages_build.install }} {{ os_packages_build.list | join | replace('\n', ' ') }} \
 && {{ os_packages_build.clean }}
{% endif %}

# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir {{ paths.environment }} \
{{ manifest }} > {{ paths.environment }}/spack.yaml

# Install the software, remove unnecessary deps
RUN cd {{ paths.environment }} && spack env activate . && spack install --fail-fast && spack gc -y
{% if strip %}

# Strip all the binaries
RUN find -L {{ paths.view }}/* -type f -exec readlink -f '{}' \; | \
    xargs file -i | \
    grep 'charset=binary' | \
    grep 'x-executable\|x-archive\|x-sharedlib' | \
    awk -F: '{print $1}' | xargs strip -s
{% endif %}

# Modifications to the environment that are necessary to run
RUN cd {{ paths.environment }} && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

{% if extra_instructions.build %}
{{ extra_instructions.build }}
{% endif %}

# Bare OS image to run the installed executables
FROM {{ run.image }}

COPY --from=builder {{ paths.environment }} {{ paths.environment }}
COPY --from=builder {{ paths.store }} {{ paths.store }}
COPY --from=builder {{ paths.view }} {{ paths.view }}
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

{% if os_packages_final %}
RUN {% if os_package_update %}{{ os_packages_final.update }} \
 && {% endif %}{{ os_packages_final.install }} {{ os_packages_final.list | join | replace('\n', ' ') }} \
 && {{ os_packages_final.clean }}
{% endif %}
{% if extra_instructions.final %}

{{ extra_instructions.final }}
{% endif %}
{% for label, value in labels.items() %}
LABEL "{{ label }}"="{{ value }}"
{% endfor %}
ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
