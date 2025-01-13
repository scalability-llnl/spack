from spack.package import *

class {{ cls_name }}(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/root-1.0.tar.gz"

    version("3.0", sha256='abcde')
    version("2.0", sha256='abcde')
    version("1.0", sha256='abcde')

{% for dep_spec, dep_type, condition in dependencies %}
{% if dep_type and condition %}
    depends_on("{{ dep_spec }}", type="{{ dep_type }}", when="{{ condition }}")
{% elif dep_type %}
    depends_on("{{ dep_spec }}", type="{{ dep_type }}")
{% elif condition %}
    depends_on("{{ dep_spec }}", when="{{ condition }}")
{% else %}
    depends_on("{{ dep_spec }}")
{% endif %}
{% endfor %}