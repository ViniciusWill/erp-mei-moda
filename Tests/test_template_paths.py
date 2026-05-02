import ast
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
ROUTES_DIR = ROOT_DIR / "app" / "routes"
TEMPLATES_DIR = ROOT_DIR / "app" / "templates"


def iter_render_template_names():
    for route_file in ROUTES_DIR.glob("*.py"):
        tree = ast.parse(route_file.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            function_name = getattr(node.func, "id", "")
            if function_name != "render_template" or not node.args:
                continue

            template_arg = node.args[0]
            if isinstance(template_arg, ast.Constant) and isinstance(template_arg.value, str):
                yield route_file, template_arg.value


def test_render_template_paths_exist_with_exact_case():
    erros = []

    for route_file, template_name in iter_render_template_names():
        template_path = TEMPLATES_DIR / template_name
        if not template_path.is_file():
            erros.append(f"{route_file.relative_to(ROOT_DIR)} -> {template_name}")

    assert not erros, "Templates nao encontrados com o mesmo uso de maiusculas/minusculas:\n" + "\n".join(erros)
