import { DS } from "../design/tokens";
import { NAV } from "../config/navigation";
import { Icon } from "../ui/Icon";
import { Badge } from "../ui/primitives";

export const Topbar = ({ section }) => (
  <div
    style={{
      height: "64px",
      backgroundColor: DS.colors.white,
      borderBottom: `1px solid ${DS.colors.border}`,
      display: "flex",
      alignItems: "center",
      padding: "0 32px",
      justifyContent: "space-between",
      position: "sticky",
      top: 0,
      zIndex: 50,
      boxShadow: DS.shadow.sm,
    }}
  >
    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
      <span style={{ fontSize: "13px", color: DS.colors.neutral600 }}>Stechs</span>
      <Icon name="chevronRight" size={14} color={DS.colors.neutral400} />
      <span style={{ fontSize: "13px", fontWeight: 600, color: DS.colors.neutral900 }}>
        {NAV.find((item) => item.key === section)?.label}
      </span>
    </div>
    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
      <Badge variant="success">API Conectada</Badge>
    </div>
  </div>
);
