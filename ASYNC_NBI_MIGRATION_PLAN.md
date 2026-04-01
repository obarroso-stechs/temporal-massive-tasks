# Async NBI Migration Plan

## Goal
Implement a new async NBI client in a separate package and migrate Temporal NBI activities to use it.

## Scope
- Create package `nbi_client_async/` from scratch.
- Keep existing `nbi/` client untouched for backward compatibility.
- Migrate Temporal activities that call NBI endpoints:
  - `temporal/activities/common_activities.py`
  - `temporal/activities/firmware_activities.py`
  - `temporal/activities/parameter_update_activities.py`
- Keep reporting activities sync for now because they use sync repositories/services.

## Execution Steps
1. Add async runtime dependency:
   - Add `httpx` to `requirements.txt`.
2. Create `nbi_client_async` package:
   - `nbi_client_async/__init__.py`
   - `nbi_client_async/client.py`
   - `nbi_client_async/services/__init__.py`
   - `nbi_client_async/services/base.py`
   - `nbi_client_async/services/devices.py`
   - `nbi_client_async/services/files.py`
3. Implement async HTTP foundation:
   - Use `httpx.AsyncClient`.
   - Preserve current auth and JSON behavior.
   - Support pydantic/dataclass/dict body serialization.
4. Implement async domain methods required by Temporal:
   - Devices: `list`, `get_parameter`, `set_parameter`
   - Files: `download`
5. Migrate Temporal activities to `async def`:
   - Use `async with AsyncNbiClient(NbiConfig())`.
   - Replace sync calls with awaitable calls.
6. Preserve compatibility in worker:
   - Keep `activity_executor` because reporting activities are still sync.
7. Validate:
   - Run static error check for edited files.
   - Run worker import/syntax check.

## Post-Migration Follow-up
- Optional phase: migrate reporting activities and DB sync services to async to fully remove sync path.
- Optional phase: remove old `nbi/` sync client once all consumers are migrated.
