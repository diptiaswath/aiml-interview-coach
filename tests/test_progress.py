"""Tests for GET /progress. Every test runs against a temporary data folder."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from app import data
from app.main import app

client = TestClient(app)


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the app at an empty temp folder so tests never touch data/results.json."""
    monkeypatch.setattr(data, "DATA_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def write_results(data_dir: Path) -> Callable[[list[dict]], Path]:
    """Return a helper that writes a list of results to the temp results.json."""

    def _write(results: list[dict]) -> Path:
        path = data_dir / "results.json"
        path.write_text(json.dumps(results), encoding="utf-8")
        return path

    return _write


def test_fixture_isolates_results(write_results: Callable[[list[dict]], Path]) -> None:
    write_results([{"total": 12}])
    assert data.load_results() == [{"total": 12}]


def test_progress_averages_totals(write_results: Callable[[list[dict]], Path]) -> None:
    write_results([{"total": 3}, {"total": 9}])
    response = client.get("/progress")
    assert response.status_code == 200
    assert response.json() == {"rounds_practised": 2, "average_total": 6.0}


def test_progress_rounds_to_one_decimal(write_results: Callable[[list[dict]], Path]) -> None:
    write_results([{"total": 3}, {"total": 4}, {"total": 4}])  # 11 / 3 = 3.666...
    assert client.get("/progress").json()["average_total"] == 3.7


def test_progress_does_not_modify_results(write_results: Callable[[list[dict]], Path]) -> None:
    path = write_results([{"total": 3}, {"total": 9}])
    before = path.read_bytes()
    client.get("/progress")
    assert path.read_bytes() == before


def test_progress_empty_when_file_missing(data_dir: Path) -> None:
    response = client.get("/progress")
    assert response.status_code == 200
    assert response.json() == {"rounds_practised": 0, "average_total": None}


def test_progress_empty_when_list_is_empty(write_results: Callable[[list[dict]], Path]) -> None:
    write_results([])
    response = client.get("/progress")
    assert response.status_code == 200
    assert response.json() == {"rounds_practised": 0, "average_total": None}


def test_progress_malformed_file_returns_json_error(data_dir: Path) -> None:
    (data_dir / "results.json").write_text("{not valid json", encoding="utf-8")
    response = client.get("/progress")
    assert response.status_code == 500
    assert response.json() == {"detail": "Results file is unreadable."}
