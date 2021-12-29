from pprint import pprint
import traceback
import jinja2


def jinja_getattr(self, s_name):
    try:
        return self._TemplateReference__context[s_name]
    except:
        print()
        pprint(self._TemplateReference__context["tree"])
        raise Exception("Undefined macro : %s" % s_name)


def c_ast_to_c(o_tree, s_template_name, s_template_folder="templates"):
    o_env = jinja2.Environment(
        loader=jinja2.PackageLoader("cnorm_to_c", s_template_folder)
    )
    o_template = o_env.get_template(
        s_template_name, globals={"getattr": jinja_getattr, "tree": o_tree}
    )
    try:
        s_generated_code = o_template.render(o_tree)
    except jinja2.exceptions.UndefinedError as exception:
        raise Exception(
            "Something was possibly wrong with the tree. Check it and the traceback : %s."
            % exception
        )
        print()
        pprint(o_tree)
        print((traceback.format_exc()))
        exit(1)
    return s_generated_code
