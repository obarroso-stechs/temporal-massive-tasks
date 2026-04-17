import { useState, useEffect, useCallback } from "react";
import { DS } from "../../shared/design/tokens";
import {
  Alert, Badge, Button, Card, Modal, Select, StatusBadge, Table, TextField, EmptyState,
} from "../../shared/ui/primitives";
import { reportsApi } from "../../api/reports";
import { tasksApi } from "../../api/tasks";

const FORMAT_ICONS = { PDF: "📄", WORD: "📝", EXCEL: "📊", CSV: "📋" };
const FORMAT_LABELS = { PDF: "PDF", WORD: "Word", EXCEL: "Excel", CSV: "CSV" };

const fmt = (iso) =>
  iso ? new Date(iso).toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" }) : "—";

function GenerateModal({ open, onClose, onGenerated }) {
  const [tasks, setTasks] = useState([]);
  const [taskId, setTaskId] = useState("");
  const [format, setFormat] = useState("PDF");
  const [force, setForce] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open) {
      setTaskId("");
      setFormat("PDF");
      setForce(false);
      setError(null);
      tasksApi.list().then(setTasks).catch(() => {});
    }
  }, [open]);

  const handleGenerate = async () => {
    if (!taskId) return setError("Seleccioná una tarea.");
    setGenerating(true);
    setError(null);
    try {
      await reportsApi.generate(taskId, format, force);
      onGenerated();
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Generar reporte" width="500px">
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        {tasks.length > 0 ? (
          <Select
            label="Seleccionar tarea"
            value={taskId}
            onChange={setTaskId}
            placeholder="Elegí una tarea..."
            options={tasks
              .filter((t) => !t.is_canceled)
              .map((t) => ({ value: String(t.id), label: t.task_name }))}
          />
        ) : null}
        <Select
          label="Formato"
          value={format}
          onChange={setFormat}
          required
          options={[
            { value: "PDF", label: "PDF" },
            { value: "EXCEL", label: "Excel" },
            { value: "WORD", label: "Word" },
            { value: "CSV", label: "CSV" },
          ]}
        />
        <label
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            cursor: "pointer",
            fontSize: "13px",
            color: DS.colors.neutral700,
          }}
        >
          <input type="checkbox" checked={force} onChange={(e) => setForce(e.target.checked)} />
          Forzar generación (marca dispositivos pendientes como FAILED si el workflow terminó abruptamente)
        </label>
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", paddingTop: "8px" }}>
          <Button variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button variant="success" onClick={handleGenerate} loading={generating} icon="download">
            Generar reporte
          </Button>
        </div>
      </div>
    </Modal>
  );
}

