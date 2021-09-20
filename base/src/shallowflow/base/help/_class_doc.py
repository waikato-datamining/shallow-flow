import json
import os
from shallowflow.api.class_utils import get_class_name, class_name_to_type
from shallowflow.api.help import class_hierarchy_help
from . import Markdown


def markdown_class_doc(conf, output_dir):
    """
    Generates class documentation using the specified configuration file.

    :param conf: the JSON file with the configuration
    :type conf: str
    :param output_dir: the top-level directory for the generated documentation
    :type output_dir: str
    """
    with open(conf, "r") as f:
        c = json.load(f)
        generator = Markdown()
        readme_modules = "# Class documentation\n\n"
        for module in c["modules"]:
            print("Processing module: %s" % module)
            readme_modules += "* [%s](%s)\n" % (module, module)
            m = c["modules"][module]
            dir = os.path.join(output_dir, module)
            if not os.path.exists(dir):
                os.mkdir(dir)
            regexp = m["module_regexp"]
            readme_module = "# %s\n" % module
            for superclass in m["superclasses"]:
                classes, files = class_hierarchy_help(class_name_to_type(superclass), generator, dir, module_regexp=regexp)
                first = True
                for cls, f in zip(classes, files):
                    if f is None:
                        continue
                    if first:
                        readme_module += "\n## %s\n\n" % superclass
                        first = False
                    readme_module += "* [%s](%s)\n" % (get_class_name(cls), f)
            # write README for classes
            with open(os.path.join(dir, "README.md"), "w") as f:
                f.write(readme_module)
        # write README for modules
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_modules)

