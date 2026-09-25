import pytest
import pandas as pd
import json
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any

from src.transform.schema_evolution import (
    SchemaVersion,
    SchemaField,
    SchemaEvolutionManager,
    detect_schema_changes,
    apply_schema_migration,
    validate_schema_compatibility,
    SchemaChangeType
)


class TestSchemaField:
    def test_field_creation(self):
        field = SchemaField(
            name='customer_id',
            data_type='string',
            nullable=False,
            description='Unique customer identifier'
        )
        assert field.name == 'customer_id'
        assert field.data_type == 'string'
        assert field.nullable is False

    def test_field_to_dict(self):
        field = SchemaField(
            name='amount',
            data_type='decimal',
            nullable=True,
            description='Transaction amount'
        )
        field_dict = field.to_dict()
        assert isinstance(field_dict, dict)
        assert field_dict['name'] == 'amount'
        assert field_dict['data_type'] == 'decimal'

    def test_field_from_dict(self):
        field_dict = {
            'name': 'status',
            'data_type': 'string',
            'nullable': False,
            'description': 'Record status'
        }
        field = SchemaField.from_dict(field_dict)
        assert field.name == 'status'
        assert field.data_type == 'string'


class TestSchemaVersion:
    def test_version_creation(self):
        version = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True)
            ],
            created_at=datetime(2024, 1, 1),
            description='Initial schema'
        )
        assert version.version_number == '1.0.0'
        assert len(version.fields) == 2

    def test_version_comparison(self):
        v1 = SchemaVersion(version_number='1.0.0', fields=[])
        v2 = SchemaVersion(version_number='2.0.0', fields=[])
        assert v1 < v2

    def test_version_serialization(self):
        version = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False)
            ],
            created_at=datetime(2024, 1, 15),
            description='Test schema'
        )
        serialized = version.to_dict()
        assert 'version_number' in serialized
        assert 'fields' in serialized
        restored = SchemaVersion.from_dict(serialized)
        assert restored.version_number == version.version_number


class TestDetectSchemaChanges:
    def test_detect_added_field(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True),
                SchemaField(name='email', data_type='string', nullable=True)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.ADDED
        assert changes[0].field_name == 'email'

    def test_detect_removed_field(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='deprecated_field', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.REMOVED

    def test_detect_type_change(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='amount', data_type='int', nullable=False)
            ]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[
                SchemaField(name='amount', data_type='decimal', nullable=False)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.TYPE_CHANGED

    def test_detect_nullable_change(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='phone', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[
                SchemaField(name='phone', data_type='string', nullable=False)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.NULLABLE_CHANGED

    def test_no_changes_for_identical_schemas(self):
        fields = [SchemaField(name='id', data_type='int', nullable=False)]
        old_schema = SchemaVersion(version_number='1.0.0', fields=fields)
        new_schema = SchemaVersion(version_number='1.0.1', fields=fields)
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 0


class TestValidateSchemaCompatibility:
    def test_backward_compatible_addition(self):
        old_schema = SchemaVersion(version_number='1.0.0', fields=[])
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[SchemaField(name='new_field', data_type='string', nullable=True)]
        )
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is True
        assert len(issues) == 0

    def test_not_backward_compatible_removal(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='required_field', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(version_number='2.0.0', fields=[])
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is False
        assert len(issues) > 0

    def test_not_backward_compatible_type_change(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='field', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='field', data_type='string', nullable=False)]
        )
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is False

    def test_nullable_to_not_nullable_breaking(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='field', data_type='string', nullable=True)]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='field', data_type='string', nullable=False)]
        )
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is False


class TestApplySchemaMigration:
    def test_migration_adds_default_values(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='status', data_type='string', nullable=True)
            ]
        )
        old_data = pd.DataFrame({'id': [1, 2, 3]})
        migrated_data = apply_schema_migration(old_data, old_schema, new_schema)
        assert 'status' in migrated_data.columns
        assert migrated_data['status'].isna().all()

    def test_migration_drops_removed_columns(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='old_field', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)]
        )
        old_data = pd.DataFrame({'id': [1, 2], 'old_field': ['a', 'b']})
        migrated_data = apply_schema_migration(old_data, old_schema, new_schema)
        assert 'old_field' not in migrated_data.columns
        assert list(migrated_data.columns) == ['id']

    def test_migration_handles_type_conversion(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='value', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='value', data_type='float', nullable=False)]
        )
        old_data = pd.DataFrame({'value': [10, 20, 30]})
        migrated_data = apply_schema_migration(old_data, old_schema, new_schema)
        assert migrated_data['value'].dtype in [float, 'float64', 'float32']


class TestSchemaEvolutionManager:
    def test_manager_creation(self):
        manager = SchemaEvolutionManager()
        assert manager.get_current_version() is None
        assert len(manager.get_all_versions()) == 0

    def test_register_and_get_version(self):
        manager = SchemaEvolutionManager()
        schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)],
            created_at=datetime.now()
        )
        manager.register_version(schema)
        retrieved = manager.get_version('1.0.0')
        assert retrieved is not None
        assert retrieved.version_number == '1.0.0'

    def test_get_latest_version(self):
        manager = SchemaEvolutionManager()
        v1 = SchemaVersion(version_number='1.0.0', fields=[SchemaField(name='id', data_type='int', nullable=False)])
        v2 = SchemaVersion(version_number='2.0.0', fields=[SchemaField(name='id', data_type='int', nullable=False)])
        v3 = SchemaVersion(version_number='1.5.0', fields=[SchemaField(name='id', data_type='int', nullable=False)])
        manager.register_version(v1)
        manager.register_version(v2)
        manager.register_version(v3)
        latest = manager.get_latest_version()
        assert latest.version_number == '2.0.0'

    def test_migrate_between_versions(self):
        manager = SchemaEvolutionManager()
        v1 = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)]
        )
        v2 = SchemaVersion(
            version_number='2.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True)
            ]
        )
        manager.register_version(v1)
        manager.register_version(v2)
        data = pd.DataFrame({'id': [1, 2, 3]})
        migrated = manager.migrate(data, '1.0.0', '2.0.0')
        assert 'name' in migrated.columns


class TestSchemaChangeType:
    def test_change_type_enum_values(self):
        assert SchemaChangeType.ADDED.value == 'added'
        assert SchemaChangeType.REMOVED.value == 'removed'
        assert SchemaChangeType.TYPE_CHANGED.value == 'type_changed'
        assert SchemaChangeType.NULLABLE_CHANGED.value == 'nullable_changed'
        assert SchemaChangeType.DESCRIPTION_CHANGED.value == 'description_changed'