import { useState } from "react";
import { DS } from "../design/tokens";
import { Icon } from "./Icon";

export const Badge = ({ children, variant = "default", size = "md" }) => {
  const variants = {
    default: { bg: DS.colors.neutral200, color: DS.colors.neutral800 },
    primary: { bg: DS.colors.primaryLight, color: DS.colors.primaryDark },
    success: { bg: DS.colors.successLight, color: DS.colors.success },
    warning: { bg: DS.colors.warningLight, color: DS.colors.warning },
    error: { bg: DS.colors.errorLight, color: DS.colors.error },
    info: { bg: DS.colors.infoLight, color: DS.colors.info },
  };
  const v = variants[variant] || variants.default;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: size === "sm" ? "2px 8px" : "4px 10px",
        borderRadius: DS.radius.full,
        fontSize: size === "sm" ? "11px" : "12px",
        fontWeight: 600,
        letterSpacing: "0.02em",
        backgroundColor: v.bg,
        color: v.color,
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </span>
  );
};

export const Button = ({
  children,
  variant = "primary",
  size = "md",
  onClick,
  disabled,
  loading,
  icon,
  fullWidth,
  style: extStyle,
}) => {
  const [hovered, setHovered] = useState(false);
  const variants = {
    primary: {
      backgroundColor: hovered ? DS.colors.primaryDark : DS.colors.primary,
      color: DS.colors.white,
      border: "none",
      boxShadow: DS.shadow.sm,
    },
    secondary: {
      backgroundColor: hovered ? DS.colors.neutral100 : DS.colors.white,
      color: DS.colors.neutral800,
      border: `1px solid ${DS.colors.border}`,
    },
    ghost: {
      backgroundColor: hovered ? DS.colors.neutral100 : "transparent",
      color: DS.colors.neutral700,
      border: "none",
    },
    danger: {
      backgroundColor: hovered ? "#B71C1C" : DS.colors.error,
      color: DS.colors.white,
      border: "none",
    },
    success: {
      backgroundColor: hovered ? "#155724" : DS.colors.success,
      color: DS.colors.white,
      border: "none",
    },
  };
  const v = variants[variant] || variants.primary;
  const sizes = {
    sm: { padding: "6px 12px", fontSize: "13px" },
    md: { padding: "10px 20px", fontSize: "14px" },
    lg: { padding: "12px 24px", fontSize: "15px" },
  };
  const s = sizes[size] || sizes.md;
  const isDisabled = disabled || loading;

  return (
    <button
      onClick={onClick}
      disabled={isDisabled}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        cursor: isDisabled ? "not-allowed" : "pointer",
        opacity: isDisabled ? 0.6 : 1,
        borderRadius: DS.radius.md,
        fontFamily: DS.font,
        fontWeight: 500,
        transition: "all 0.15s ease",
        width: fullWidth ? "100%" : undefined,
        ...v,
        ...s,
        ...(extStyle || {}),
      }}
    >
      {loading ? <Spinner size={16} color="currentColor" /> : icon && <Icon name={icon} size={16} color="currentColor" />}
      {children}
    </button>
  );
};

export const TextField = ({
  label,
  placeholder,
  value,
  onChange,
  type = "text",
  helper,
  error,
  required,
  disabled,
}) => (
  <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
    {label && (
      <label style={{ fontSize: "13px", fontWeight: 500, color: DS.colors.neutral800 }}>
        {label}
        {required && <span style={{ color: DS.colors.error }}> *</span>}
      </label>
    )}
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      disabled={disabled}
      style={{
        padding: "10px 14px",
        borderRadius: DS.radius.md,
        fontFamily: DS.font,
        fontSize: "14px",
        color: DS.colors.neutral900,
        border: `1px solid ${error ? DS.colors.error : DS.colors.border}`,
        outline: "none",
        backgroundColor: disabled ? DS.colors.neutral100 : DS.colors.white,
        transition: "border 0.15s",
      }}
      onFocus={(e) => {
        if (!disabled) e.target.style.borderColor = DS.colors.primary;
      }}
      onBlur={(e) => {
        e.target.style.borderColor = error ? DS.colors.error : DS.colors.border;
      }}
    />
    {(helper || error) && (
      <span style={{ fontSize: "12px", color: error ? DS.colors.error : DS.colors.neutral600 }}>
        {error || helper}
      </span>
    )}
  </div>
);

