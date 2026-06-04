import pytest
import main

@pytest.fixture(autouse=True)
def reset_todo_list():
    main.todo_list.clear()
    main.id_counter = 1
    yield