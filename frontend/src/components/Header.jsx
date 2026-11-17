import React from "react";
import { Shield, AlertTriangle, Terminal, Lock, Activity, LayoutDashboard } from "lucide-react";

export default function Header({ activeTab, setActiveTab }) {
  const tabs = [
    { id: "workbench", label: "Incident Workbench (Overview)", icon: LayoutDashboard },
    { id: "timeline", label: "Incident Timeline", icon: Activity },
    { id: "simulator", label: "Zero-Trust Simulator", icon: Shield },
    { id: "detections", label: "Detection Engine (DET 1-10)", icon: AlertTriangle },
    { id: "epistemic", label: "Epistemic Truth Matrix", icon: Terminal },
    { id: "evidence", label: "Evidence & Hashes", icon: Lock },
  ];

  return (
    <header className="border-b border-slate-800 bg-[#090d16]/90 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Classification */}
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
              <Shield className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono font-bold text-lg text-white tracking-wider">
                  NORTHSTAR<span className="text-cyan-400">_SENTINEL</span>
                </span>
                <span className="text-[10px] font-mono font-semibold uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                  DEFENSE TRACK
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono">
                CASE NS-26-014 | Chennai Learning Center Incident
              </p>
            </div>
          </div>

          {/* Incident Status Pill */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="flex items-center space-x-2 bg-slate-900/80 px-3 py-1.5 rounded-full border border-slate-800 text-xs font-mono">
              <span className="h-2 w-2 rounded-full bg-rose-500 animate-ping"></span>
              <span className="text-slate-300">INCIDENT OCCURRED:</span>
              <span className="text-rose-400 font-semibold">12-OCT-2026 03:15 IST</span>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 border-t border-slate-800/60 overflow-x-auto py-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-medium font-mono transition-all whitespace-nowrap ${
                  isActive
                    ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? "text-cyan-400" : "text-slate-500"}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
