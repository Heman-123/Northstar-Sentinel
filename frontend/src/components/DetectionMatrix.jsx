import React, { useState } from "react";
import { AlertTriangle, Shield, CheckCircle, ChevronDown, ChevronUp, ExternalLink } from "lucide-react";
import { DETECTION_RULES } from "../data/incidentData";

export default function DetectionMatrix() {
  const [expandedId, setExpandedId] = useState("DET-001");

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="bg-[#0d131f] border border-slate-800 rounded-xl p-5 mb-8">
      <div className="pb-4 border-b border-slate-800 mb-6">
        <h2 className="text-lg font-bold text-white flex items-center space-x-2 font-mono">
          <AlertTriangle className="h-5 w-5 text-amber-400" />
          <span>BEHAVIORAL & POLICY DETECTION RULES (DET-001 TO DET-010)</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Explainable, deterministic detection rules with decoupled Severity and Confidence scores. No black-box hallucinations.
        </p>
      </div>

      <div className="space-y-3">
        {DETECTION_RULES.map((rule) => {
          const isExpanded = expandedId === rule.id;
          const isP1 = rule.tier.startsWith("P1");
          const isP2 = rule.tier.startsWith("P2");

          const tierColor = isP1
            ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
            : isP2
            ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
            : "bg-blue-500/10 text-blue-400 border-blue-500/30";

          return (
            <div
              key={rule.id}
              className="bg-[#111827]/80 border border-slate-800 rounded-lg overflow-hidden transition-all hover:border-slate-700"
            >
              {/* Rule Card Header */}
              <div
                onClick={() => toggleExpand(rule.id)}
                className="p-4 flex items-center justify-between cursor-pointer select-none"
              >
                <div className="flex items-center space-x-3 flex-1 pr-4">
                  <span className="font-mono text-xs font-bold text-cyan-400 bg-cyan-950/60 px-2 py-1 rounded border border-cyan-800/40">
                    {rule.id}
                  </span>
                  <div>
                    <h3 className="text-sm font-semibold text-white font-sans">
                      {rule.title}
                    </h3>
                    <div className="flex items-center space-x-3 mt-1">
                      <span className="text-[10px] font-mono text-slate-400">
                        MITRE: <span className="text-slate-300 font-semibold">{rule.mitre}</span>
                      </span>
                      <span className="text-[10px] font-mono text-slate-400">
                        OWASP: <span className="text-slate-300 font-semibold">{rule.owasp}</span>
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="hidden sm:flex flex-col items-end mr-2">
                    <span className="text-[10px] font-mono text-slate-400">Triage Score</span>
                    <span className="text-xs font-mono font-bold text-white">
                      {rule.triageScore}/100
                    </span>
                  </div>
                  <span
                    className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded border ${tierColor}`}
                  >
                    {rule.severity}
                  </span>
                  {isExpanded ? (
                    <ChevronUp className="h-4 w-4 text-slate-400" />
                  ) : (
                    <ChevronDown className="h-4 w-4 text-slate-400" />
                  )}
                </div>
              </div>

              {/* Collapsible Details */}
              {isExpanded && (
                <div className="p-4 bg-slate-950/50 border-t border-slate-800 text-xs space-y-3 font-sans">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-slate-400 font-mono text-[11px] block mb-1">
                        Supporting Evidence Citations:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {rule.evidence.map((ev, idx) => (
                          <span
                            key={idx}
                            className="bg-slate-800 text-cyan-300 px-2 py-0.5 rounded font-mono text-[10px] border border-slate-700"
                          >
                            {ev}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-400 font-mono text-[11px] block mb-1">
                        Priority Evaluation:
                      </span>
                      <span className="text-slate-200 font-mono font-semibold">
                        {rule.tier} (Confidence: {rule.confidence})
                      </span>
                    </div>
                  </div>

                  <div className="bg-emerald-950/30 border border-emerald-500/20 p-3 rounded-lg">
                    <div className="flex items-center space-x-2 text-emerald-400 font-mono text-[11px] font-bold mb-1">
                      <Shield className="h-4 w-4" />
                      <span>RECOMMENDED DEFENSIVE CONTROL</span>
                    </div>
                    <p className="text-emerald-200/90 text-xs">
                      {rule.defense}
                    </p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