function ReportDetailModal({ open, onClose, report }) {
  if (!report) return null;

  return (
    <Modal open={open} onClose={onClose} title="Detalle del reporte" width="760px">
      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        {/* Header */}
        <div
          style={{
            display: "flex",
            gap: "16px",
            padding: "16px",
            backgroundColor: DS.colors.neutral50,
            borderRadius: DS.radius.md,
            border: `1px solid ${DS.colors.border}`,
          }}
        >
          <span style={{ fontSize: "36px" }}>{FORMAT_ICONS[report.report_format] || "📄"}</span>
          <div style={{ flex: 1 }}>
            <h4 style={{ margin: "0 0 4px", fontSize: "16px" }}>{report.task_name}</h4>
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              <Badge variant="default">{FORMAT_LABELS[report.report_format]}</Badge>
              {report.task_type && (
                <Badge variant={report.task_type === "FIRMWARE_UPDATE" ? "primary" : report.task_type === "GET_PARAMETER_VALUES" ? "success" : "info"}>
                    {report.task_type === "FIRMWARE_UPDATE" ? "Firmware" : report.task_type === "PARAMETER_SET" ? "Parameter Set" : report.task_type === "GET_PARAMETER_VALUES" ? "Get Params" : "Parámetros"}
                </Badge>
              )}
              <Badge variant={report.has_file ? "success" : "warning"}>
                {report.has_file ? "Archivo disponible" : "Sin archivo"}
              </Badge>
            </div>
          </div>
        </div>

        {/* Meta */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "8px 24px",
            padding: "14px 16px",
            backgroundColor: DS.colors.neutral50,
            borderRadius: DS.radius.md,
            border: `1px solid ${DS.colors.border}`,
            fontSize: "13px",
          }}
        >
          {[
            ["Workflow ID", report.workflow_id],
            ["Creado", fmt(report.created_at)],
          ].map(([k, v]) => (
            <div key={k} style={{ display: "flex", gap: "6px" }}>
              <span style={{ color: DS.colors.neutral600, fontWeight: 500, flexShrink: 0 }}>{k}:</span>
              <span
                style={{
                  color: DS.colors.neutral800,
                  fontFamily: k === "Workflow ID" ? DS.monoFont : undefined,
                  fontSize: k === "Workflow ID" ? "12px" : undefined,
                  wordBreak: "break-all",
                }}
              >
                {v}
              </span>
            </div>
          ))}
        </div>

        {/* Devices */}
        {report.devices?.length > 0 && (
          <div>
            <h4 style={{ margin: "0 0 12px", fontSize: "14px", fontWeight: 600 }}>
              Dispositivos ({report.devices.length})
            </h4>
            <Table
              columns={[
                {
                  key: "serial_number",
                  label: "Serial",
                  render: (v) => <span style={{ fontFamily: DS.monoFont, fontSize: "13px" }}>{v}</span>,
                },
                { key: "model", label: "Modelo", render: (v) => v || "—" },
                { key: "status", label: "Estado", render: (v) => <StatusBadge status={v} /> },
                {
                  key: "detail",
                  label: "Detalle",
                  render: (v) => (
                    <span style={{ fontSize: "12px", color: DS.colors.neutral600, whiteSpace: "pre-wrap", maxWidth: "300px", display: "block" }}>{v || "—"}</span>
                  ),
                },
              ]}
              data={report.devices}
              emptyMessage="Sin dispositivos"
            />
          </div>
        )}
      </div>
    </Modal>
  );
}

