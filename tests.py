import unittest
import os
import json
import random

from tasks import TASKS
from storage import load_history, save_history

_HISTORY_FILE = "history.json"


class TestTasks(unittest.TestCase):
    """Тесты базы задач и генерации."""

    def test_tasks_not_empty(self):
        """База задач не пуста (позитивный)."""
        self.assertGreater(len(TASKS), 0)

    def test_tasks_have_required_keys(self):
        """Каждая задача содержит поля task и type (позитивный)."""
        for t in TASKS:
            self.assertIn("task", t)
            self.assertIn("type", t)

    def test_tasks_no_empty_fields(self):
        """Поля task и type не пусты (позитивный)."""
        for t in TASKS:
            self.assertTrue(t["task"].strip())
            self.assertTrue(t["type"].strip())

    def test_filter_by_type_sport(self):
        """Фильтр по типу 'спорт' работает (позитивный)."""
        pool = [t for t in TASKS if t["type"] == "спорт"]
        self.assertTrue(all(t["type"] == "спорт" for t in pool))
        self.assertGreater(len(pool), 0)

    def test_filter_by_type_study(self):
        """Фильтр по типу 'учёба' работает (позитивный)."""
        pool = [t for t in TASKS if t["type"] == "учёба"]
        self.assertGreater(len(pool), 0)

    def test_filter_no_match(self):
        """Несуществующий тип возвращает пустой пул (негативный)."""
        pool = [t for t in TASKS if t["type"] == "несуществующий"]
        self.assertEqual(pool, [])

    def test_custom_task_empty_text_invalid(self):
        """Пустой текст задачи не допустим (негативный)."""
        text = "  "
        self.assertFalse(bool(text.strip()))

    def test_random_choice(self):
        """random.choice возвращает элемент из пула (позитивный)."""
        result = random.choice(TASKS)
        self.assertIn(result, TASKS)


class TestStorage(unittest.TestCase):
    """Тесты JSON-хранилища."""

    def tearDown(self):
        if os.path.exists(_HISTORY_FILE):
            os.remove(_HISTORY_FILE)

    def test_save_and_load(self):
        """Сохранение и загрузка корректны (позитивный)."""
        data = [{"task": "Test", "type": "работа", "date": "2025-01-01 00:00:00"}]
        save_history(data)
        self.assertEqual(load_history(), data)

    def test_load_no_file(self):
        """Загрузка без файла — пустой список (позитивный)."""
        if os.path.exists(_HISTORY_FILE):
            os.remove(_HISTORY_FILE)
        self.assertEqual(load_history(), [])

    def test_load_corrupt(self):
        """Повреждённый JSON — пустой список (негативный)."""
        with open(_HISTORY_FILE, "w") as f:
            f.write("{{bad")
        self.assertEqual(load_history(), [])

    def test_load_wrong_type(self):
        """JSON-объект вместо массива — пустой список (граничный)."""
        with open(_HISTORY_FILE, "w") as f:
            json.dump({"key": "val"}, f)
        self.assertEqual(load_history(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
