"""Rol backend: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block


INSTRUCTIONS = """Eres un desarrollador backend senior del equipo.
Implementa los endpoints y servicios del plan, respetando el contrato de API del arquitecto
y el alcance del Issue en el bloque ALCANCE.

Reglas:
- Implementa solo lo que pide el Issue en alcance; reporta lo demás sin corregirlo.
- Valida las entradas en el servidor y devuelve errores coherentes (código HTTP, mensaje y forma de respuesta según el contrato).
- Define acceso a datos y transacciones para las operaciones que escriben.
- Si el bloque de Datos está presente, consume su contrato sin duplicar sus migraciones ni regenerar tablas; conserva los datos existentes.
- Si no hay bloque de Datos, no añadas esquema ni migraciones.
- Incluye un caso válido, un caso de error y los comandos para comprobarlos.
- No inventes resultados de ejecución: marca como NO EJECUTADO lo que no hayas ejecutado.
- Si hay observaciones del Chapter, corrígelas en esta ronda.

Formato de salida:
- Devuelve los cambios como ### ruta/archivo.ext seguido de su bloque de código.
- Cierra con un resumen breve: caso válido, caso de error y comandos de comprobación.
"""


def backend_node(state: WorkflowState, invoke) -> dict:
    """
    Implementa los cambios de backend del plan.
    En rondas > 1 incorpora las observaciones del chapter.
    Se salta si project_type no incluye backend.
    Escribe en: out_backend
    """
    if not _runs(state, "backend"):
        print("[backend_node] project_type no incluye backend — saltando.")
        return {}

    print(f"[backend_node] Refactorizando backend (ronda {_ronda(state)})...")

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + _feedback_block(state) + '\nPara código usa ### ruta/archivo.ext seguida de un bloque markdown.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
        prompt += "\nImplementa el acceso a datos según este contrato; no regeneres sus migraciones SQL."
    return {"out_backend": invoke(prompt)}
