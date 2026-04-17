import { DS } from "../design/tokens";
import { NAV } from "../config/navigation";
import { Icon } from "../ui/Icon";

export const Sidebar = ({ section, setSection, sidebarOpen, setSidebarOpen }) => {
  const sidebarW = sidebarOpen ? 256 : 64;

  return (
    <div
      style={{
        width: sidebarW,
        flexShrink: 0,
        backgroundColor: DS.colors.white,
        borderRight: `1px solid ${DS.colors.border}`,
        display: "flex",
        flexDirection: "column",
        transition: "width 0.25s ease",
        position: "fixed",
        top: 0,
        left: 0,
        bottom: 0,
        zIndex: 100,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "0 16px",
          height: "64px",
          display: "flex",
          alignItems: "center",
          borderBottom: `1px solid ${DS.colors.border}`,
          gap: "12px",
        }}
      >
        <button
          onClick={() => setSidebarOpen((prev) => !prev)}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            color: DS.colors.neutral700,
            display: "flex",
            padding: "8px",
            borderRadius: DS.radius.md,
            flexShrink: 0,
          }}
        >
          <Icon name="menu" size={20} />
        </button>
        {sidebarOpen && (
          <div style={{ overflow: "hidden", whiteSpace: "nowrap" }}>
            <div style={{ fontSize: "16px", fontWeight: 700, color: DS.colors.neutral900, letterSpacing: "-0.01em" }}>Stechs</div>
            <div style={{ fontSize: "11px", color: DS.colors.neutral600, fontWeight: 500 }}>Device Manager</div>
          </div>
        )}
      </div>

      <nav style={{ padding: "12px 8px", flex: 1 }}>
        {NAV.map((item) => {
          const active = section === item.key;
          return (
            <button
              key={item.key}
              onClick={() => setSection(item.key)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                padding: "10px 12px",
                marginBottom: "2px",
                borderRadius: DS.radius.md,
                border: "none",
                cursor: "pointer",
                backgroundColor: active ? DS.colors.primaryLight : "transparent",
                color: active ? DS.colors.primary : DS.colors.neutral700,
                fontFamily: DS.font,
                fontSize: "14px",
                fontWeight: active ? 600 : 400,
                transition: "all 0.15s",
                textAlign: "left",
                whiteSpace: "nowrap",
              }}
              onMouseEnter={(e) => {
                if (!active) {
                  e.currentTarget.style.backgroundColor = DS.colors.neutral100;
                }
              }}
              onMouseLeave={(e) => {
                if (!active) {
                  e.currentTarget.style.backgroundColor = "transparent";
                }
              }}
            >
              <span style={{ flexShrink: 0 }}>
                <Icon name={item.icon} size={20} color={active ? DS.colors.primary : DS.colors.neutral600} />
              </span>
              {sidebarOpen && item.label}
            </button>
          );
        })}
      </nav>

      {sidebarOpen && (
        <div
          style={{
            padding: "16px",
            borderTop: `1px solid ${DS.colors.border}`,
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <div
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              backgroundColor: DS.colors.primary,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: DS.colors.white,
              fontWeight: 700,
              fontSize: "13px",
              flexShrink: 0,
            }}
          >
            A
          </div>
          <div style={{ overflow: "hidden" }}>
            <div style={{ fontSize: "13px", fontWeight: 600, color: DS.colors.neutral900, whiteSpace: "nowrap" }}>Admin</div>
            <div style={{ fontSize: "11px", color: DS.colors.neutral600 }}>admin@stechs.io</div>
          </div>
        </div>
      )}
    </div>
  );
};
