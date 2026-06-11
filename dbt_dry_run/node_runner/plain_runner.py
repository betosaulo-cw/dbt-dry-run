from dbt_dry_run.exception import UpstreamFailedException
from dbt_dry_run.literals import insert_dependant_sql_literals
from dbt_dry_run.models.manifest import Node
from dbt_dry_run.node_runner import NodeRunner
from dbt_dry_run.results import DryRunResult, DryRunStatus


class PlainRunner(NodeRunner):
    """Runs the compiled SQL as-is, without any DDL wrappers (no CREATE VIEW, no MERGE).
    Useful for CI environments where the service account has only read permissions."""

    def run(self, node: Node) -> DryRunResult:
        try:
            run_sql = insert_dependant_sql_literals(node, self._results)
        except UpstreamFailedException as e:
            return DryRunResult(node, None, DryRunStatus.FAILURE, 0, e)

        status, model_schema, total_bytes_processed, exception = self._sql_runner.query(
            run_sql
        )
        return DryRunResult(node, model_schema, status, total_bytes_processed, exception)
