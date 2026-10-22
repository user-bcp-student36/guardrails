"""Arquitecto: diagnóstico y plan del repositorio, en una sola llamada."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block


INSTRUCTIONS = (
    "Role: Arquitecto de software del equipo.\n"
    "Goal: Analiza el Issue del bloque ALCANCE, sus criterios de aceptación y las interfaces del producto. "
    "Define componentes, responsabilidades y límites del cambio, sin proponer trabajo fuera del Issue. "
    "Especifica entradas, respuestas y errores de la API con ejemplos de petición y respuesta. "
    "Relaciona cada criterio de aceptación con el componente que lo resuelve, y declara supuestos y preguntas pendientes. "
    "Devuelve ## Analysis y ## Plan en líneas independientes, con diagnóstico, archivos afectados y orden de los cambios.\n"
    "Backstory: Conoces el producto de login: POST /auth/login, token firmado con claims y expiración. "
    "Diseñas con cautela y usas marcadores como <TOKEN> en lugar de secretos o credenciales reales.\n"
)


def architect_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta el alcance del issue y la constitución.") + "\nRepositorio: " + state['repo_name']
            + "\nTipo: " + state.get('project_type','ambos')
            + "\nCódigo original:\n" + _ctx(state['snapshot'],10000)
            + "\nDevuelve las secciones ## Analysis y ## Plan, cada una en su propia línea.")
    report = invoke(prompt)
    analysis, separator, plan = report.partition("\n## Plan\n")
    if not analysis.startswith("## Analysis\n") or not separator or not plan.strip():
        raise ValueError(
            "El arquitecto debe devolver las secciones ## Analysis y ## Plan."
        )
    return {
        "out_architect": report,
        "out_analysis": analysis.removeprefix("## Analysis\n").strip(),
        "out_plan": plan.strip(),
    }
