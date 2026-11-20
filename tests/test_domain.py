from decimal import Decimal
import pytest
from app.errors import DataError
from app.modules.domain.rule import evaluate


def test_refund_after_cutoff(cases):
    actual, evidence = evaluate(cases['refund_after_cutoff'])
    assert actual == Decimal('700')
    assert evidence and all(len(row)==3 for row in evidence)


def test_next_business_day(cases):
    # TRAP-23
    actual, evidence = evaluate(cases['next_business_day'])
    assert actual == Decimal('-100')


def test_same_time(cases):
    actual, evidence = evaluate(cases['same_time'])
    assert actual == Decimal('600')


def test_no_cash(cases):
    actual, evidence = evaluate(cases['no_cash'])
    assert actual == Decimal('0')


def test_over_cash(cases):
    with pytest.raises(DataError) as error:
        evaluate(cases['over_cash'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}


def test_over_refund(cases):
    with pytest.raises(DataError) as error:
        evaluate(cases['over_refund'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}


def test_duplicate(cases):
    with pytest.raises(DataError) as error:
        evaluate(cases['duplicate'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}