export const Textarea = ({ label, placeholder, value, onChange, rows = 5, helper, error, required, disabled }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
    {label && (
      <label style={{ fontSize: "13px", fontWeight: 500, color: DS.colors.neutral800 }}>
        {label}
        {required && <span style={{ color: DS.colors.error }}> *</span>}
      </label>
    )}
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={rows}
      disabled={disabled}
      style={{
        padding: "10px 14px",
        borderRadius: DS.radius.md,
        fontFamily: DS.monoFont,
        fontSize: "13px",
        color: DS.colors.neutral900,
        border: `1px solid ${error ? DS.colors.error : DS.colors.border}`,
        outline: "none",
        backgroundColor: disabled ? DS.colors.neutral100 : DS.colors.white,
        resize: "vertical",
        transition: "border 0.15s",
      }}
      onFocus={(e) => { if (!disabled) e.target.style.borderColor = DS.colors.primary; }}
      onBlur={(e) => { e.target.style.borderColor = error ? DS.colors.error : DS.colors.border; }}
    />
    {(helper || error) && (
      <span style={{ fontSize: "12px", color: error ? DS.colors.error : DS.colors.neutral600 }}>
        {error || helper}
      </span>
    )}
  </div>
);

export const Select = ({ label, value, onChange, options, placeholder, required, disabled }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
    {label && (
      <label style={{ fontSize: "13px", fontWeight: 500, color: DS.colors.neutral800 }}>
        {label}
        {required && <span style={{ color: DS.colors.error }}> *</span>}
      </label>
    )}
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
      style={{
        padding: "10px 14px",
        borderRadius: DS.radius.md,
        fontFamily: DS.font,
        fontSize: "14px",
        color: value ? DS.colors.neutral900 : DS.colors.neutral600,
        border: `1px solid ${DS.colors.border}`,
        backgroundColor: disabled ? DS.colors.neutral100 : DS.colors.white,
        outline: "none",
        cursor: disabled ? "not-allowed" : "pointer",
        appearance: "auto",
      }}
    >
      {placeholder && <option value="">{placeholder}</option>}
      {options.map((o) => (
        <option key={o.value} value={o.value}>
          {o.label}
        </option>
      ))}
    </select>
  </div>
);

export const Card = ({ children, style: extStyle, padding = "24px" }) => (
  <div
    style={{
      backgroundColor: DS.colors.surface,
      borderRadius: DS.radius.lg,
      border: `1px solid ${DS.colors.border}`,
      boxShadow: DS.shadow.sm,
      padding,
      ...extStyle,
    }}
  >
    {children}
  </div>
);

