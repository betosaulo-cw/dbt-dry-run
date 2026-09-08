from dbt_dry_run.exception import UpstreamFailedException
from dbt_dry_run.models.dry_run_result import DryRunResult
from dbt_dry_run.models.manifest import Node
from dbt_dry_run.models.report import DryRunStatus
from dbt_dry_run.node_runner import NodeRunner
from dbt_dry_run.sql.statements import (
    SQLPreprocessor,
    add_dbt_max_partition_declaration,
    add_sql_header,
    insert_dependant_sql_literals,
)


class PlainRunner(NodeRunner):
    """Runs the compiled SQL as-is, without any DDL wrappers (no CREATE VIEW, no MERGE).
    Useful for CI environments where the service account has only read permissions."""

    preprocessor = SQLPreprocessor(
        [
            insert_dependant_sql_literals,
            add_sql_header,
            add_dbt_max_partition_declaration,
        ]
    )

    def run(self, node: Node) -> DryRunResult:
        try:
            run_sql = self.preprocessor(node, self._results)
        except UpstreamFailedException as e:
            return DryRunResult(node, None, DryRunStatus.FAILURE, e)

        status, model_schema, exception = self._sql_runner.query(run_sql)
        return DryRunResult(node, model_schema, status, exception)