export default function ReportsSection() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [filterFormat, setFilterFormat] = useState("");
  const [generateModal, setGenerateModal] = useState(false);
  const [detailModal, setDetailModal] = useState({ open: false, report: null });
  const [detailLoading, setDetailLoading] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    reportsApi.list().then(setReports).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const openDetail = async (report) => {
    setDetailModal({ open: true, report });
    setDetailLoading(true);
    try {
      const detail = await reportsApi.getById(report.id);
      setDetailModal({ open: true, report: detail });
    } catch (e) {
      setError(e.message);
      setDetailModal({ open: false, report: null });
    } finally {
      setDetailLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await reportsApi.delete(id);
      setSuccess("Reporte eliminado.");
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const filtered = filterFormat
    ? reports.filter((r) => r.report_format === filterFormat)
    : reports;

  const stats = {
    total: reports.length,
    withFile: reports.filter((r) => r.has_file).length,
  };

  const columns = [
    {
      key: "report_format",
      label: "Formato",
      render: (v) => (
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ fontSize: "20px" }}>{FORMAT_ICONS[v] || "📄"}</span>
          <Badge variant="default">{FORMAT_LABELS[v] || v}</Badge>
        </div>
      ),
    },
    {
      key: "task_name",
      label: "Tarea",
      render: (v, row) => (
        <div>
          <p style={{ margin: 0, fontWeight: 500, fontSize: "14px" }}>{v}</p>
          {row.task_type && (
            <Badge variant={row.task_type === "FIRMWARE_UPDATE" ? "primary" : row.task_type === "GET_PARAMETER_VALUES" ? "success" : "info"} size="sm">
              {row.task_type === "FIRMWARE_UPDATE" ? "Firmware" : row.task_type === "PARAMETER_SET" ? "Parameter Set" : row.task_type === "GET_PARAMETER_VALUES" ? "Get Params" : "Parámetros"}
            </Badge>
          )}
        </div>
      ),
    },
    {
      key: "has_file",
      label: "Estado",
      render: (v) => (
        <Badge variant={v ? "success" : "warning"}>{v ? "Disponible" : "Sin archivo"}</Badge>
      ),
    },
    {
      key: "created_at",
      label: "Generado",
      render: (v) => <span style={{ fontSize: "12px" }}>{fmt(v)}</span>,
    },
    {
      key: "_actions",
      label: "",
      render: (_, row) => (
        <div style={{ display: "flex", gap: "6px", justifyContent: "flex-end" }}>
          <Button variant="ghost" size="sm" icon="eye" onClick={(e) => { e.stopPropagation(); openDetail(row); }}>
            Ver
          </Button>
          {row.has_file && (
            <a href={reportsApi.downloadUrl(row.id)} download style={{ textDecoration: "none" }}>
              <Button variant="ghost" size="sm" icon="download">
                Descargar
              </Button>
            </a>
          )}
          <Button
            variant="ghost"
            size="sm"
            icon="trash"
            style={{ color: DS.colors.error }}
            onClick={(e) => { e.stopPropagation(); handleDelete(row.id); }}
          >
            Eliminar
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ margin: "0 0 4px", fontSize: "22px", fontWeight: 700, color: DS.colors.neutral900 }}>
          Reportes
        </h2>
        <p style={{ margin: 0, fontSize: "14px", color: DS.colors.neutral600 }}>
          Generá y descargá reportes de ejecución de tareas.
        </p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      {success && <Alert type="success" message={success} onClose={() => setSuccess(null)} />}

      {/* Stats */}
      {!loading && reports.length > 0 && (
        <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap" }}>
          {[
            { label: "Total", value: stats.total, color: DS.colors.primary },
            { label: "Con archivo", value: stats.withFile, color: DS.colors.success },
            { label: "Sin archivo", value: stats.total - stats.withFile, color: DS.colors.warning },
          ].map((s) => (
            <div
              key={s.label}
              style={{
                padding: "12px 20px",
                borderRadius: DS.radius.md,
                backgroundColor: DS.colors.surface,
                border: `1px solid ${DS.colors.border}`,
                display: "flex",
                flexDirection: "column",
                gap: "2px",
                minWidth: "100px",
              }}
            >
              <span style={{ fontSize: "22px", fontWeight: 700, color: s.color }}>{s.value}</span>
              <span style={{ fontSize: "12px", color: DS.colors.neutral600 }}>{s.label}</span>
            </div>
          ))}
        </div>
      )}

      <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", gap: "16px", marginBottom: "16px", flexWrap: "wrap" }}>
        <div style={{ minWidth: "180px" }}>
          <Select
            label="Filtrar por formato"
            value={filterFormat}
            onChange={setFilterFormat}
            placeholder="Todos los formatos"
            options={[
              { value: "PDF", label: "PDF" },
              { value: "EXCEL", label: "Excel" },
              { value: "WORD", label: "Word" },
              { value: "CSV", label: "CSV" },
            ]}
          />
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <Button variant="secondary" onClick={load} size="sm">Recargar</Button>
          <Button variant="success" icon="download" onClick={() => setGenerateModal(true)}>
            Generar reporte
          </Button>
        </div>
      </div>

      {!loading && reports.length === 0 ? (
        <Card>
          <EmptyState
            icon="📊"
            title="No hay reportes generados"
            description="Generá un reporte a partir de una tarea completada para obtener un resumen descargable."
          />
        </Card>
      ) : (
        <Card padding="0">
          <Table
            columns={columns}
            data={filtered}
            loading={loading}
            onRowClick={openDetail}
            emptyMessage={filterFormat ? `Sin reportes en formato ${filterFormat}` : "No hay reportes"}
          />
        </Card>
      )}

      <GenerateModal
        open={generateModal}
        onClose={() => setGenerateModal(false)}
        onGenerated={() => { load(); setSuccess("Reporte generado correctamente."); }}
      />

      <ReportDetailModal
        open={detailModal.open}
        onClose={() => setDetailModal({ open: false, report: null })}
        report={detailLoading ? null : detailModal.report}
      />
    </div>
  );
}
