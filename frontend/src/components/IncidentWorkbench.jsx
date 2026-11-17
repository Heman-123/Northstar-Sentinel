import React, { useState, useEffect } from "react";
import {
  AlertTriangle,
  Target,
  Info,
  Zap,
  MessageSquare,
  Plus,
  Ban,
  KeyRound,
  HardDrive,
  Shield,
  Clock,
  ArrowRight,
  CheckCircle2
} from "lucide-react";
import { DETECTION_RULES, TIMELINE_EVENTS } from "../incidentData";

export default function IncidentWorkbench({ onSwitchTab }) {
  const [selectedFindingId, setSelectedFindingId] = useState("DET-001");
  const [notes, setNotes] = useState(() => {
    try {
      const saved = localStorage.getItem("ns_sentinel_notes");
      if (saved) return JSON.parse(saved);
    } catch (e) {}
    return [
      { author: "lead.dfir@northstar.edu.in", time: "03:30 AM", text: "Active Firewall Shun executed on IP 203.0.113.77 at Gateway Layer 0." },
      { author: "soc.analyst@northstar.edu.in", time: "03:35 AM", text: "Revoked JTI rc-prod-01 across IdP cluster. Token expiry set to 0ms." },
      { author: "lead.dfir@northstar.edu.in", time: "04:15 AM", text: "CampusVault export bucket quarantined. Direct external GET requests restricted." },
      { author: "dpo@northstar.edu.in", time: "06:00 AM", text: "DPDPA 2023 statutory notification draft formulated for Data Protection Board." }
    ];
  });
  const [newNote, setNewNote] = useState("");
  const [owner, setOwner] = useState("lead.dfir@northstar.edu.in");
  const [status, setStatus] = useState("Under Active Containment");
  const [disposition, setDisposition] = useState("True Positive - Service Token Replay");
  const [soarBanner, setSoarBanner] = useState("Ready: All Zero-Trust hooks live on PEP port 8765.");

  const selectedFinding = DETECTION_RULES.find((r) => r.id === selectedFindingId) || DETECTION_RULES[0];

  const handlePostNote = (e) => {
    e.preventDefault();
    if (!newNote.trim()) return;
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const updated = [{ author: owner, time: timeStr, text: newNote.trim() }, ...notes];
    setNotes(updated);
    setNewNote("");
    try {
      localStorage.setItem("ns_sentinel_notes", JSON.stringify(updated));
    } catch (e) {}
  };

  const executeAction = (action) => {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    let msg = "";
    if (action === "shun") {
      msg = "SOAR Playbook Triggered: Active Firewall Shun applied to IP 203.0.113.77.";
      setSoarBanner("ACTION EXECUTED: IP 203.0.113.77 blacklisted at Layer 0.");
    } else if (action === "revoke") {
      msg = "SOAR Playbook Triggered: JTI rc-prod-01 revoked in-memory across IdP.";
      setSoarBanner("ACTION EXECUTED: Token JTI rc-prod-01 revoked in 0ms.");
    } else if (action === "isolate") {
      msg = "SOAR Playbook Triggered: CampusVault export bucket locked to DLP mode.";
      setSoarBanner("ACTION EXECUTED: CampusVault export bucket locked to DLP.");
    }
    const updated = [{ author: "soar.sentinel@northstar.edu.in", time: timeStr, text: msg }, ...notes];
    setNotes(updated);
    try {
      localStorage.setItem("ns_sentinel_notes", JSON.stringify(updated));
    } catch (e) {}
  };

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        
        {/* =============================================================== */}
        {/* COLUMN 1: LEFT FINDINGS RAIL (SPLUNK ES INCLUDED FINDINGS)      */}
        {/* =============================================================== */}
        <div className="lg:col-span-3 bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl space-y-3 font-mono text-xs">
          <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-4 w-4 text-amber-400" />
              <h3 className="font-bold text-white uppercase text-xs">Included Findings</h3>
            </div>
            <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 font-bold text-[10px] border border-rose-500/30">
              10 Rules Fired
            </span>
          </div>

          <p className="text-[11px] text-slate-400 font-sans leading-normal">
            Select a finding to inspect evidentiary logs, highlight MITRE ATT&CK techniques, and verify defensive controls.
          </p>

          <div className="space-y-2 max-h-[700px] overflow-y-auto pr-1">
            {DETECTION_RULES.map((r) => {
              const isSelected = r.id === selectedFindingId;
              const isCrit = r.priority === "P1";
              return (
                <div
                  key={r.id}
                  onClick={() => setSelectedFindingId(r.id)}
                  className={`p-3 rounded-lg border transition-all cursor-pointer ${
                    isSelected
                      ? "border-cyan-400 bg-cyan-950/20 shadow-md shadow-cyan-500/10"
                      : isCrit
                      ? "border-rose-500/30 bg-[#11182c] hover:bg-slate-800/80"
                      : "border-amber-500/30 bg-[#11182c] hover:bg-slate-800/80"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-white">{r.id}</span>
                    <span
                      className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                        isCrit
                          ? "bg-rose-500/10 text-rose-400 border border-rose-500/30"
                          : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                      }`}
                    >
                      {r.priority} | {r.score}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-200 font-sans leading-snug line-clamp-2">
                    {r.title}
                  </div>
                  <div className="mt-1 flex items-center justify-between text-[10px] text-slate-500">
                    <span>{r.mitre}</span>
                    <span className="text-cyan-400">{r.evidence ? r.evidence[0] : ""}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* =============================================================== */}
        {/* COLUMN 2: CENTER CANVAS (MITRE MAP & FINDING DETAILS)           */}
        {/* =============================================================== */}
        <div className="lg:col-span-6 space-y-5">
          
          {/* Executive KPI Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 font-mono text-xs">
            <div className="bg-[#0d1322] p-3 rounded-xl border border-rose-500/30">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Compromised Learners</span>
              <div className="text-lg font-bold text-rose-400 mt-1">2,300 PII</div>
              <span className="text-[10px] text-slate-500 font-sans">100% Active Academy Records</span>
            </div>

            <div className="bg-[#0d1322] p-3 rounded-xl border border-amber-500/30">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Total Cloud Egress</span>
              <div className="text-lg font-bold text-amber-400 mt-1">972.4 KB</div>
              <span className="text-[10px] text-slate-500 font-sans">2x Downloads (CampusVault)</span>
            </div>

            <div className="bg-[#0d1322] p-3 rounded-xl border border-cyan-500/30">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Latency Degradation</span>
              <div className="text-lg font-bold text-cyan-400 mt-1">8,420 ms</div>
              <span className="text-[10px] text-slate-500 font-sans">~187x Surge Over 45ms</span>
            </div>

            <div className="bg-[#0d1322] p-3 rounded-xl border border-purple-500/30">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Adversary Source IP</span>
              <div className="text-sm font-bold text-purple-400 truncate mt-1">203.0.113.77</div>
              <span className="text-[10px] text-slate-500 font-sans">Key Replay Ingress</span>
            </div>

            <div className="bg-[#0d1322] p-3 rounded-xl border border-emerald-500/30">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Chain of Custody</span>
              <div className="text-lg font-bold text-emerald-400 mt-1">12 / 12 (100%)</div>
              <span className="text-[10px] text-slate-500 font-sans">SHA-256 Hashes Verified</span>
            </div>

            <div className="bg-[#0d1322] p-3 rounded-xl border border-emerald-500/30">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Adaptive Threat Ban</span>
              <div className="text-lg font-bold text-emerald-400 mt-1">ACTIVE</div>
              <span className="text-[10px] text-slate-500 font-sans">1-Hr Threat Quarantine</span>
            </div>
          </div>

          {/* MITRE ATT&CK Active Heatmap */}
          <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
              <div className="flex items-center space-x-2">
                <Target className="h-4 w-4 text-purple-400" />
                <h3 className="font-mono font-bold text-xs text-white uppercase">MITRE ATT&CK Enterprise Matrix (Active Heatmap)</h3>
              </div>
              <div className="flex items-center space-x-2 text-[10px] font-mono">
                <span className="flex items-center space-x-1 text-purple-300">
                  <span className="h-2.5 w-2.5 rounded bg-purple-600"></span>
                  <span>Detected Technique</span>
                </span>
              </div>
            </div>

            <div className="grid grid-cols-7 gap-1.5 text-[10px] font-mono overflow-x-auto min-w-[650px] pb-1">
              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Resource Dev</div>
                <div className="p-1.5 rounded bg-slate-900/40 text-slate-600 border border-slate-800/60 text-[8px] text-center">Acquire Infra</div>
              </div>

              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Initial Access</div>
                <div className="p-1.5 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Valid Accounts</div>
                  <div className="text-[8px] text-purple-200">T1078.004</div>
                </div>
              </div>

              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Execution</div>
                <div className="p-1.5 rounded bg-slate-900/40 text-slate-600 border border-slate-800/60 text-[8px] text-center">Command Line</div>
              </div>

              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Persistence</div>
                <div className="p-1.5 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Account Manip</div>
                  <div className="text-[8px] text-purple-200">T1098</div>
                </div>
              </div>

              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Discovery</div>
                <div className="p-1 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Unsec Creds</div>
                  <div className="text-[8px] text-purple-200">T1552</div>
                </div>
                <div className="p-1 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Acct Discov</div>
                  <div className="text-[8px] text-purple-200">T1087</div>
                </div>
              </div>

              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Collection</div>
                <div className="p-1 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Cloud Storage</div>
                  <div className="text-[8px] text-purple-200">T1530</div>
                </div>
                <div className="p-1 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Archive Data</div>
                  <div className="text-[8px] text-purple-200">T1560</div>
                </div>
              </div>

              <div className="space-y-1">
                <div className="p-1 rounded bg-slate-900 text-slate-400 text-center font-bold text-[9px] border border-slate-800">Exfiltration</div>
                <div className="p-1.5 rounded bg-purple-600 text-white font-bold text-center border border-purple-400 shadow-sm">
                  <div>Exfil to Cloud</div>
                  <div className="text-[8px] text-purple-200">T1567.002</div>
                </div>
              </div>
            </div>
          </div>

          {/* Finding Inspector Card */}
          <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl font-mono text-xs">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800 mb-3">
              <span className="text-cyan-400 font-bold uppercase tracking-wider flex items-center space-x-1.5">
                <Info className="h-4 w-4" />
                <span>{selectedFinding.id} FORENSIC INSPECTOR</span>
              </span>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  selectedFinding.priority === "P1"
                    ? "bg-rose-500/10 text-rose-400 border border-rose-500/30"
                    : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                }`}
              >
                {selectedFinding.priority} | SCORE: {selectedFinding.score}
              </span>
            </div>

            <div className="space-y-2.5 font-sans">
              <h4 className="text-sm font-bold text-white font-mono">
                [{selectedFinding.id}] {selectedFinding.title}
              </h4>
              <p className="text-slate-300 leading-relaxed text-xs">
                {selectedFinding.desc || selectedFinding.description}
              </p>
              <div className="p-3 rounded-lg bg-[#080c17] border border-slate-800 font-mono text-xs space-y-1">
                <div className="text-slate-400 text-[11px]">
                  Evidentiary Log Ref: <span className="text-cyan-400">{Array.isArray(selectedFinding.evidence) ? selectedFinding.evidence.join(", ") : selectedFinding.evidence}</span>
                </div>
                <div className="text-slate-400 text-[11px]">
                  MITRE Technique: <span className="text-purple-300">{selectedFinding.mitre}</span>
                </div>
                <div className="text-slate-400 text-[11px]">
                  Recommended PEP Defense:{" "}
                  <span className="text-emerald-400">
                    {selectedFinding.remediation || selectedFinding.def || "Enforce Zero-Trust perimeter policy."}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Mini Timeline Preview */}
          <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800 mb-3">
              <div className="flex items-center space-x-2">
                <Clock className="h-4 w-4 text-cyan-400" />
                <h3 className="font-mono font-bold text-xs text-white uppercase">Correlated Attack Sequence (03:15 – 03:25 IST)</h3>
              </div>
              <button
                onClick={() => onSwitchTab && onSwitchTab("timeline")}
                className="text-[11px] font-mono text-cyan-400 hover:underline flex items-center space-x-1"
              >
                <span>View Full Timeline</span>
                <ArrowRight className="h-3 w-3" />
              </button>
            </div>

            <div className="space-y-2 text-xs font-mono">
              {TIMELINE_EVENTS.slice(0, 4).map((item, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-[#080c17] border border-slate-800 flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-cyan-400 font-bold">{item.time}</span>
                    <span className="text-slate-500">•</span>
                    <span className="text-slate-200">{item.action}</span>
                  </div>
                  <span className="text-[9px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 font-bold">
                    {item.badge}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* =============================================================== */}
        {/* COLUMN 3: RIGHT PANEL (SPLUNK ES INCIDENT INFO & NOTES)         */}
        {/* =============================================================== */}
        <div className="lg:col-span-3 space-y-5 font-mono text-xs">
          
          {/* Incident Info */}
          <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl space-y-3.5">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <div className="flex items-center space-x-2">
                <Info className="h-4 w-4 text-cyan-400" />
                <h3 className="font-bold text-white uppercase text-xs">Incident Information</h3>
              </div>
              <span className="text-[10px] text-slate-500">SPLUNK ES</span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-[11px]">
              <div>
                <label className="text-slate-400 block mb-1 text-[10px]">Owner</label>
                <select
                  value={owner}
                  onChange={(e) => setOwner(e.target.value)}
                  className="w-full bg-[#080c17] border border-slate-800 text-slate-200 rounded p-1.5 focus:border-cyan-400 focus:outline-none text-[11px]"
                >
                  <option value="lead.dfir@northstar.edu.in">lead.dfir@northstar.edu.in</option>
                  <option value="soc.analyst@northstar.edu.in">soc.analyst@northstar.edu.in</option>
                  <option value="ciso@northstar.edu.in">ciso@northstar.edu.in</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 text-[10px]">Status</label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="w-full bg-[#080c17] border border-slate-800 text-emerald-400 font-bold rounded p-1.5 focus:border-cyan-400 focus:outline-none text-[11px]"
                >
                  <option value="Under Active Containment">Under Active Containment</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Resolved">Resolved</option>
                  <option value="Closed">Closed</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 text-[10px]">Urgency</label>
                <div className="p-1.5 rounded bg-rose-950/60 border border-rose-500/40 text-rose-400 font-bold text-center">
                  Critical (P1)
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 text-[10px]">Sensitivity</label>
                <div className="p-1.5 rounded bg-rose-950/60 border border-rose-500/40 text-rose-400 font-bold text-center">
                  Red (PII Restr.)
                </div>
              </div>
            </div>

            <div>
              <label className="text-slate-400 block mb-1 text-[10px]">Disposition</label>
              <select
                value={disposition}
                onChange={(e) => setDisposition(e.target.value)}
                className="w-full bg-[#080c17] border border-slate-800 text-cyan-400 font-bold rounded p-1.5 focus:border-cyan-400 focus:outline-none text-[11px]"
              >
                <option value="True Positive - Service Token Replay">True Positive - Service Token Replay</option>
                <option value="True Positive - Data Exfiltration">True Positive - Data Exfiltration</option>
                <option value="Under Investigation">Under Investigation</option>
                <option value="False Positive">False Positive</option>
              </select>
            </div>

            <div className="pt-2 border-t border-slate-800 space-y-1.5 text-[11px] font-sans">
              <div className="flex justify-between">
                <span className="text-slate-500 font-mono text-[10px]">Reference ID:</span>
                <code className="text-slate-300 font-mono text-[10px]">c49e016a-1534-7256</code>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 font-mono text-[10px]">Target Entity:</span>
                <code className="text-cyan-400 font-mono text-[10px]">svc_rollcall</code>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 font-mono text-[10px]">Ingress IP:</span>
                <code className="text-rose-400 font-mono text-[10px]">203.0.113.77</code>
              </div>
            </div>
          </div>

          {/* One-Click SOAR Response */}
          <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl space-y-2.5">
            <div className="flex items-center space-x-2 pb-1.5 border-b border-slate-800 text-white font-mono text-xs font-bold">
              <Zap className="h-4 w-4 text-rose-500" />
              <span>One-Click SOAR Response</span>
            </div>

            <button
              onClick={() => executeAction("shun")}
              className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/40 text-rose-300 transition-all"
            >
              <span className="flex items-center space-x-2">
                <Ban className="h-3.5 w-3.5 text-rose-400" />
                <span className="font-bold">Shun IP 203.0.113.77</span>
              </span>
              <span className="text-[9px] bg-rose-950 px-1 py-0.5 rounded">LAYER 0</span>
            </button>

            <button
              onClick={() => executeAction("revoke")}
              className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/40 text-amber-300 transition-all"
            >
              <span className="flex items-center space-x-2">
                <KeyRound className="h-3.5 w-3.5 text-amber-400" />
                <span className="font-bold">Revoke JTI rc-prod-01</span>
              </span>
              <span className="text-[9px] bg-amber-950 px-1 py-0.5 rounded">0ms TTL</span>
            </button>

            <button
              onClick={() => executeAction("isolate")}
              className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/40 text-cyan-300 transition-all"
            >
              <span className="flex items-center space-x-2">
                <HardDrive className="h-3.5 w-3.5 text-cyan-400" />
                <span className="font-bold">Lock CampusVault S3</span>
              </span>
              <span className="text-[9px] bg-cyan-950 px-1 py-0.5 rounded">DLP ENFORCE</span>
            </button>

            <div className="p-2 rounded bg-[#080c17] border border-slate-800 text-[10px] text-slate-400 leading-tight">
              {soarBanner}
            </div>
          </div>

          {/* Dynamic Case Notes Thread */}
          <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-4 shadow-xl space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <div className="flex items-center space-x-2">
                <MessageSquare className="h-4 w-4 text-purple-400" />
                <h3 className="font-bold text-white uppercase text-xs">Investigation Notes ({notes.length})</h3>
              </div>
            </div>

            <div className="space-y-2.5 max-h-56 overflow-y-auto pr-1">
              {notes.map((n, i) => (
                <div key={i} className="p-2.5 bg-[#080c17] rounded-lg border border-slate-800 text-xs">
                  <div className="flex items-center space-x-1.5 mb-1">
                    <div className="h-4 w-4 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold text-[8px]">
                      U
                    </div>
                    <span className="font-bold text-white text-[11px]">{n.author.split("@")[0]}</span>
                    <span className="text-slate-500 text-[10px]">• {n.time}</span>
                  </div>
                  <p className="text-slate-300 font-sans leading-relaxed text-[11px]">{n.text}</p>
                </div>
              ))}
            </div>

            <form onSubmit={handlePostNote} className="pt-2 border-t border-slate-800">
              <textarea
                rows={2}
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                placeholder="Add forensic note or action update..."
                className="w-full bg-[#080c17] border border-slate-800 rounded p-2 text-slate-200 text-xs focus:border-cyan-400 focus:outline-none resize-none"
              />
              <button
                type="submit"
                className="mt-2 w-full py-1.5 rounded bg-purple-600 hover:bg-purple-500 text-white font-bold flex items-center justify-center space-x-1.5 transition-all text-xs"
              >
                <Plus className="h-3.5 w-3.5" />
                <span>Post Case Note</span>
              </button>
            </form>
          </div>

        </div>

      </div>
    </div>
  );
}
