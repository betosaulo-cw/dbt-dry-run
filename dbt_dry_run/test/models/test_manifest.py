import pytest

from dbt_dry_run.models.manifest import NodeConfig, NodeMeta, PartitionBy
from dbt_dry_run.test.utils import SimpleNode


def test_partition_by_config_case_insensitive() -> None:
    partition_by = PartitionBy(field="a_field", data_type="TIMESTAMP")
    assert partition_by.field == "a_field"
    assert partition_by.data_type == "timestamp"


@pytest.mark.parametrize("config_meta", [False, True])
def test_node_get_meta_key_return_config_meta(
    config_meta: bool,
) -> None:
    config = NodeConfig(
        materialized="table",
        meta=NodeMeta.model_validate({NodeMeta.DEFAULT_CHECK_COLUMNS_KEY: config_meta}),
    )
    node = SimpleNode(
        unique_id="a",
        depends_on=[],
        table_config=config,
    ).to_node()

    assert node.get_meta_key(NodeMeta.DEFAULT_CHECK_COLUMNS_KEY) is config_meta


def test_node_get_meta_key_none_if_meta_is_none() -> None:
    config = NodeConfig(
        materialized="table",
        meta=None,
    )
    node = SimpleNode(
        unique_id="a",
        depends_on=[],
        table_config=config,
    ).to_node()

    assert node.get_meta_key("ANY_KEY") is None


def test_metadata_parses_check_columns() -> None:
    metadata = NodeMeta.model_validate({NodeMeta.DEFAULT_CHECK_COLUMNS_KEY: False})
    assert metadata[NodeMeta.DEFAULT_CHECK_COLUMNS_KEY] is False


def test_metadata_contains_key() -> None:
    metadata = NodeMeta.model_validate({"my_key": False})
    assert ("my_key" in metadata) is True
