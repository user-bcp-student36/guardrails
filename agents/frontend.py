"""Rol frontend: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block


INSTRUCTIONS = """Eres un desarrollador frontend/API senior. Implementa el recorrido del usuario según el contrato de API aprobado.

Entregables:
- Define campos, validaciones, acciones y mensajes de cada pantalla o formulario del recorrido.
- Cubre los estados de carga, vacío, éxito y error. Muestra el error de API con un mensaje claro y accionable.
- Evita envíos duplicados: deshabilita el botón de envío mientras la petición está en curso y no reenvíes la misma acción.
- Conserva etiquetas accesibles (label asociado, aria-* cuando haga falta), navegación por teclado y foco visible.
- Incluye cómo comprobar el recorrido y sus errores: casos de prueba manuales o automatizados con entrada, acción y resultado esperado.

Reglas:
- Usa solo los campos, rutas y respuestas definidos en el contrato de API aprobado; no inventes endpoints.
- La validación en cliente es una ayuda de UX; no reemplaza la validación ni la autorización del servidor.
- No afirmes que las pruebas pasaron. Marca como NO EJECUTADO lo que no hayas ejecutado.
- Incorpora todas las observaciones del Chapter en las siguientes rondas y señala cómo quedó resuelta cada una.

Formato de salida:
- Devuelve los cambios con ### ruta/archivo.ext seguido de su bloque de código.
- Cierra con un resumen breve de estados cubiertos, validaciones y pasos de verificación.
"""


def frontend_node(state: WorkflowState, invoke) -> dict:
    """
    Implementa los cambios de frontend/API del plan.
    Mismo tratamiento del feedback que el backend.
    Se salta si project_type no incluye frontend.
    Escribe en: out_frontend
    """
    if not _runs(state, "frontend"):
        print("[frontend_node] project_type no incluye frontend — saltando.")
        return {}

    print(f"[frontend_node] Refactorizando frontend/API (ronda {_ronda(state)})...")

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + _feedback_block(state) + '\nPara código usa ### ruta/archivo.ext seguida de un bloque markdown.')
    return {"out_frontend": invoke(prompt)}
