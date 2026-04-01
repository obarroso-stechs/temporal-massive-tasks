import { useState, useEffect, useCallback } from "react";
import { DS } from "../../shared/design/tokens";
import {
  Alert, Badge, Button, Card, Modal, Select, Table, TextField, EmptyState,
} from "../../shared/ui/primitives";
import { groupsApi } from "../../api/groups";
import { devicesApi } from "../../api/devices";

function GroupFormModal({ open, onClose, initial, allDevices, onSaved }) {
  const isEdit = !!initial;
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [deviceIds, setDeviceIds] = useState([]);
  const [addingId, setAddingId] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open) {
      setName(initial?.name ?? "");
      setDescription(initial?.description ?? "");
      setDeviceIds([]);
      setAddingId("");
      setError(null);
    }
  }, [open, initial]);

  const selectedIds = new Set(deviceIds);
  const availableDevices = allDevices.filter((d) => !selectedIds.has(d.id));

  const handleSave = async () => {
    if (!name.trim()) return setError("El nombre es obligatorio.");
    setSaving(true);
    setError(null);
    try {
      const payload = {
        name: name.trim(),
        description: description || null,
        ...(isEdit ? {} : { device_ids: deviceIds.length ? deviceIds : undefined }),
      };
      if (isEdit) {
        await groupsApi.update(initial.id, payload);
      } else {
        await groupsApi.create(payload);
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
    <Modal open={open} onClose={onClose} title={isEdit ? `Editar grupo · ${initial?.name}` : "Nuevo grupo"} width="440px">
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        <TextField label="Nombre del grupo" value={name} onChange={setName} placeholder="Grupo Norte" required />
        <TextField label="Descripción" value={description} onChange={setDescription} placeholder="Dispositivos zona norte" />

        {!isEdit && (
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <div style={{ display: "flex", gap: "10px", alignItems: "flex-end" }}>
              <div style={{ flex: 1 }}>
                <Select
                  label="Dispositivos iniciales"
                  value={addingId}
                  onChange={setAddingId}
                  placeholder="Seleccioná un dispositivo..."
                  options={availableDevices.map((d) => ({
                    value: String(d.id),
                    label: `${d.serial_number}${d.model ? ` · ${d.model}` : ""}`,
                  }))}
                />
              </div>
              <Button
                variant="secondary"
                icon="plus"
                onClick={() => {
                  if (!addingId) return;
                  const id = Number(addingId);
                  if (!deviceIds.includes(id)) setDeviceIds((prev) => [...prev, id]);
                  setAddingId("");
                }}
                disabled={!addingId}
              >
                Agregar
              </Button>
            </div>

            {deviceIds.length > 0 && (
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {deviceIds.map((id) => {
                  const device = allDevices.find((d) => d.id === id);
                  return (
                    <Badge key={id} variant="primary" size="sm">
                      <span style={{ marginRight: "6px" }}>{device?.serial_number ?? `ID ${id}`}</span>
                      <button
                        onClick={() => setDeviceIds((prev) => prev.filter((x) => x !== id))}
                        style={{
                          background: "transparent",
                          border: "none",
                          color: "inherit",
                          cursor: "pointer",
                          padding: 0,
                          lineHeight: 1,
                        }}
                        aria-label={`Quitar dispositivo ${device?.serial_number ?? id}`}
                        title="Quitar"
                      >
                        ×
                      </button>
                    </Badge>
                  );
                })}
              </div>
            )}
          </div>
        )}

        <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", paddingTop: "8px" }}>
          <Button variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button variant="success" onClick={handleSave} loading={saving}>
            {isEdit ? "Guardar cambios" : "Crear grupo"}
          </Button>
        </div>
      </div>
    </Modal>
  );
}

function DeleteGroupModal({ open, onClose, group, onDeleted }) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState(null);

  const handleDelete = async () => {
    setDeleting(true);
    setError(null);
    try {
      await groupsApi.delete(group.id);
      onDeleted();
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Eliminar grupo" width="440px">
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
      <p style={{ margin: "0 0 20px", fontSize: "14px", color: DS.colors.neutral700 }}>
        ¿Eliminar el grupo <strong>{group?.name}</strong>? Esta acción no se puede deshacer.
      </p>
      <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px" }}>
        <Button variant="secondary" onClick={onClose}>Cancelar</Button>
        <Button variant="danger" onClick={handleDelete} loading={deleting}>Eliminar</Button>
      </div>
    </Modal>
  );
}

function GroupDetailModal({ open, onClose, group, allDevices, onUpdated }) {
  const [addingId, setAddingId] = useState("");
  const [removingId, setRemovingId] = useState(null);
  const [assigning, setAssigning] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open) { setAddingId(""); setError(null); }
  }, [open]);

  if (!group) return null;

  const assignedIds = new Set(group.devices.map((d) => d.id));
  const available = allDevices.filter((d) => !assignedIds.has(d.id));

  const handleAdd = async () => {
    if (!addingId) return;
    setAssigning(true);
    setError(null);
    try {
      await groupsApi.assignDevices(group.id, [Number(addingId)]);
      setAddingId("");
      onUpdated();
    } catch (e) {
      setError(e.message);
    } finally {
      setAssigning(false);
    }
  };

  const handleRemove = async (deviceId) => {
    setRemovingId(deviceId);
    setError(null);
    try {
      await groupsApi.removeDevice(group.id, deviceId);
      onUpdated();
    } catch (e) {
      setError(e.message);
    } finally {
      setRemovingId(null);
    }
  };

  const deviceColumns = [
    {
      key: "serial_number",
      label: "Serial",
      render: (v) => <span style={{ fontFamily: DS.monoFont, fontSize: "13px" }}>{v}</span>,
    },
    { key: "model", label: "Modelo", render: (v) => v || <span style={{ color: DS.colors.neutral400 }}>—</span> },
    { key: "manufacturer", label: "Fabricante", render: (v) => v || <span style={{ color: DS.colors.neutral400 }}>—</span> },
    {
      key: "_remove",
      label: "",
      render: (_, row) => (
        <Button
          variant="ghost"
          size="sm"
          icon="trash"
          style={{ color: DS.colors.error }}
          loading={removingId === row.id}
          onClick={() => handleRemove(row.id)}
        >
          Quitar
        </Button>
      ),
    },
  ];

  return (
    <Modal open={open} onClose={onClose} title={group.name} width="720px">
      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      {group.description && (
        <p style={{ margin: "0 0 20px", fontSize: "13px", color: DS.colors.neutral600 }}>
          {group.description}
        </p>
      )}

      {/* Add device */}
      {available.length > 0 && (
        <div
          style={{
            display: "flex",
            gap: "10px",
            alignItems: "flex-end",
            marginBottom: "20px",
            padding: "14px 16px",
            backgroundColor: DS.colors.neutral50,
            borderRadius: DS.radius.md,
            border: `1px solid ${DS.colors.border}`,
          }}
        >
          <div style={{ flex: 1 }}>
            <Select
              label="Agregar dispositivo"
              value={addingId}
              onChange={setAddingId}
              placeholder="Seleccioná un dispositivo..."
              options={available.map((d) => ({
                value: String(d.id),
                label: `${d.serial_number}${d.model ? ` · ${d.model}` : ""}`,
              }))}
            />
          </div>
          <Button variant="success" onClick={handleAdd} loading={assigning} disabled={!addingId} icon="plus">
            Agregar
          </Button>
        </div>
      )}

      {/* Device list */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
          <h4 style={{ margin: 0, fontSize: "14px", fontWeight: 600 }}>Dispositivos</h4>
          <Badge variant="primary">{group.devices.length}</Badge>
        </div>
        {group.devices.length === 0 ? (
          <div
            style={{
              padding: "32px",
              textAlign: "center",
              color: DS.colors.neutral500,
              fontSize: "13px",
              backgroundColor: DS.colors.neutral50,
              borderRadius: DS.radius.md,
              border: `1px dashed ${DS.colors.border}`,
            }}
          >
            Este grupo no tiene dispositivos asignados aún.
          </div>
        ) : (
          <Table columns={deviceColumns} data={group.devices} emptyMessage="Sin dispositivos" />
        )}
      </div>
    </Modal>
  );
}

