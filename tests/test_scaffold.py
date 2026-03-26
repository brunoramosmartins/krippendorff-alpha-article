"""Sanity checks for the Phase 0 repository scaffold."""


def test_src_package_version() -> None:
    import src

    assert src.__version__ == "0.1.0"
