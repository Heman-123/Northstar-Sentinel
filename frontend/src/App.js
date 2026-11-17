import React, { useState } from "react";
import Header from "./components/Header";
import IncidentWorkbench from "./components/IncidentWorkbench";
import MetricsOverview from "./components/MetricsOverview";
import IncidentTimeline from "./components/IncidentTimeline";
import LiveDefenseSimulator from "./components/LiveDefenseSimulator";
import DetectionMatrix from "./components/DetectionMatrix";
import EpistemicMatrix from "./components/EpistemicMatrix";
import EvidenceChainOfCustody from "./components/EvidenceChainOfCustody";
import { ShieldCheck, GitBranch } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("workbench");

  return (
    <div className="min-h-screen bg-[#070b12] text-slate-100 flex flex-col font-sans">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-[1750px] w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab !== "workbench" && <MetricsOverview />}

        {activeTab === "workbench" && <IncidentWorkbench onSwitchTab={setActiveTab} />}
        {activeTab === "timeline" && <IncidentTimeline />}
        {activeTab === "simulator" && <LiveDefenseSimulator />}
        {activeTab === "detections" && <DetectionMatrix />}
        {activeTab === "epistemic" && <EpistemicMatrix />}
        {activeTab === "evidence" && <EvidenceChainOfCustody />}
      </main>

      <footer className="border-t border-slate-800/80 bg-[#090d16] py-4 text-xs font-mono text-slate-500">
        <div className="max-w-[1750px] mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="h-4 w-4 text-cyan-400" />
            <span>Northstar Sentinel — Case File NS-26-014 Investigation</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-slate-400">Track: DEFENSE</span>
            <span>•</span>
            <a
              href="https://github.com/Heman-123/Northstar-Sentinel.git"
              target="_blank"
              rel="noreferrer"
              className="text-cyan-400 hover:underline flex items-center space-x-1"
            >
              <GitBranch className="h-3.5 w-3.5" />
              <span>GitHub: Heman-123/Northstar-Sentinel</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