export default function GroupsSection() {
  const [groups, setGroups] = useState([]);
  const [allDevices, setAllDevices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formModal, setFormModal] = useState({ open: false, group: null });
  const [deleteModal, setDeleteModal] = useState({ open: false, group: null });
  const [detailModal, setDetailModal] = useState({ open: false, group: null });

  const loadGroups = useCallback(() => {
    setLoading(true);
    setError(null);
    groupsApi.list().then(setGroups).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadGroups();
    devicesApi.list().then(setAllDevices).catch(() => {});
  }, [loadGroups]);

  const openDetail = (group) => setDetailModal({ open: true, group });

  const refreshDetail = () => {
    loadGroups();
    // Also refresh the group in the detail modal
    groupsApi.list().then((gs) => {
      setGroups(gs);
      setDetailModal((prev) => {
        if (!prev.group) return prev;
        const updated = gs.find((g) => g.id === prev.group.id);
        return updated ? { ...prev, group: updated } : prev;
      });
    });
  };

  return (
    <div>
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ margin: "0 0 4px", fontSize: "22px", fontWeight: 700, color: DS.colors.neutral900 }}>
          Grupos de Dispositivos
        </h2>
        <p style={{ margin: 0, fontSize: "14px", color: DS.colors.neutral600 }}>
          Organizá dispositivos en grupos para facilitar actualizaciones masivas.
        </p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      <div style={{ display: "flex", justifyContent: "flex-end", gap: "8px", marginBottom: "20px" }}>
        <Button variant="secondary" onClick={loadGroups} size="sm">Recargar</Button>
        <Button variant="success" icon="plus" onClick={() => setFormModal({ open: true, group: null })}>
          Nuevo grupo
        </Button>
      </div>

      {!loading && groups.length === 0 ? (
        <Card>
          <EmptyState
            icon="🗂️"
            title="No hay grupos creados"
            description="Creá un grupo para organizar tus dispositivos y lanzar actualizaciones en conjunto."
          />
        </Card>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "16px" }}>
          {loading
            ? Array.from({ length: 3 }).map((_, i) => (
                <div
                  key={i}
                  style={{
                    height: "140px",
                    borderRadius: DS.radius.lg,
                    backgroundColor: DS.colors.neutral100,
                    animation: "pulse 1.5s ease-in-out infinite",
                  }}
                />
              ))
            : groups.map((group) => (
                <Card
                  key={group.id}
                  style={{ cursor: "pointer", transition: "box-shadow 0.15s" }}
                  padding="20px"
                >
                  <div
                    onClick={() => openDetail(group)}
                    onMouseEnter={(e) => (e.currentTarget.parentElement.style.boxShadow = DS.shadow.md)}
                    onMouseLeave={(e) => (e.currentTarget.parentElement.style.boxShadow = DS.shadow.sm)}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
                      <h3 style={{ margin: 0, fontSize: "16px", fontWeight: 600, color: DS.colors.neutral900 }}>
                        {group.name}
                      </h3>
                      <Badge variant="primary">{group.devices.length} disp.</Badge>
                    </div>
                    {group.description && (
                      <p style={{ margin: "0 0 12px", fontSize: "13px", color: DS.colors.neutral600 }}>
                        {group.description}
                      </p>
                    )}
                    {group.devices.length > 0 ? (
                      <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "12px" }}>
                        {group.devices.slice(0, 4).map((d) => (
                          <span
                            key={d.id}
                            style={{
                              fontSize: "11px",
                              fontFamily: DS.monoFont,
                              backgroundColor: DS.colors.neutral100,
                              padding: "2px 8px",
                              borderRadius: DS.radius.sm,
                              color: DS.colors.neutral700,
                            }}
                          >
                            {d.serial_number}
                          </span>
                        ))}
                        {group.devices.length > 4 && (
                          <span style={{ fontSize: "11px", color: DS.colors.neutral500 }}>
                            +{group.devices.length - 4} más
                          </span>
                        )}
                      </div>
                    ) : (
                      <p style={{ margin: "0 0 12px", fontSize: "12px", color: DS.colors.neutral400, fontStyle: "italic" }}>
                        Sin dispositivos asignados
                      </p>
                    )}
                  </div>
                  <div
                    style={{
                      display: "flex",
                      gap: "6px",
                      paddingTop: "12px",
                      borderTop: `1px solid ${DS.colors.neutral100}`,
                    }}
                  >
                    <Button variant="ghost" size="sm" icon="eye" onClick={() => openDetail(group)}>
                      Ver
                    </Button>
                    <Button variant="ghost" size="sm" icon="edit" onClick={() => setFormModal({ open: true, group })}>
                      Editar
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      icon="trash"
                      style={{ color: DS.colors.error, marginLeft: "auto" }}
                      onClick={() => setDeleteModal({ open: true, group })}
                    >
                      Eliminar
                    </Button>
                  </div>
                </Card>
              ))}
        </div>
      )}

      <GroupFormModal
        open={formModal.open}
        onClose={() => setFormModal({ open: false, group: null })}
        initial={formModal.group}
        allDevices={allDevices}
        onSaved={loadGroups}
      />
      <DeleteGroupModal
        open={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, group: null })}
        group={deleteModal.group}
        onDeleted={loadGroups}
      />
      <GroupDetailModal
        open={detailModal.open}
        onClose={() => setDetailModal({ open: false, group: null })}
        group={detailModal.group}
        allDevices={allDevices}
        onUpdated={refreshDetail}
      />
    </div>
  );
}
