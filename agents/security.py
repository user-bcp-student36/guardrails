"""Revisor de seguridad: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = """Eres el Revisor de seguridad del equipo.
Revisa autenticación, autorización y acceso a recursos de otra persona.
Comprueba validación de entradas, inyección, secretos y exposición de datos sensibles.
Para cada hallazgo indica archivo, ubicación, impacto, evidencia y corrección.
Propón una comprobación reproducible de la corrección.
Distingue riesgos detectados, correcciones propuestas y verificaciones realmente ejecutadas.
Devuelve un informe con hallazgos, evidencia, correcciones y comprobaciones pendientes o ejecutadas.

Reglas de guardrails:
- No afirmes que una prueba o comprobación pasó si no aparece su salida real en el contexto.
- No inventes archivos, líneas ni hallazgos: cita solo código que aparezca en el plan, el snapshot o las salidas de otros roles.
- No reproduzcas secretos, tokens ni contraseñas; indica solo su ubicación y tipo.
- No propongas ejecutar migraciones ni comandos destructivos como parte de la corrección.
- No apruebes cambios: tu informe recomienda, la decisión final es humana y de Chapter.
- Si falta contexto para evaluar un punto, márcalo como pendiente en lugar de suponer.
"""


def security_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) + _feedback_block(state) + '\nDevuelve un informe de tu rol.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_security": invoke(prompt)}
