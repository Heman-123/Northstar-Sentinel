import React, { useState } from "react";
import { Play, Shield, ShieldAlert, Cpu, Terminal, ArrowRight, RefreshCw, CheckCircle, XCircle } from "lucide-react";
import { SIMULATION_SCENARIOS } from "../data/incidentData";

export default function LiveDefenseSimulator() {
  const [selectedScenario, setSelectedScenario] = useState(SIMULATION_SCENARIOS[0]);
  const [securityMode, setSecurityMode] = useState("hardened"); // "vulnerable" or "hardened"
  const [executionLog, setExecutionLog] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const runSimulation = () => {
    setIsSimulating(true);
    setExecutionLog(null);

    setTimeout(() => {
      const isHardened = securityMode === "hardened";
      const outcome = isHardened ? selectedScenario.hardenedResult : selectedScenario.vulnerableResult;

      const log = {
        timestamp: new Date().toISOString(),
        scenarioName: selectedScenario.name,
        client: selectedScenario.client,
        sourceIp: selectedScenario.sourceIp,
        endpoint: selectedScenario.endpoint,
        mode: securityMode.toUpperCase(),
        statusCode: outcome.status,
        verdict: outcome.label,
        details: outcome.desc,
        isBlocked: outcome.status !== 200
      };

      setExecutionLog(log);
      setIsSimulating(false);
    }, 600);
  };

  return (
    <div className="bg-[#0d131f] border border-slate-800 rounded-xl p-5 mb-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 mb-6 gap-3">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center space-x-2 font-mono">
            <Shield className="h-5 w-5 text-cyan-400" />
            <span>LIVE DEFENSE SIMULATOR & POLICY ENFORCEMENT LAB</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Safely test threat scenarios against the Vulnerable Baseline vs. Northstar Sentinel's Zero-Trust Shield.
          </p>
        </div>

        {/* Security Mode Toggle */}
        <div className="flex items-center space-x-2 bg-slate-900 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setSecurityMode("vulnerable")}
            className={`px-3 py-1 text-xs font-mono font-bold rounded transition-all ${
              securityMode === "vulnerable"
                ? "bg-rose-500 text-white shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Vulnerable Baseline
          </button>
          <button
            onClick={() => setSecurityMode("hardened")}
            className={`px-3 py-1 text-xs font-mono font-bold rounded transition-all ${
              securityMode === "hardened"
                ? "bg-emerald-500 text-black shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Sentinel Shield (Hardened)
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Scenario Selector (Left Column) */}
        <div className="lg:col-span-5 space-y-3">
          <label className="text-xs font-mono text-slate-400 uppercase tracking-wide block">
            Select Simulation Scenario:
          </label>
          {SIMULATION_SCENARIOS.map((scen) => (
            <div
              key={scen.id}
              onClick={() => {
                setSelectedScenario(scen);
                setExecutionLog(null);
              }}
              className={`p-3 rounded-lg border cursor-pointer transition-all ${
                selectedScenario.id === scen.id
                  ? "bg-cyan-950/40 border-cyan-500/60 shadow-sm"
                  : "bg-slate-900/60 border-slate-800 hover:border-slate-700"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-mono text-xs font-bold text-white">
                  {scen.name}
                </span>
                <span className="font-mono text-[10px] text-cyan-400 bg-cyan-900/40 px-1.5 py-0.5 rounded">
                  {scen.endpoint}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans leading-relaxed">
                {scen.description}
              </p>
              <div className="mt-2 flex items-center space-x-3 text-[10px] font-mono text-slate-500">
                <span>Client: {scen.client}</span>
                <span>•</span>
                <span>Source IP: {scen.sourceIp}</span>
              </div>
            </div>
          ))}

          <button
            onClick={runSimulation}
            disabled={isSimulating}
            className="w-full mt-4 flex items-center justify-center space-x-2 py-2.5 px-4 bg-cyan-500 hover:bg-cyan-400 text-black font-mono font-bold text-xs rounded-lg transition-colors shadow-lg shadow-cyan-500/10 disabled:opacity-50"
          >
            {isSimulating ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                <span>EVALUATING PACKET...</span>
              </>
            ) : (
              <>
                <Play className="h-4 w-4 fill-current" />
                <span>DISPATCH SIMULATED PACKET</span>
              </>
            )}
          </button>
        </div>

        {/* Live Terminal & Response Inspector (Right Column) */}
        <div className="lg:col-span-7 bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 mb-3">
              <div className="flex items-center space-x-2">
                <Terminal className="h-4 w-4 text-cyan-400" />
                <span className="text-xs font-bold text-slate-300">
                  PACKET INSPECTION & PEP TELEMETRY
                </span>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                PORT 8765 / LOCAL MOCK
              </span>
            </div>

            {/* Packet Parameters */}
            <div className="bg-slate-900/70 p-3 rounded border border-slate-800/60 text-xs space-y-1 mb-4">
              <div className="text-slate-400">
                <span className="text-cyan-400">REQUEST: </span>
                <span className="text-white font-bold">{selectedScenario.endpoint}</span>
              </div>
              <div className="text-slate-400">
                <span className="text-cyan-400">CLIENT_ID: </span>
                <span className="text-white">{selectedScenario.client}</span>
              </div>
              <div className="text-slate-400">
                <span className="text-cyan-400">SOURCE_IP: </span>
                <span className={selectedScenario.sourceIp === "203.0.113.77" ? "text-rose-400 font-bold" : "text-emerald-400"}>
                  {selectedScenario.sourceIp}
                </span>
              </div>
              <div className="text-slate-400">
                <span className="text-cyan-400">ENFORCEMENT_ENGINE: </span>
                <span className={securityMode === "hardened" ? "text-emerald-400 font-bold" : "text-rose-400 font-bold"}>
                  {securityMode.toUpperCase()}
                </span>
              </div>
            </div>

            {/* Output Stream */}
            {executionLog ? (
              <div
                className={`p-4 rounded-lg border ${
                  executionLog.statusCode === 200
                    ? securityMode === "vulnerable" && selectedScenario.id !== "SCENARIO_LEGITIMATE"
                      ? "bg-rose-950/30 border-rose-500/40 text-rose-300"
                      : "bg-emerald-950/30 border-emerald-500/40 text-emerald-300"
                    : "bg-emerald-950/30 border-emerald-500/40 text-emerald-300"
                }`}
              >
                <div className="flex items-center space-x-2 text-sm font-bold mb-2">
                  {executionLog.statusCode === 200 ? (
                    securityMode === "vulnerable" && selectedScenario.id !== "SCENARIO_LEGITIMATE" ? (
                      <XCircle className="h-5 w-5 text-rose-400" />
                    ) : (
                      <CheckCircle className="h-5 w-5 text-emerald-400" />
                    )
                  ) : (
                    <Shield className="h-5 w-5 text-emerald-400" />
                  )}
                  <span>
                    HTTP {executionLog.statusCode} — {executionLog.verdict}
                  </span>
                </div>
                <p className="text-xs leading-relaxed opacity-90 font-sans">
                  {executionLog.details}
                </p>
                <div className="mt-3 pt-2 border-t border-current/20 text-[10px] opacity-75">
                  Evaluated at {executionLog.timestamp} | Zero-Trust PEP
                </div>
              </div>
            ) : (
              <div className="h-32 flex flex-col items-center justify-center text-slate-500 text-xs">
                <span>Select a scenario and click "Dispatch Simulated Packet" to execute.</span>
              </div>
            )}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] text-slate-500 flex justify-between">
            <span>Isolation: Strictly Local Mock (127.0.0.1)</span>
            <span>Zero Network Egress</span>
          </div>
        </div>
      </div>
    </div>
  );
}
