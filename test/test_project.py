#!/usr/bin/env python3
from pathlib import Path

import pytest
import yaml

from manager.service.project.project import Lifecycle, ProjectApps


def test_list_project_returns_immediate_directories_with_service_yml(
    tmp_path: Path,
) -> None:
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "service.yml").write_text("name: example\n", encoding="utf-8")
    (tmp_path / "missing-manifest").mkdir()
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    (nested_dir / "nested-project").mkdir()
    (
        nested_dir / "nested-project" / "service.yml"
    ).write_text("name: nested\n", encoding="utf-8")

    assert ProjectApps(tmp_path).list_project() == [project_dir]


def test_get_project_info_migrates_v0_manifest(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "service.yml").write_text(
        "name: example\nDependencies: [database]\nlifecycle: always_on\n",
        encoding="utf-8",
    )

    project = ProjectApps(tmp_path).get_project_info(project_dir)

    assert project.schema_version == 1
    assert project.dependencies == ["database"]
    assert project.life_cycle is Lifecycle.ALWAYS_ON
    assert project.project_path == project_dir
    upgraded_manifest = yaml.safe_load(
        (project_dir / "service.yml").read_text(encoding="utf-8")
    )
    assert upgraded_manifest["schema_version"] == 1
    assert upgraded_manifest["dependencies"] == ["database"]
    assert upgraded_manifest["life_cycle"] == "always_on"
    assert "Dependencies" not in upgraded_manifest
    assert "lifecycle" not in upgraded_manifest


def test_get_project_info_accepts_manifest_path(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    manifest_path = project_dir / "service.yml"
    manifest_path.write_text(
        "schema_version: 1\nname: example\ndependencies: []\nlife_cycle: sleep\n",
        encoding="utf-8",
    )

    project = ProjectApps(tmp_path).get_project_info(manifest_path)

    assert project.name == "example"
    assert project.project_path == project_dir


def test_get_project_info_does_not_find_nested_or_root_manifest(
    tmp_path: Path,
) -> None:
    nested_project = tmp_path / "nested" / "project"
    nested_project.mkdir(parents=True)
    (nested_project / "service.yml").write_text("name: nested\n", encoding="utf-8")
    (tmp_path / "service.yml").write_text("name: root\n", encoding="utf-8")

    with pytest.raises(ValueError, match="immediate subdirectory"):
        ProjectApps(tmp_path).get_project_info(nested_project)
    with pytest.raises(ValueError, match="immediate subdirectory"):
        ProjectApps(tmp_path).get_project_info(tmp_path / "service.yml")


def test_get_project_info_rejects_unsupported_schema_version(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "service.yml").write_text(
        "schema_version: 2\nname: example\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Unsupported schema_version"):
        ProjectApps(tmp_path).get_project_info(project_dir)
