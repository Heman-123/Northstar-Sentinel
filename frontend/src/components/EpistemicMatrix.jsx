import React from "react";
import { CheckCircle2, HelpCircle, AlertOctagon, Scale } from "lucide-react";
import { EPISTEMIC_MATRIX } from "../data/incidentData";

export default function EpistemicMatrix() {
  return (
    <div className="bg-[#0d131f] border border-slate-800 rounded-xl p-5 mb-8">
      <div className="pb-4 border-b border-slate-800 mb-6">
        <h2 className="text-lg font-bold text-white flex items-center space-x-2 font-mono">
          <Scale className="h-5 w-5 text-cyan-400" />
          <span>EPISTEMIC TRUTH MATRIX: FORENSIC RIGOR AUDIT</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Strict separation of log-grounded observations from deductive inferences and unknown variables. Avoids attribution hallucinations.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tier 1: Confirmed Observations */}
        <div className="bg-[#111827]/80 border border-emerald-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-emerald-400 mb-3 pb-2 border-b border-emerald-500/20">
              <CheckCircle2 className="h-5 w-5" />
              <span className="font-mono font-bold text-sm tracking-wider uppercase">
                Tier 1: Confirmed Facts
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mb-4 font-sans">
              Directly proven by immutable log entries, timestamps, and cryptographic artifacts.
            </p>
            <div className="space-y-3">
              {EPISTEMIC_MATRIX.confirmedFacts.map((fact) => (
                <div
                  key={fact.id}
                  className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 text-xs"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono font-bold text-emerald-400 text-[10px]">
                      {fact.id}
                    </span>
                    <span className="font-mono text-slate-400 text-[10px] bg-slate-800 px-1.5 py-0.5 rounded">
                      {fact.citation}
                    </span>
                  </div>
                  <p className="text-slate-300 font-sans text-xs">{fact.claim}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] font-mono text-emerald-400/80">
            ✓ 100% Evidentiary Grounding
          </div>
        </div>

        {/* Tier 2: Strongly Supported Inferences */}
        <div className="bg-[#111827]/80 border border-cyan-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-cyan-400 mb-3 pb-2 border-b border-cyan-500/20">
              <HelpCircle className="h-5 w-5" />
              <span className="font-mono font-bold text-sm tracking-wider uppercase">
                Tier 2: Supported Inferences
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mb-4 font-sans">
              Logical technical deductions derived from cross-correlation of multiple evidence streams.
            </p>
            <div className="space-y-3">
              {EPISTEMIC_MATRIX.supportedInferences.map((inf) => (
                <div
                  key={inf.id}
                  className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 text-xs"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono font-bold text-cyan-400 text-[10px]">
                      {inf.id}
                    </span>
                    <span className="font-mono text-slate-400 text-[10px] bg-slate-800 px-1.5 py-0.5 rounded">
                      {inf.citation}
                    </span>
                  </div>
                  <p className="text-slate-300 font-sans text-xs">{inf.claim}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] font-mono text-cyan-400/80">
            ℹ Multi-Point Correlation
          </div>
        </div>

        {/* Tier 3: Epistemic Unknowns */}
        <div className="bg-[#111827]/80 border border-amber-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-amber-400 mb-3 pb-2 border-b border-amber-500/20">
              <AlertOctagon className="h-5 w-5" />
              <span className="font-mono font-bold text-sm tracking-wider uppercase">
                Tier 3: Epistemic Unknowns
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mb-4 font-sans">
              Critical variables that cannot be definitively established from available evidence.
            </p>
            <div className="space-y-3">
              {EPISTEMIC_MATRIX.epistemicUnknowns.map((unk) => (
                <div
                  key={unk.id}
                  className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 text-xs"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono font-bold text-amber-400 text-[10px]">
                      {unk.id}
                    </span>
                    <span className="font-mono text-slate-400 text-[10px] bg-slate-800 px-1.5 py-0.5 rounded">
                      {unk.citation}
                    </span>
                  </div>
                  <p className="text-slate-300 font-sans text-xs">{unk.claim}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] font-mono text-amber-400/80">
            ⚠ Explicitly Unattributed
          </div>
        </div>
      </div>
    </div>
  );
}
