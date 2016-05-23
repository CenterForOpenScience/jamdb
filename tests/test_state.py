import pytest


@pytest.mark.skip(reason='Unimplemented Test')
class TestState:

    @pytest.mark.foo
    def test_clear(self):
        pass

    def test_get(self):
        pass

    def test_list(self):
        pass

    def test_get_doesnt_exist(self):
        pass

    def test_keys(self):
        pass

    def test_keys_empty(self):
        pass

    def test_apply(self):
        pass

    def test_apply_unsafe(self):
        pass

    def test_apply_safe(self):
        pass

    def test_create(self):
        pass

    def test_rename(self):
        pass

    def test_delete(self):
        pass

    def test_replace(self):
        pass

    def test_update(self):
        pass