export const Modal = ({ open, onClose, title, children, width = "560px" }) => {
  if (!open) return null;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0,0,0,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        padding: "20px",
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        style={{
          backgroundColor: DS.colors.white,
          borderRadius: DS.radius.xl,
          boxShadow: DS.shadow.xl,
          width: "100%",
          maxWidth: width,
          maxHeight: "90vh",
          display: "flex",
          flexDirection: "column",
          animation: "slideUp 0.2s ease",
        }}
      >
        <div
          style={{
            padding: "20px 24px",
            borderBottom: `1px solid ${DS.colors.border}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexShrink: 0,
          }}
        >
          <h3 style={{ margin: 0, fontSize: "18px", fontWeight: 600, color: DS.colors.neutral900 }}>
            {title}
          </h3>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              color: DS.colors.neutral600,
              display: "flex",
              padding: "4px",
              borderRadius: DS.radius.sm,
            }}
          >
            <Icon name="x" size={20} />
          </button>
        </div>
        <div style={{ padding: "24px", overflowY: "auto", flex: 1 }}>{children}</div>
      </div>
    </div>
  );
};

export const Table = ({
  columns,
  data,
  emptyMessage = "No hay datos disponibles",
  onRowClick,
  loading,
}) => {
  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", padding: "48px" }}>
        <Spinner size={32} />
      </div>
    );
  }

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
        <thead>
          <tr style={{ backgroundColor: DS.colors.neutral50 }}>
            {columns.map((col) => (
              <th
                key={col.key}
                style={{
                  padding: "12px 16px",
                  textAlign: "left",
                  fontWeight: 600,
                  color: DS.colors.neutral700,
                  fontSize: "12px",
                  letterSpacing: "0.05em",
                  textTransform: "uppercase",
                  borderBottom: `1px solid ${DS.colors.border}`,
                  whiteSpace: "nowrap",
                }}
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length}
                style={{ padding: "48px", textAlign: "center", color: DS.colors.neutral500 }}
              >
                <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px" }}>
                  <span style={{ fontSize: "32px" }}>📭</span>
                  <span style={{ fontSize: "14px" }}>{emptyMessage}</span>
                </div>
              </td>
            </tr>
          ) : (
            data.map((row, i) => (
              <tr
                key={row.id ?? i}
                onClick={onRowClick ? () => onRowClick(row) : undefined}
                style={{
                  borderBottom: `1px solid ${DS.colors.neutral100}`,
                  transition: "background 0.1s",
                  cursor: onRowClick ? "pointer" : "default",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = DS.colors.neutral50;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = "transparent";
                }}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    style={{ padding: "14px 16px", color: DS.colors.neutral800, verticalAlign: "middle" }}
                  >
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export const Alert = ({ type = "info", message, onClose }) => {
  const types = {
    info: { bg: DS.colors.infoLight, color: DS.colors.info, icon: "info" },
    success: { bg: DS.colors.successLight, color: DS.colors.success, icon: "check" },
    warning: { bg: DS.colors.warningLight, color: DS.colors.warning, icon: "info" },
    error: { bg: DS.colors.errorLight, color: DS.colors.error, icon: "x" },
  };
  const t = types[type];

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "12px",
        padding: "14px 16px",
        borderRadius: DS.radius.md,
        backgroundColor: t.bg,
        color: t.color,
        marginBottom: "16px",
      }}
    >
      <Icon name={t.icon} size={18} color={t.color} />
      <span style={{ flex: 1, fontSize: "14px", fontWeight: 500 }}>{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          style={{ background: "none", border: "none", cursor: "pointer", color: t.color, display: "flex" }}
        >
          <Icon name="x" size={16} />
        </button>
      )}
    </div>
  );
};

export const Tabs = ({ tabs, active, onChange }) => (
  <div
    style={{
      display: "flex",
      borderBottom: `1px solid ${DS.colors.border}`,
      gap: "4px",
      marginBottom: "24px",
    }}
  >
    {tabs.map((tab) => (
      <button
        key={tab.key}
        onClick={() => onChange(tab.key)}
        style={{
          padding: "10px 16px",
          background: "none",
          border: "none",
          cursor: "pointer",
          fontFamily: DS.font,
          fontSize: "14px",
          fontWeight: active === tab.key ? 600 : 400,
          color: active === tab.key ? DS.colors.primary : DS.colors.neutral700,
          borderBottom: active === tab.key ? `2px solid ${DS.colors.primary}` : "2px solid transparent",
          marginBottom: "-1px",
          transition: "all 0.15s",
        }}
      >
        {tab.label}
      </button>
    ))}
  </div>
);

const STATUS_CONFIG = {
  COMPLETED: { label: "Completado", variant: "success", color: "#1E8E3E" },
  RUNNING:   { label: "En curso",   variant: "primary", color: "#1A73E8" },
  PENDING:   { label: "Pendiente",  variant: "default", color: "#9AA0A6" },
  SCHEDULED: { label: "Programado", variant: "warning", color: "#F29900" },
  FAILED:    { label: "Fallido",    variant: "error",   color: "#D93025" },
  CANCELED:  { label: "Cancelado",  variant: "info",    color: "#5F6368" },
  TIMED_OUT: { label: "Tiempo ag.", variant: "warning", color: "#E37400" },
  SUCCESS:   { label: "Exitoso",    variant: "success", color: "#1E8E3E" },
  ERROR:     { label: "Error",      variant: "error",   color: "#D93025" },
};

export const StatusBadge = ({ status }) => {
  const m = STATUS_CONFIG[status] || { label: status ?? "—", variant: "default" };
  return <Badge variant={m.variant}>{m.label}</Badge>;
};

/** Stacked horizontal bar showing device status distribution */
export const StatusBar = ({ devices = [], total }) => {
  const count = total ?? devices.length;
  if (count === 0) return <span style={{ fontSize: "13px", color: DS.colors.neutral500 }}>Sin dispositivos</span>;

  const counts = {};
  devices.forEach((d) => {
    const s = d.status ?? d;
    counts[s] = (counts[s] ?? 0) + 1;
  });

  const order = ["COMPLETED", "RUNNING", "PENDING", "SCHEDULED", "FAILED", "CANCELED", "TIMED_OUT"];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "6px", minWidth: "160px" }}>
      <div
        style={{
          display: "flex",
          height: "8px",
          borderRadius: "4px",
          overflow: "hidden",
          backgroundColor: DS.colors.neutral200,
        }}
      >
        {order.map((s) => {
          const n = counts[s] ?? 0;
          if (!n) return null;
          const pct = (n / count) * 100;
          const cfg = STATUS_CONFIG[s] || { color: "#9AA0A6" };
          return (
            <div
              key={s}
              title={`${cfg.label ?? s}: ${n} (${Math.round(pct)}%)`}
              style={{ width: `${pct}%`, backgroundColor: cfg.color, transition: "width 0.3s" }}
            />
          );
        })}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
        {order.map((s) => {
          const n = counts[s] ?? 0;
          if (!n) return null;
          const pct = Math.round((n / count) * 100);
          const cfg = STATUS_CONFIG[s] || { color: "#9AA0A6", label: s };
          return (
            <span
              key={s}
              style={{
                fontSize: "11px",
                color: cfg.color,
                fontWeight: 600,
                display: "flex",
                alignItems: "center",
                gap: "3px",
              }}
            >
              <span
                style={{
                  width: "7px",
                  height: "7px",
                  borderRadius: "50%",
                  backgroundColor: cfg.color,
                  display: "inline-block",
                  flexShrink: 0,
                }}
              />
              {cfg.label}: {n} ({pct}%)
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const Spinner = ({ size = 24, color = DS.colors.primary }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    style={{ animation: "spin 0.8s linear infinite" }}
  >
    <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2.5" strokeOpacity="0.2" />
    <path
      d="M12 2a10 10 0 0 1 10 10"
      stroke={color}
      strokeWidth="2.5"
      strokeLinecap="round"
    />
  </svg>
);

export const EmptyState = ({ icon = "📭", title, description }) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "64px 32px",
      gap: "12px",
      color: DS.colors.neutral500,
    }}
  >
    <span style={{ fontSize: "48px" }}>{icon}</span>
    <p style={{ margin: 0, fontSize: "16px", fontWeight: 600, color: DS.colors.neutral700 }}>{title}</p>
    {description && <p style={{ margin: 0, fontSize: "14px", textAlign: "center", maxWidth: "360px" }}>{description}</p>}
  </div>
);
