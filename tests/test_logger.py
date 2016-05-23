import pytest

from jam.base import Operation
from jam.models import Log


class TestReadOnlyLogger:

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_cant_create(self):
        pass


class TestLogger:

    def test_create(self, logger, freezetime):
        log = logger.create('test', Operation.CREATE, 'data_ref', 'user')
        assert isinstance(log, Log)
        assert log == logger.get(log.ref)
        assert log is not logger.get(log.ref)

        assert log.record_id == 'test'
        assert log.created_by == 'user'
        assert log.modified_by == 'user'
        assert log.data_ref == 'data_ref'
        assert log.operation == Operation.CREATE
        assert log.created_on == log.modified_on
        assert log.created_on == freezetime.time_to_freeze.timestamp()
        assert log.modified_on == freezetime.time_to_freeze.timestamp()

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_create_with_previous(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_create_operation_params(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_get(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_latest_snapshot(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_latest_snapshot_no_snapshot(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_history(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_history_no_existant(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_after(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_after_empty(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_bulk_read(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_at_time(self, logger):
        pass

    @pytest.mark.skip(reason='Unimplemented Test')
    def test_create_snapshot(self, logger):
        pass
