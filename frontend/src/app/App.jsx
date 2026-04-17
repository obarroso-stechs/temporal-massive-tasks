import { useState } from "react";
import DevicesSection from "../features/devices/DevicesSection";
import GroupsSection from "../features/groups/GroupsSection";
import ReportsSection from "../features/reports/ReportsSection";
import TaskExecutionSection from "../features/tasks/TaskExecutionSection";
import { DS } from "../shared/design/tokens";
import { Sidebar } from "../shared/layout/Sidebar";
import { Topbar } from "../shared/layout/Topbar";
import { GlobalStyles } from "../shared/styles/GlobalStyles";

export const App = () => {
  const [section, setSection] = useState("tasks");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const sidebarW = sidebarOpen ? 256 : 64;

  return (
    <div style={{ display: "flex", minHeight: "100vh", backgroundColor: DS.colors.surfaceVariant, fontFamily: DS.font }}>
      <GlobalStyles />

      <Sidebar section={section} setSection={setSection} sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      <div style={{ marginLeft: sidebarW, flex: 1, display: "flex", flexDirection: "column", transition: "margin-left 0.25s ease" }}>
        <Topbar section={section} />

        <main style={{ padding: "32px", maxWidth: "1280px", width: "100%" }}>
          {section === "tasks" && <TaskExecutionSection />}
          {section === "devices" && <DevicesSection />}
          {section === "groups" && <GroupsSection />}
          {section === "reports" && <ReportsSection />}
        </main>
      </div>
    </div>
  );
};
