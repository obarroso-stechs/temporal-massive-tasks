"""Temporal firmware update workflows."""

__all__ = ["run_firmware_update_batch", "run_worker"]


def run_firmware_update_batch(*args, **kwargs):
	# Lazy import: evita side effects al importar el paquete dentro del sandbox.
	from .client import run_firmware_update_batch as _run_firmware_update_batch

	return _run_firmware_update_batch(*args, **kwargs)


def run_worker(*args, **kwargs):
	# Lazy import: evita cargar worker/config al importar solo workflows.
	from .worker import run_worker as _run_worker

	return _run_worker(*args, **kwargs)
