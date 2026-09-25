from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict


class TransformationType(str, Enum):
    EXTRACT = "extract"
    TRANSFORM = "transform"
    LOAD = "load"
    FILTER = "filter"
    AGGREGATE = "aggregate"
    JOIN = "join"
    VALIDATE = "validate"
    ENRICH = "enrich"
    CLEAN = "clean"
    MASK = "mask"


class DataAssetType(str, Enum):
    TABLE = "table"
    FILE = "file"
    STREAM = "stream"
    VIEW = "view"
    DATASET = "dataset"


class DataNode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    asset_type: DataAssetType
    source_system: Optional[str] = None
    schema_definition: Optional[dict[str, Any]] = None
    partition_columns: Optional[list[str]] = None
    storage_location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DataTransformation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    transformation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transformation_type: TransformationType
    source_nodes: list[str] = Field(default_factory=list)
    target_node: str
    transformation_logic: str
    transformation_params: dict[str, Any] = Field(default_factory=dict)
    executed_by: Optional[str] = None
    execution_id: Optional[str] = None
    execution_timestamp: Optional[datetime] = None
    checksum: Optional[str] = None
    status: str = "pending"
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None


class DataLineageEdge(BaseModel):
    edge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_node_id: str
    target_node_id: str
    transformation_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class LineageGraph(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    graph_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nodes: dict[str, DataNode] = Field(default_factory=dict)
    transformations: dict[str, DataTransformation] = Field(default_factory=dict)
    edges: dict[str, DataLineageEdge] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DataLineageTracker:
    def __init__(self):
        self.graphs: dict[str, LineageGraph] = {}
        self._active_graph: Optional[LineageGraph] = None

    def create_graph(self, graph_name: str) -> LineageGraph:
        graph = LineageGraph()
        self.graphs[graph.graph_id] = graph
        self._active_graph = graph
        return graph

    def get_or_create_graph(self, graph_id: Optional[str] = None) -> LineageGraph:
        if graph_id and graph_id in self.graphs:
            self._active_graph = self.graphs[graph_id]
            return self._active_graph
        return self.create_graph(f"graph_{graph_id or len(self.graphs)}")

    def register_node(
        self,
        name: str,
        asset_type: DataAssetType,
        source_system: Optional[str] = None,
        schema_definition: Optional[dict[str, Any]] = None,
        partition_columns: Optional[list[str]] = None,
        storage_location: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> DataNode:
        if self._active_graph is None:
            self.get_or_create_graph()

        node = DataNode(
            name=name,
            asset_type=asset_type,
            source_system=source_system,
            schema_definition=schema_definition,
            partition_columns=partition_columns,
            storage_location=storage_location,
            metadata=metadata or {},
        )
        self._active_graph.nodes[node.node_id] = node
        return node

    def register_transformation(
        self,
        transformation_type: TransformationType,
        source_node_ids: list[str],
        target_node_id: str,
        transformation_logic: str,
        transformation_params: Optional[dict[str, Any]] = None,
        executed_by: Optional[str] = None,
        execution_id: Optional[str] = None,
    ) -> DataTransformation:
        if self._active_graph is None:
            raise ValueError("No active lineage graph. Create one first.")

        transformation = DataTransformation(
            transformation_type=transformation_type,
            source_nodes=source_node_ids,
            target_node=target_node_id,
            transformation_logic=transformation_logic,
            transformation_params=transformation_params or {},
            executed_by=executed_by,
            execution_id=execution_id,
        )
        self._active_graph.transformations[transformation.transformation_id] = transformation

        for source_id in source_node_ids:
            edge = DataLineageEdge(
                source_node_id=source_id,
                target_node_id=target_node_id,
                transformation_id=transformation.transformation_id,
            )
            self._active_graph.edges[edge.edge_id] = edge

        return transformation

    def mark_transformation_complete(
        self,
        transformation_id: str,
        status: str,
        checksum: Optional[str] = None,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ) -> None:
        if self._active_graph is None:
            raise ValueError("No active lineage graph.")

        if transformation_id not in self._active_graph.transformations:
            raise KeyError(f"Transformation {transformation_id} not found.")

        transformation = self._active_graph.transformations[transformation_id]
        transformation.status = status
        transformation.execution_timestamp = datetime.utcnow()
        transformation.checksum = checksum
        transformation.error_message = error_message
        transformation.duration_ms = duration_ms

    def get_upstream_dependencies(self, node_id: str) -> list[DataNode]:
        if self._active_graph is None:
            return []

        visited = set()
        result = []
        stack = [node_id]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            for edge in self._active_graph.edges.values():
                if edge.target_node_id == current and edge.is_active:
                    source_node = self._active_graph.nodes.get(edge.source_node_id)
                    if source_node and source_node.node_id not in visited:
                        result.append(source_node)
                        stack.append(source_node.node_id)

        return result

    def get_downstream_dependencies(self, node_id: str) -> list[DataNode]:
        if self._active_graph is None:
            return []

        visited = set()
        result = []
        stack = [node_id]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            for edge in self._active_graph.edges.values():
                if edge.source_node_id == current and edge.is_active:
                    target_node = self._active_graph.nodes.get(edge.target_node_id)
                    if target_node and target_node.node_id not in visited:
                        result.append(target_node)
                        stack.append(target_node.node_id)

        return result

    def get_full_lineage_path(self, start_node_id: str, end_node_id: str) -> list[DataLineageEdge]:
        if self._active_graph is None:
            return []

        graph = self._active_graph.graph
        try:
            from collections import deque

            queue = deque([(start_node_id, [start_node_id])])
            visited = {start_node_id}

            while queue:
                current, path = queue.popleft()

                if current == end_node_id:
                    edges_path = []
                    for i in range(len(path) - 1):
                        for edge in self._active_graph.edges.values():
                            if edge.source_node_id == path[i] and edge.target_node_id == path[i + 1]:
                                edges_path.append(edge)
                                break
                    return edges_path

                for edge in self._active_graph.edges.values():
                    if edge.source_node_id == current and edge.is_active:
                        next_node = edge.target_node_id
                        if next_node not in visited:
                            visited.add(next_node)
                            queue.append((next_node, path + [next_node]))

            return []
        except ImportError:
            return []

    def export_lineage_metadata(self) -> dict[str, Any]:
        if self._active_graph is None:
            return {"graphs": []}

        return {
            "graph_id": self._active_graph.graph_id,
            "nodes": [
                {
                    "node_id": n.node_id,
                    "name": n.name,
                    "asset_type": n.asset_type.value,
                    "source_system": n.source_system,
                    "schema_definition": n.schema_definition,
                    "partition_columns": n.partition_columns,
                    "storage_location": n.storage_location,
                }
                for n in self._active_graph.nodes.values()
            ],
            "transformations": [
                {
                    "transformation_id": t.transformation_id,
                    "transformation_type": t.transformation_type.value,
                    "source_nodes": t.source_nodes,
                    "target_node": t.target_node,
                    "transformation_logic": t.transformation_logic,
                    "status": t.status,
                    "checksum": t.checksum,
                    "duration_ms": t.duration_ms,
                }
                for t in self._active_graph.transformations.values()
            ],
            "edge_count": len(self._active_graph.edges),
        }

    def get_active_graph(self) -> Optional[LineageGraph]:
        return self._active_graph

    def set_active_graph(self, graph_id: str) -> None:
        if graph_id in self.graphs:
            self._active_graph = self.graphs[graph_id]
        else:
            raise KeyError(f"Graph {graph_id} not found.")

    def calculate_data_quality_impact(self, transformation_id: str) -> dict[str, Any]:
        if self._active_graph is None:
            return {"error": "No active graph"}

        transformation = self._active_graph.transformations.get(transformation_id)
        if not transformation:
            return {"error": "Transformation not found"}

        source_nodes = [
            self._active_graph.nodes.get(sid)
            for sid in transformation.source_nodes
            if sid in self._active_graph.nodes
        ]
        target_node = self._active_graph.nodes.get(transformation.target_node)

        quality_score = 100.0
        if transformation.status == "failed":
            quality_score = 0.0
        elif transformation.error_message:
            quality_score = 50.0

        return {
            "transformation_id": transformation_id,
            "source_nodes_count": len(source_nodes),
            "target_node": target_node.name if target_node else None,
            "quality_score": quality_score,
            "has_errors": transformation.status == "failed",
            "duration_ms": transformation.duration_ms,
        }

    def get_data_flow_summary(self) -> dict[str, Any]:
        if self._active_graph is None:
            return {"error": "No active graph"}

        node_count = len(self._active_graph.nodes)
        transformation_count = len(self._active_graph.transformations)
        edge_count = len(self._active_graph.edges)

        by_type: dict[str, int] = {}
        for node in self._active_graph.nodes.values():
            at = node.asset_type.value
            by_type[at] = by_type.get(at, 0) + 1

        successful = sum(
            1 for t in self._active_graph.transformations.values() if t.status == "completed"
        )
        failed = sum(
            1 for t in self._active_graph.transformations.values() if t.status == "failed"
        )

        return {
            "total_nodes": node_count,
            "total_transformations": transformation_count,
            "total_edges": edge_count,
            "nodes_by_type": by_type,
            "transformations_successful": successful,
            "transformations_failed": failed,
            "success_rate": (successful / transformation_count * 100) if transformation_count > 0 else 0,
        }