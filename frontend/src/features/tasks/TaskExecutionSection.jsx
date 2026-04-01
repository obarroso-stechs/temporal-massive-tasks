import { useState, useEffect, useCallback } from "react";
import { DS } from "../../shared/design/tokens";
import {
  Alert, Badge, Button, Card, Modal, Select, StatusBadge,
  StatusBar, Spinner, Table, Tabs, TextField, Textarea,
} from "../../shared/ui/primitives";
import { tasksApi } from "../../api/tasks";
import { groupsApi } from "../../api/groups";
import { firmwareApi, parameterApi, parameterSetApi } from "../../api/workflows";

const fmt = (iso) =>
  iso ? new Date(iso).toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" }) : "—";

const duration = (start, end) => {
  if (!start || !end) return "—";
  const ms = new Date(end) - new Date(start);
  const s = Math.floor(ms / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  return `${m}m ${s % 60}s`;
};

const TASK_TYPE_LABELS = {
  FIRMWARE_UPDATE: "Firmware Update",
  PARAMETER_UPDATE: "Parameter Update",
  PARAMETER_SET: "Parameter Set",
};

const TASK_API_BY_TYPE = {
  FIRMWARE_UPDATE: firmwareApi,
  PARAMETER_UPDATE: parameterApi,
  PARAMETER_SET: parameterSetApi,
};

function parseParameterSetInput(raw) {
  const parameters = {};
  const lines = raw
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  for (const line of lines) {
    const separatorIndex = line.indexOf(":");
    if (separatorIndex <= 0 || separatorIndex === line.length - 1) {
      throw new Error(`Formato inválido en línea: "${line}". Usá path: value.`);
    }

    const key = line.slice(0, separatorIndex).trim();
    const rawValue = line.slice(separatorIndex + 1).trim();

    if (!key || !rawValue) {
      throw new Error(`Formato inválido en línea: "${line}". Usá path: value.`);
    }

    const lowered = rawValue.toLowerCase();
    if (lowered === "true") {
      parameters[key] = true;
      continue;
    }
    if (lowered === "false") {
      parameters[key] = false;
      continue;
    }

    const numeric = Number(rawValue);
    if (!Number.isNaN(numeric) && rawValue !== "") {
      parameters[key] = rawValue.includes(".") ? numeric : Number.parseInt(rawValue, 10);
      continue;
    }

    parameters[key] = rawValue;
  }

  if (!Object.keys(parameters).length) {
    throw new Error("Ingresá al menos un parámetro en formato path: value.");
  }

  return parameters;
}

// ── Device event timeline modal ─────────────────────────────────────────────

function DeviceEventModal({ open, onClose, taskType, workflowId, serialNumber }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!open || !workflowId || !serialNumber) return;
    setLoading(true);
    setError(null);
    setData(null);

    const fetcher = TASK_API_BY_TYPE[taskType]?.getDeviceStatus;
    if (!fetcher) {
      setError(`Tipo de tarea no soportado: ${taskType}`);
      setLoading(false);
      return;
    }

    fetcher(workflowId, serialNumber)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [open, workflowId, serialNumber, taskType]);

  return (
    <Modal open={open} onClose={onClose} title={`Dispositivo: ${serialNumber}`} width="700px">
      {loading && (
        <div style={{ display: "flex", justifyContent: "center", padding: "32px" }}>
          <Spinner size={36} />
        </div>
      )}
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      {data && (
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "16px",
              padding: "16px",
              borderRadius: DS.radius.md,
              backgroundColor: DS.colors.neutral50,
              border: `1px solid ${DS.colors.border}`,
            }}
          >
            <div style={{ flex: 1 }}>
              <p style={{ margin: 0, fontSize: "12px", color: DS.colors.neutral600, fontWeight: 500 }}>
                WORKFLOW ID
              </p>
              <p
                style={{
                  margin: "2px 0 0",
                  fontSize: "12px",
                  fontFamily: DS.monoFont,
                  color: DS.colors.neutral800,
                  wordBreak: "break-all",
                }}
              >
                {data.workflow_id}
              </p>
            </div>
            <StatusBadge status={data.status} />
          </div>

          {data.message && (
            <div
              style={{
                padding: "12px 16px",
                borderRadius: DS.radius.md,
                backgroundColor: DS.colors.infoLight,
                color: DS.colors.info,
                fontSize: "13px",
              }}
            >
              {data.message}
            </div>
          )}

          <div>
            <h4 style={{ margin: "0 0 12px", fontSize: "14px", fontWeight: 600, color: DS.colors.neutral800 }}>
              Historial de eventos ({data.events?.length ?? 0})
            </h4>
            {!data.events?.length ? (
              <p style={{ color: DS.colors.neutral500, fontSize: "13px" }}>Sin eventos registrados.</p>
            ) : (
              <div
                style={{
                  borderLeft: `2px solid ${DS.colors.border}`,
                  marginLeft: "8px",
                  paddingLeft: "16px",
                }}
              >
                {data.events.map((ev, i) => (
                  <div key={ev.event_id ?? i} style={{ position: "relative", paddingBottom: "16px" }}>
                    <div
                      style={{
                        position: "absolute",
                        left: "-23px",
                        top: "4px",
                        width: "10px",
                        height: "10px",
                        borderRadius: "50%",
                        backgroundColor: DS.colors.primary,
                        border: `2px solid ${DS.colors.white}`,
                      }}
                    />
                    <div style={{ display: "flex", alignItems: "baseline", gap: "8px", flexWrap: "wrap" }}>
                      <span
                        style={{
                          fontSize: "12px",
                          fontWeight: 600,
                          backgroundColor: DS.colors.primaryLight,
                          color: DS.colors.primaryDark,
                          padding: "2px 8px",
                          borderRadius: DS.radius.sm,
                        }}
                      >
                        {ev.event_type}
                      </span>
                      <span style={{ fontSize: "12px", color: DS.colors.neutral500 }}>
                        {ev.timestamp ? fmt(ev.timestamp) : `#${ev.event_id}`}
                      </span>
                    </div>
                    {ev.details && Object.keys(ev.details).length > 0 && (
                      <pre
                        style={{
                          margin: "6px 0 0",
                          padding: "8px 12px",
                          backgroundColor: DS.colors.neutral50,
                          borderRadius: DS.radius.sm,
                          fontSize: "11px",
                          fontFamily: DS.monoFont,
                          color: DS.colors.neutral700,
                          overflowX: "auto",
                          whiteSpace: "pre-wrap",
                          wordBreak: "break-all",
                        }}
                      >
                        {JSON.stringify(ev.details, null, 2)}
                      </pre>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
}

// ── Live workflow status modal (real-time from Temporal) ─────────────────────

function WorkflowLiveStatusModal({ open, onClose, onRefresh, task }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const [localPaused, setLocalPaused] = useState(false);

  const getApi = useCallback(() => {
    if (!task?.task_type) return null;
    return TASK_API_BY_TYPE[task.task_type] ?? null;
  }, [task]);

  const fetch = useCallback(() => {
    if (!task) return;
    const apiClient = getApi();
    if (!apiClient) {
      setError(`Tipo de tarea no soportado: ${task.task_type}`);
      return;
    }
    setLoading(true);
    setError(null);
    apiClient.getBatchStatus(task.workflow_id)
      .then((d) => { setData(d); setLocalPaused(d.is_paused ?? false); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [task, getApi]);

  useEffect(() => {
    if (open) { fetch(); }
    else { setData(null); setError(null); setActionLoading(null); setLocalPaused(false); }
  }, [open, fetch]);

  const handlePause = async () => {
    const apiClient = getApi();
    if (!apiClient) return;
    setActionLoading("pause");
    try {
      await apiClient.pauseBatch(task.workflow_id);
      setLocalPaused(true);
    } catch (e) {
      setError(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleResume = async () => {
    const apiClient = getApi();
    if (!apiClient) return;
    setActionLoading("resume");
    try {
      await apiClient.resumeBatch(task.workflow_id);
      setLocalPaused(false);
    } catch (e) {
      setError(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleCancel = async () => {
    if (!window.confirm("¿Cancelar el batch? Los dispositivos pendientes quedarán como CANCELED.")) return;
    const apiClient = getApi();
    if (!apiClient) return;
    setActionLoading("cancel");
    try {
      await apiClient.cancelBatch(task.workflow_id);
      setTimeout(fetch, 1500);
    } catch (e) {
      setError(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const isRunning = data?.status === "RUNNING";

  const STATUS_COLORS = {
    COMPLETED: "#1E8E3E",
    RUNNING: DS.colors.primary,
    PENDING: "#9AA0A6",
    FAILED: "#D93025",
    TIMED_OUT: "#E37400",
    TERMINATED: "#5F6368",
    CANCELED: "#5F6368",
  };

  const deviceColumns = [
    {
      key: "serial_number",
      label: "Serial",
      render: (v) => <span style={{ fontFamily: DS.monoFont, fontSize: "13px" }}>{v}</span>,
    },
    {
      key: "status",
      label: "Estado",
      render: (v) => <StatusBadge status={v} />,
    },
    {
      key: "message",
      label: "Mensaje",
      render: (v) => (
        <span
          title={v}
          style={{
            fontSize: "12px",
            color: DS.colors.neutral600,
            display: "block",
            maxWidth: "220px",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {v || "—"}
        </span>
      ),
    },
  ];

  return (
    <>
      <Modal open={open} onClose={() => { onRefresh?.(); onClose(); }} title="Estado en tiempo real" width="860px">
        {/* Toolbar */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
          <span
            style={{
              fontSize: "12px",
              fontFamily: DS.monoFont,
              color: DS.colors.neutral600,
              flex: 1,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {task?.workflow_id}
          </span>
          {isRunning && !localPaused && (
            <Button
              variant="secondary"
              size="sm"
              onClick={handlePause}
              loading={actionLoading === "pause"}
              disabled={!!actionLoading}
            >
              Pausar
            </Button>
          )}
          {isRunning && localPaused && (
            <Button
              variant="secondary"
              size="sm"
              onClick={handleResume}
              loading={actionLoading === "resume"}
              disabled={!!actionLoading}
            >
              Reanudar
            </Button>
          )}
          {isRunning && (
            <Button
              variant="danger"
              size="sm"
              onClick={handleCancel}
              loading={actionLoading === "cancel"}
              disabled={!!actionLoading}
            >
              Cancelar
            </Button>
          )}
          <Button variant="secondary" size="sm" onClick={fetch} loading={loading} disabled={!!actionLoading}>
            Actualizar
          </Button>
        </div>

        {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

        {loading && !data && (
          <div style={{ display: "flex", justifyContent: "center", padding: "32px" }}>
            <Spinner size={36} />
          </div>
        )}

        {data && (
          <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            {/* Overall status + progress counters */}
            <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", alignItems: "center" }}>
              <div
                style={{
                  padding: "10px 18px",
                  borderRadius: DS.radius.md,
                  backgroundColor: DS.colors.neutral50,
                  border: `1px solid ${DS.colors.border}`,
                  display: "flex",
                  flexDirection: "column",
                  gap: "2px",
                  minWidth: "80px",
                }}
              >
                <span
                  style={{
                    fontSize: "11px",
                    fontWeight: 600,
                    color: DS.colors.neutral500,
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                  }}
                >
                  Workflow
                </span>
                <span
                  style={{
                    fontSize: "14px",
                    fontWeight: 700,
                    color: STATUS_COLORS[data.status] ?? DS.colors.neutral800,
                  }}
                >
                  {data.status}
                </span>
              </div>
              {data.progress &&
                [
                  { label: "Total", value: data.progress.total, color: DS.colors.primary },
                  { label: "Procesados", value: data.progress.processed, color: "#1E8E3E" },
                  { label: "Pendientes", value: data.progress.pending, color: "#9AA0A6" },
                  { label: "Fallidos", value: data.progress.failed, color: "#D93025" },
                ].map((s) => (
                  <div
                    key={s.label}
                    style={{
                      padding: "10px 18px",
                      borderRadius: DS.radius.md,
                      backgroundColor: DS.colors.neutral50,
                      border: `1px solid ${DS.colors.border}`,
                      display: "flex",
                      flexDirection: "column",
                      gap: "2px",
                      minWidth: "80px",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "20px",
                        fontWeight: 700,
                        color: s.color,
                        lineHeight: 1,
                      }}
                    >
                      {s.value}
                    </span>
                    <span style={{ fontSize: "11px", color: DS.colors.neutral600 }}>{s.label}</span>
                  </div>
                ))}
            </div>

            {/* Status distribution bar */}
            <StatusBar devices={data.devices} total={data.progress?.total ?? data.devices.length} />

            {/* Device table */}
            <div>
              <p style={{ margin: "0 0 10px", fontSize: "13px", color: DS.colors.neutral500 }}>
                Hacé click en un dispositivo para ver el historial de eventos.
              </p>
              <Table
                columns={deviceColumns}
                data={data.devices}
                emptyMessage="Sin dispositivos"
                onRowClick={(row) =>
                  setSelectedDevice({ serial: row.serial_number, workflowId: task.workflow_id })
                }
              />
            </div>
          </div>
        )}
      </Modal>

      <DeviceEventModal
        open={!!selectedDevice}
        onClose={() => setSelectedDevice(null)}
        taskType={task?.task_type}
        workflowId={selectedDevice?.workflowId}
        serialNumber={selectedDevice?.serial}
      />
    </>
  );
}

// ── Batch form (shared between firmware and parameter update) ────────────────

function BatchForm({ type, groups, onSubmit, loading }) {
  const [mode, setMode] = useState("serials");
  const [serials, setSerials] = useState("");
  const [groupId, setGroupId] = useState("");
  const [filename, setFilename] = useState("");
  const [parameterMap, setParameterMap] = useState("");
  const [scheduleMode, setScheduleMode] = useState("now");
  const [startAt, setStartAt] = useState("");
  const [error, setError] = useState(null);

  const isFirmware = type === "firmware";
  const isParameterSet = type === "parameter-set";

  const handleSubmit = () => {
    setError(null);
    if (isFirmware) {
      if (!filename.trim()) return setError("El nombre del archivo es obligatorio.");
      if (!filename.trim().endsWith(".bin")) return setError("El archivo debe tener extensión .bin");
    }
    if (scheduleMode === "schedule" && !startAt) {
      return setError("Seleccioná una fecha y hora de inicio.");
    }

    let body;
    if (mode === "serials") {
      const items = serials.split("\n").map((s) => s.trim()).filter(Boolean);
      if (!items.length) return setError("Ingresá al menos un número de serie.");
      body = { items: items.map((s) => ({ serialNumber: s })) };
    } else {
      if (!groupId) return setError("Seleccioná un grupo.");
      body = { group_id: Number(groupId) };
    }

    if (isParameterSet) {
      try {
        body = {
          ...body,
          parameters: parseParameterSetInput(parameterMap),
        };
      } catch (e) {
        setError(e.message);
        return;
      }
    }

    if (scheduleMode === "schedule") {
      body = { ...body, start_at: new Date(startAt).toISOString() };
    }

    onSubmit({ body, filename: filename.trim(), scheduleMode });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      {/* Mode switcher */}
      <div
        style={{
          display: "flex",
          border: `1px solid ${DS.colors.border}`,
          borderRadius: DS.radius.md,
          overflow: "hidden",
          width: "fit-content",
        }}
      >
        {[
          { key: "serials", label: "Por seriales" },
          { key: "group", label: "Por grupo" },
        ].map((m) => (
          <button
            key={m.key}
            onClick={() => setMode(m.key)}
            style={{
              padding: "8px 18px",
              border: "none",
              cursor: "pointer",
              fontFamily: DS.font,
              fontSize: "13px",
              fontWeight: 500,
              backgroundColor: mode === m.key ? DS.colors.primary : DS.colors.white,
              color: mode === m.key ? DS.colors.white : DS.colors.neutral700,
              transition: "all 0.15s",
            }}
          >
            {m.label}
          </button>
        ))}
      </div>

      {mode === "serials" ? (
        <Textarea
          label="Números de serie (uno por línea)"
          placeholder={"SN-001\nSN-002\nSN-003"}
          value={serials}
          onChange={setSerials}
          rows={6}
          required
        />
      ) : (
        <Select
          label="Grupo de dispositivos"
          value={groupId}
          onChange={setGroupId}
          placeholder="Seleccioná un grupo..."
          required
          options={groups.map((g) => ({
            value: String(g.id),
            label: `${g.name}${g.devices?.length ? ` (${g.devices.length} disp.)` : ""}`,
          }))}
        />
      )}

      {isFirmware && (
        <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
          <label style={{ fontSize: "13px", fontWeight: 500, color: DS.colors.neutral800 }}>
            Archivo de firmware <span style={{ color: DS.colors.error }}>*</span>
          </label>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
            <label
              style={{
                display: "inline-flex",
                alignItems: "center",
                padding: "9px 16px",
                borderRadius: DS.radius.md,
                border: `1px solid ${DS.colors.border}`,
                backgroundColor: DS.colors.white,
                cursor: "pointer",
                fontSize: "13px",
                fontFamily: DS.font,
                color: DS.colors.neutral700,
                whiteSpace: "nowrap",
              }}
            >
              Seleccionar archivo .bin
              <input
                type="file"
                accept=".bin"
                style={{ display: "none" }}
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) setFilename(file.name);
                }}
              />
            </label>
            {filename ? (
              <span style={{ fontSize: "13px", color: DS.colors.neutral700, fontFamily: DS.monoFont, wordBreak: "break-all" }}>
                {filename}
              </span>
            ) : (
              <span style={{ fontSize: "12px", color: DS.colors.neutral500 }}>Ningún archivo seleccionado</span>
            )}
          </div>
          <span style={{ fontSize: "12px", color: DS.colors.neutral500 }}>Debe tener extensión .bin</span>
        </div>
      )}

      {isParameterSet && (
        <Textarea
          label="Parámetros a setear (path: value, uno por línea)"
          placeholder={"Device.WiFi.SSID.1.SSID: stechs-demo\nDevice.WiFi.SSID.1.Enable: true\nDevice.Custom.Param: 123"}
          value={parameterMap}
          onChange={setParameterMap}
          rows={6}
          required
          helper="Tipos soportados: string, boolean, int y float"
        />
      )}

      {/* Execution mode */}
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <label style={{ fontSize: "13px", fontWeight: 500, color: DS.colors.neutral800 }}>Ejecución</label>
        <div style={{ display: "flex", gap: "20px" }}>
          {[
            { key: "now", label: "Ejecutar ahora" },
            { key: "schedule", label: "Programar" },
          ].map((s) => (
            <label
              key={s.key}
              style={{ display: "flex", alignItems: "center", gap: "6px", cursor: "pointer", fontSize: "14px" }}
            >
              <input type="radio" checked={scheduleMode === s.key} onChange={() => setScheduleMode(s.key)} />
              {s.label}
            </label>
          ))}
        </div>
        {scheduleMode === "schedule" && (
          <TextField
            label="Fecha y hora de inicio"
            type="datetime-local"
            value={startAt}
            onChange={setStartAt}
            required
          />
        )}
      </div>

      <Button variant="success" onClick={handleSubmit} loading={loading} icon="play">
        {scheduleMode === "now" ? "Ejecutar ahora" : "Programar tarea"}
      </Button>
    </div>
  );
}

// ── Task history tab ─────────────────────────────────────────────────────────

function TaskHistoryTab() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [liveTask, setLiveTask] = useState(null);
  const [filterType, setFilterType] = useState("");

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    tasksApi
      .list(filterType ? { task_type: filterType } : {})
      .then(setTasks)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [filterType]);

  useEffect(() => { load(); }, [load]);

  const columns = [
    {
      key: "task_name",
      label: "Nombre",
      render: (v, row) => (
        <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
          <span style={{ fontWeight: 500 }}>{v}</span>
          {row.scheduled_at && !row.started_at && (
            <Badge variant="warning" size="sm">Programado · {fmt(row.scheduled_at)}</Badge>
          )}
        </div>
      ),
    },
    {
      key: "task_type",
      label: "Tipo",
      render: (v) => (
        <Badge variant={v === "FIRMWARE_UPDATE" ? "primary" : v === "PARAMETER_SET" ? "warning" : "info"}>
          {TASK_TYPE_LABELS[v] || v}
        </Badge>
      ),
    },
    {
      key: "created_at",
      label: "Creado",
      render: (v) => <span style={{ fontSize: "12px" }}>{fmt(v)}</span>,
    },
    {
      key: "started_at",
      label: "Inicio",
      render: (v) => <span style={{ fontSize: "12px" }}>{fmt(v)}</span>,
    },
    {
      key: "end_at",
      label: "Fin / Duración",
      render: (v, row) => (
        <div style={{ display: "flex", flexDirection: "column", gap: "2px" }}>
          <span style={{ fontSize: "12px" }}>{fmt(v)}</span>
          <span style={{ fontSize: "11px", color: DS.colors.neutral500 }}>
            {duration(row.started_at, v)}
          </span>
        </div>
      ),
    },
    {
      key: "_live",
      label: "",
      render: (_, row) => (
        <Button
          variant="ghost"
          size="sm"
          icon="refresh"
          onClick={(e) => { e.stopPropagation(); setLiveTask(row); }}
        >
          Actualizar
        </Button>
      ),
    },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      <div style={{ display: "flex", alignItems: "flex-end", gap: "12px", flexWrap: "wrap" }}>
        <div style={{ minWidth: "200px" }}>
          <Select
            label="Filtrar por tipo"
            value={filterType}
            onChange={(v) => setFilterType(v)}
            placeholder="Todos los tipos"
            options={[
              { value: "FIRMWARE_UPDATE", label: "Firmware Update" },
              { value: "PARAMETER_UPDATE", label: "Parameter Update" },
              { value: "PARAMETER_SET", label: "Parameter Set" },
            ]}
          />
        </div>
        <span style={{ fontSize: "12px", color: DS.colors.neutral500, marginLeft: "4px" }}>
          Click en una fila para ver el estado en tiempo real por dispositivo.
        </span>
      </div>

      <Card padding="0">
        <Table
          columns={columns}
          data={tasks}
          loading={loading}
          onRowClick={(row) => setLiveTask(row)}
          emptyMessage="No hay tareas registradas aún"
        />
      </Card>

      <WorkflowLiveStatusModal
        open={liveTask != null}
        onClose={() => setLiveTask(null)}
        onRefresh={load}
        task={liveTask}
      />
    </div>
  );
}

// ── Main section ─────────────────────────────────────────────────────────────

export default function TaskExecutionSection() {
  const [activeTab, setActiveTab] = useState("firmware");
  const [groups, setGroups] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    groupsApi.list().then(setGroups).catch(() => {});
  }, []);

  const handleFirmwareSubmit = async ({ body, filename, scheduleMode }) => {
    setSubmitting(true);
    setAlert(null);
    try {
      if (scheduleMode === "now") {
        await firmwareApi.startBatch(body, filename);
      } else {
        await firmwareApi.scheduleBatch(body, filename);
      }
      setAlert({ type: "success", message: "Tarea de firmware lanzada correctamente. Podés seguir el progreso en Historial." });
    } catch (e) {
      setAlert({ type: "error", message: e.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleParameterSubmit = async ({ body, scheduleMode }) => {
    setSubmitting(true);
    setAlert(null);
    try {
      if (scheduleMode === "now") {
        await parameterApi.startBatch(body);
      } else {
        await parameterApi.scheduleBatch(body);
      }
      setAlert({ type: "success", message: "Tarea de parámetros lanzada correctamente. Podés seguir el progreso en Historial." });
    } catch (e) {
      setAlert({ type: "error", message: e.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleParameterSetSubmit = async ({ body, scheduleMode }) => {
    setSubmitting(true);
    setAlert(null);
    try {
      if (scheduleMode === "now") {
        await parameterSetApi.startBatch(body);
      } else {
        await parameterSetApi.scheduleBatch(body);
      }
      setAlert({ type: "success", message: "Tarea de parameter set lanzada correctamente. Podés seguir el progreso en Historial." });
    } catch (e) {
      setAlert({ type: "error", message: e.message });
    } finally {
      setSubmitting(false);
    }
  };

  const tabs = [
    { key: "firmware", label: "Actualizar Firmware" },
    { key: "parameter", label: "Actualizar Parámetros" },
    { key: "parameter-set", label: "Set de Parámetros" },
    { key: "history", label: "Historial de Tareas" },
  ];

  return (
    <div>
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ margin: "0 0 4px", fontSize: "22px", fontWeight: 700, color: DS.colors.neutral900 }}>
          Gestión de Tareas
        </h2>
        <p style={{ margin: 0, fontSize: "14px", color: DS.colors.neutral600 }}>
          Ejecutá tareas masivas de firmware, actualización de parámetros y set de parámetros en dispositivos o grupos.
        </p>
      </div>

      <Tabs tabs={tabs} active={activeTab} onChange={setActiveTab} />

      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}

      {activeTab === "firmware" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "24px" }}>
          <Card>
            <h3 style={{ margin: "0 0 20px", fontSize: "16px", fontWeight: 600 }}>
              Actualización de Firmware
            </h3>
            <BatchForm type="firmware" groups={groups} onSubmit={handleFirmwareSubmit} loading={submitting} />
          </Card>
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <Card style={{ backgroundColor: DS.colors.neutral50 }}>
              <h4 style={{ margin: "0 0 12px", fontSize: "13px", fontWeight: 600, color: DS.colors.neutral700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                Pasos
              </h4>
              <ol style={{ margin: 0, paddingLeft: "18px", display: "flex", flexDirection: "column", gap: "10px" }}>
                {[
                  "Seleccioná seriales individuales o un grupo.",
                  "Seleccioná el archivo .bin.",
                  "Elegí ejecutar ahora o programar.",
                  "Monitoreá en Historial de Tareas.",
                ].map((step, i) => (
                  <li key={i} style={{ fontSize: "13px", color: DS.colors.neutral600, lineHeight: 1.5 }}>
                    {step}
                  </li>
                ))}
              </ol>
            </Card>
          </div>
        </div>
      )}

      {activeTab === "parameter" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "24px" }}>
          <Card>
            <h3 style={{ margin: "0 0 20px", fontSize: "16px", fontWeight: 600 }}>
              Actualización de Parámetros
            </h3>
            <BatchForm type="parameter" groups={groups} onSubmit={handleParameterSubmit} loading={submitting} />
          </Card>
          <Card style={{ backgroundColor: DS.colors.neutral50 }}>
            <h4 style={{ margin: "0 0 12px", fontSize: "13px", fontWeight: 600, color: DS.colors.neutral700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Información
            </h4>
            <p style={{ margin: 0, fontSize: "13px", color: DS.colors.neutral600, lineHeight: 1.6 }}>
              La actualización se ejecuta en paralelo en todos los dispositivos del lote. Un fallo en un dispositivo no afecta a los demás.
            </p>
          </Card>
        </div>
      )}

      {activeTab === "parameter-set" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "24px" }}>
          <Card>
            <h3 style={{ margin: "0 0 20px", fontSize: "16px", fontWeight: 600 }}>
              Set de Parámetros
            </h3>
            <BatchForm type="parameter-set" groups={groups} onSubmit={handleParameterSetSubmit} loading={submitting} />
          </Card>
          <Card style={{ backgroundColor: DS.colors.neutral50 }}>
            <h4 style={{ margin: "0 0 12px", fontSize: "13px", fontWeight: 600, color: DS.colors.neutral700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Formato
            </h4>
            <p style={{ margin: 0, fontSize: "13px", color: DS.colors.neutral600, lineHeight: 1.6 }}>
              Ingresá un parámetro por línea con formato <strong>path: value</strong>. Ejemplo: Device.WiFi.SSID.1.Enable: true.
            </p>
          </Card>
        </div>
      )}

      {activeTab === "history" && <TaskHistoryTab />}
    </div>
  );
}
