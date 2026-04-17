import { useState, useEffect, useCallback } from "react";
import { DS } from "../../shared/design/tokens";
import {
  Alert, Button, Card, Modal, Table, TextField, EmptyState,
} from "../../shared/ui/primitives";
import { devicesApi } from "../../api/devices";

const EMPTY_FORM = {
  serial_number: "",
  description: "",
  manufacturer: "",
  model: "",
  software_version: "",
  firmware_version: "",
};

function DeviceFormModal({ open, onClose, initial, onSaved }) {
  const isEdit = !!initial;
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open) {
      setForm(initial ? { ...EMPTY_FORM, ...initial } : EMPTY_FORM);
      setError(null);
    }
  }, [open, initial]);

  const set = (key) => (val) => setForm((f) => ({ ...f, [key]: val }));

  const handleSave = async () => {
    if (!form.serial_number.trim()) return setError("El número de serie es obligatorio.");
    setSaving(true);
    setError(null);
    try {
      const payload = {
        description: form.description || null,
        manufacturer: form.manufacturer || null,
        model: form.model || null,
        software_version: form.software_version || null,
        firmware_version: form.firmware_version || null,
      };
      if (isEdit) {
        await devicesApi.update(form.serial_number, payload);
      } else {
        await devicesApi.create({ serial_number: form.serial_number.trim(), ...payload });
      }
      onSaved();
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={isEdit ? `Editar · ${initial?.serial_number}` : "Nuevo dispositivo"}
    >
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        <TextField
          label="Número de serie"
          value={form.serial_number}
          onChange={set("serial_number")}
          placeholder="SN-001"
          required
          disabled={isEdit}
        />
        <TextField
          label="Descripción"
          value={form.description}
          onChange={set("description")}
          placeholder="Router principal sala B"
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
          <TextField label="Fabricante" value={form.manufacturer} onChange={set("manufacturer")} placeholder="Cisco" />
          <TextField label="Modelo" value={form.model} onChange={set("model")} placeholder="ISR-4321" />
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
          <TextField label="Versión de software" value={form.software_version} onChange={set("software_version")} placeholder="16.9.4" />
          <TextField label="Versión de firmware" value={form.firmware_version} onChange={set("firmware_version")} placeholder="2.1.0" />
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", paddingTop: "8px" }}>
          <Button variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button variant="success" onClick={handleSave} loading={saving}>
            {isEdit ? "Guardar cambios" : "Crear dispositivo"}
          </Button>
        </div>
      </div>
    </Modal>
  );
}

function DeleteModal({ open, onClose, device, onDeleted }) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState(null);

  const handleDelete = async () => {
    setDeleting(true);
    setError(null);
    try {
      await devicesApi.delete(device.serial_number);
      onDeleted();
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Eliminar dispositivo" width="440px">
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      <p style={{ margin: "0 0 20px", fontSize: "14px", color: DS.colors.neutral700 }}>
        ¿Eliminar{" "}
        <strong style={{ fontFamily: DS.monoFont }}>{device?.serial_number}</strong>? Esta acción no se puede deshacer.
      </p>
      <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px" }}>
        <Button variant="secondary" onClick={onClose}>Cancelar</Button>
        <Button variant="danger" onClick={handleDelete} loading={deleting}>Eliminar</Button>
      </div>
    </Modal>
  );
}

export default function DevicesSection() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [formModal, setFormModal] = useState({ open: false, device: null });
  const [deleteModal, setDeleteModal] = useState({ open: false, device: null });

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    devicesApi.list().then(setDevices).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = devices.filter((d) => {
    const q = search.toLowerCase();
    return (
      d.serial_number?.toLowerCase().includes(q) ||
      d.model?.toLowerCase().includes(q) ||
      d.manufacturer?.toLowerCase().includes(q) ||
      d.description?.toLowerCase().includes(q)
    );
  });

  const mono = (v) => v ? <span style={{ fontFamily: DS.monoFont, fontSize: "12px" }}>{v}</span> : <span style={{ color: DS.colors.neutral400 }}>—</span>;
  const plain = (v) => v || <span style={{ color: DS.colors.neutral400 }}>—</span>;

  const columns = [
    {
      key: "serial_number",
      label: "Serial",
      render: (v) => <span style={{ fontFamily: DS.monoFont, fontSize: "13px", fontWeight: 600 }}>{v}</span>,
    },
    { key: "description", label: "Descripción", render: plain },
    { key: "manufacturer", label: "Fabricante", render: plain },
    { key: "model", label: "Modelo", render: plain },
    { key: "firmware_version", label: "Firmware", render: mono },
    { key: "software_version", label: "Software", render: mono },
    {
      key: "_actions",
      label: "",
      render: (_, row) => (
        <div style={{ display: "flex", gap: "6px", justifyContent: "flex-end" }}>
          <Button variant="ghost" size="sm" icon="edit" onClick={(e) => { e.stopPropagation(); setFormModal({ open: true, device: row }); }}>
            Editar
          </Button>
          <Button
            variant="ghost"
            size="sm"
            icon="trash"
            style={{ color: DS.colors.error }}
            onClick={(e) => { e.stopPropagation(); setDeleteModal({ open: true, device: row }); }}
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
          Gestión de Dispositivos
        </h2>
        <p style={{ margin: 0, fontSize: "14px", color: DS.colors.neutral600 }}>
          Inventario de dispositivos de red disponibles para actualizaciones.
        </p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", gap: "16px", marginBottom: "16px", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: "200px", maxWidth: "360px" }}>
          <TextField placeholder="Buscar por serial, modelo, fabricante..." value={search} onChange={setSearch} />
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <Button variant="secondary" onClick={load} size="sm">Recargar</Button>
          <Button variant="success" icon="plus" onClick={() => setFormModal({ open: true, device: null })}>
            Nuevo dispositivo
          </Button>
        </div>
      </div>

      {!loading && devices.length === 0 ? (
        <Card>
          <EmptyState
            icon="📡"
            title="No hay dispositivos registrados"
            description="Agregá tu primer dispositivo para comenzar a gestionar actualizaciones masivas."
          />
        </Card>
      ) : (
        <Card padding="0">
          <Table columns={columns} data={filtered} loading={loading} emptyMessage={search ? `Sin resultados para "${search}"` : "No hay dispositivos"} />
          {!loading && (
            <div style={{ padding: "10px 16px", borderTop: `1px solid ${DS.colors.neutral100}`, fontSize: "12px", color: DS.colors.neutral500 }}>
              {filtered.length} de {devices.length} dispositivo{devices.length !== 1 ? "s" : ""}
            </div>
          )}
        </Card>
      )}

      <DeviceFormModal
        open={formModal.open}
        onClose={() => setFormModal({ open: false, device: null })}
        initial={formModal.device}
        onSaved={load}
      />
      <DeleteModal
        open={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, device: null })}
        device={deleteModal.device}
        onDeleted={load}
      />
    </div>
  );
}
