import os
import pytest
from tests.mocks.mock_driver import MockDriver
from griptape.drivers import DiskMemoryDriver
from griptape.memory import Memory
from griptape.tasks import PromptTask
from griptape.structures import Pipeline


class TestPromptDriver:
    MEMORY_FILE_PATH = "test_memory.json"

    @pytest.fixture(autouse=True)
    def run_before_and_after_tests(self):
        self.__delete_file(self.MEMORY_FILE_PATH)

        yield

        self.__delete_file(self.MEMORY_FILE_PATH)

    def test_store(self):
        prompt_driver = MockDriver()
        memory_driver = DiskMemoryDriver(file_path=self.MEMORY_FILE_PATH)
        memory = Memory(driver=memory_driver)
        pipeline = Pipeline(prompt_driver=prompt_driver, memory=memory)

        pipeline.add_task(
            PromptTask("test")
        )

        try:
            with open(self.MEMORY_FILE_PATH, "r"):
                assert False
        except FileNotFoundError:
            assert True

        pipeline.run()

        with open(self.MEMORY_FILE_PATH, "r"):
            assert True

    def test_load(self):
        prompt_driver = MockDriver()
        memory_driver = DiskMemoryDriver(file_path=self.MEMORY_FILE_PATH)
        memory = Memory(driver=memory_driver)
        pipeline = Pipeline(prompt_driver=prompt_driver, memory=memory)

        pipeline.add_task(
            PromptTask("test")
        )

        pipeline.run()
        pipeline.run()

        new_memory = memory_driver.load()

        assert new_memory.type == "Memory"
        assert len(new_memory.runs) == 2
        assert new_memory.runs[0].input == "test"
        assert new_memory.runs[0].output == "mock output"

    def __delete_file(self, file_path):
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass