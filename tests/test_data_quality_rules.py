import pytest
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime, date

from src.transform.data_quality_rules import (
    DataQualityRule,
    QualityThreshold,
    QualityResult,
    validate_completeness,
    validate_uniqueness,
    validate_consistency,
    validate_timeliness,
    run_quality_checks
)


class TestCompletenessRule:
    def test_completeness_passes_when_no_nulls(self):
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'email': ['a@test.com', 'b@test.com', 'c@test.com'],
            'phone': ['123', '456', '789']
        })
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_completeness(df, 'email', threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_completeness_fails_when_below_threshold(self):
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'email': ['a@test.com', None, 'c@test.com', None, 'e@test.com']
        })
        threshold = QualityThreshold(min_percentage=90.0)
        result = validate_completeness(df, 'email', threshold)
        assert result.passed is False
        assert result.score == 60.0

    def test_completeness_handles_empty_column(self):
        df = pd.DataFrame({'col': pd.Series(dtype='str')})
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_completeness(df, 'col', threshold)
        assert result.passed is False
        assert result.score == 0.0


class TestUniquenessRule:
    def test_uniqueness_passes_with_unique_values(self):
        df = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'code': ['A', 'B', 'C', 'D']
        })
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_uniqueness(df, 'id', threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_uniqueness_fails_with_duplicates(self):
        df = pd.DataFrame({
            'id': [1, 2, 1, 3, 2],
            'code': ['A', 'B', 'A', 'C', 'B']
        })
        threshold = QualityThreshold(min_percentage=90.0)
        result = validate_uniqueness(df, 'id', threshold)
        assert result.passed is False
        assert result.score == 60.0

    def test_uniqueness_with_nulls_ignores_null_count(self):
        df = pd.DataFrame({
            'id': [1, 2, None, 3, None]
        })
        threshold = QualityThreshold(min_percentage=80.0)
        result = validate_uniqueness(df, 'id', threshold)
        assert result.passed is True


class TestConsistencyRule:
    def test_consistency_passes_for_valid_range(self):
        df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_consistency(df, 'age', min_value=18, max_value=65, threshold=threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_consistency_fails_for_invalid_values(self):n        df = pd.DataFrame({
            'age': [25, 150, 35, -5, 45]
        })
        threshold = QualityThreshold(min_percentage=90.0)
        result = validate_consistency(df, 'age', min_value=18, max_value=65, threshold=threshold)
        assert result.passed is False
        assert result.score == 60.0

    def test_consistency_with_regex_pattern(self):
        df = pd.DataFrame({
            'email': ['user@test.com', 'invalid', 'other@test.com', 'bad_format']
        })
        threshold = QualityThreshold(min_percentage=80.0)
        result = validate_consistency(
            df, 'email', 
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            threshold=threshold
        )
        assert result.passed is False
        assert result.score == 50.0


class TestTimelinessRule:
    def test_timeliness_passes_with_recent_data(self):
        df = pd.DataFrame({
            'record_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])
        })
        threshold = QualityThreshold(min_percentage=95.0)
        reference_date = date(2024, 1, 5)
        result = validate_timeliness(df, 'record_date', max_days_old=7, reference_date=reference_date, threshold=threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_timeliness_fails_with_stale_data(self):
        df = pd.DataFrame({
            'record_date': pd.to_datetime(['2023-12-01', '2023-12-15', '2024-01-01'])
        })
        threshold = QualityThreshold(min_percentage=90.0)
        reference_date = date(2024, 1, 10)
        result = validate_timeliness(df, 'record_date', max_days_old=7, reference_date=reference_date, threshold=threshold)
        assert result.passed is False


class TestQualityResult:
    def test_quality_result_calculation(self):
        result = QualityResult(
            rule_name='test_rule',
            column_name='test_col',
            passed=True,
            score=95.5,
            total_records=100,
            valid_records=95,
            invalid_records=5,
            details={'threshold': 90.0}
        )
        assert result.passed is True
        assert result.score == 95.5
        assert result.total_records == 100

    def test_quality_result_to_dict(self):
        result = QualityResult(
            rule_name='test',
            column_name='col',
            passed=True,
            score=100.0,
            total_records=50,
            valid_records=50,
            invalid_records=0
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['rule_name'] == 'test'
        assert result_dict['score'] == 100.0


class TestRunQualityChecks:
    def test_run_multiple_rules(self):
        df = pd.DataFrame({
            'id': [1, 2, 3, 2],
            'email': ['a@test.com', None, 'c@test.com', 'd@test.com'],
            'age': [25, 35, 150, 45]
        })
        rules = [
            DataQualityRule(
                name='unique_ids',
                column='id',
                rule_type='uniqueness',
                threshold=QualityThreshold(min_percentage=90.0)
            ),
            DataQualityRule(
                name='complete_emails',
                column='email',
                rule_type='completeness',
                threshold=QualityThreshold(min_percentage=80.0)
            ),
            DataQualityRule(
                name='valid_ages',
                column='age',
                rule_type='consistency',
                threshold=QualityThreshold(min_percentage=90.0),
                params={'min_value': 0, 'max_value': 120}
            )
        ]
        results = run_quality_checks(df, rules)
        assert len(results) == 3
        assert any(r.passed for r in results)
        assert any(not r.passed for r in results)

    def test_run_quality_checks_returns_empty_for_empty_rules(self):
        df = pd.DataFrame({'col': [1, 2, 3]})
        results = run_quality_checks(df, [])
        assert results == []


class TestDataQualityRuleModel:
    def test_rule_creation_with_defaults(self):
        rule = DataQualityRule(
            name='test_rule',
            column='test_col',
            rule_type='completeness',
            threshold=QualityThreshold(min_percentage=95.0)
        )
        assert rule.name == 'test_rule'
        assert rule.column == 'test_col'
        assert rule.rule_type == 'completeness'
        assert rule.enabled is True

    def test_rule_with_custom_params(self):
        rule = DataQualityRule(
            name='age_check',
            column='age',
            rule_type='consistency',
            threshold=QualityThreshold(min_percentage=90.0),
            params={'min_value': 18, 'max_value': 65}
        )
        assert rule.params['min_value'] == 18
        assert rule.params['max_value'] == 65