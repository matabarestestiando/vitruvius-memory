import os
from langsmith import tracing_context, traceable
from langsmith.run_helpers import get_current_run_tree


@traceable(
    name="vitruvius-operation",
    process_inputs=lambda _: {},
    process_outputs=lambda _: {},
)
def _event(operation, metadata):
    run = get_current_run_tree()
    if run:
        run.add_metadata({"operation": operation, **metadata})


def event(operation, **metadata):
    # Callers pass identifiers/counts only, never query text, arguments, credentials or file contents.
    if not os.getenv("LANGSMITH_API_KEY"):
        return
    with tracing_context(
        enabled=True, project_name=os.getenv("LANGSMITH_PROJECT", "vitruvius-memory")
    ):
        _event(operation, metadata)
