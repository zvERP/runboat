from pathlib import Path

import pytest

from runboat.exceptions import RepoOrBranchNotSupported
from runboat.settings import BuildLocation, BuildSettings, settings


def test_get_build_settings() -> None:
    assert settings.get_build_settings("OCA/mis-builder", "15.0") == [
        BuildSettings(image="ghcr.io/oca/oca-ci/py3.8-odoo15.0:latest")
    ]
    with pytest.raises(RepoOrBranchNotSupported):
        settings.get_build_settings("acsone/mis-builder", "15.0")
    with pytest.raises(RepoOrBranchNotSupported):
        assert not settings.get_build_settings("OCA/mis-builder", "15.0-stuff")
    assert settings.get_build_settings("OCA/mis-builder", "15.0") == [
        BuildSettings(image="ghcr.io/oca/oca-ci/py3.8-odoo15.0:latest")
    ]
    assert settings.get_build_settings("OCA/mis-builder", "16.0") == [
        BuildSettings(
            image="ghcr.io/oca/oca-ci/py3.10-odoo16.0:latest",
            kubefiles_path=Path("/tmp"),
        )
    ]


def test_select_build_location_is_stable(monkeypatch: pytest.MonkeyPatch) -> None:
    locations = [
        BuildLocation(
            name=name,
            node_selector={"topology.kubernetes.io/zone": name},
            env={"PGHOST": f"postgres-{name}"},
        )
        for name in ("nbg1", "fsn1", "hel1")
    ]
    monkeypatch.setattr(settings, "build_locations", locations)

    selected = settings.select_build_location("b123")
    assert selected is not None
    assert settings.select_build_location("b123") == selected
    assert settings.get_build_location(selected.name) == selected
