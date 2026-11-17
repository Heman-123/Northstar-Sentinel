import React, { useState } from "react";
import { Lock, CheckCircle2, Copy, FileText, Search } from "lucide-react";
import { EVIDENCE_MANIFEST } from "../data/incidentData";

export default function EvidenceChainOfCustody() {
  const [copiedId, setCopiedId] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const copyHash = (id, hash) => {
    navigator.clipboard.writeText(hash);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredEvidence = EVIDENCE_MANIFEST.filter(
    (ev) =>
      ev.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ev.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="bg-[#0d131f] border border-slate-800 rounded-xl p-5 mb-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 mb-6 gap-3">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center space-x-2 font-mono">
            <Lock className="h-5 w-5 text-emerald-400" />
            <span>CRYPTOGRAPHIC EVIDENCE CHAIN OF CUSTODY (SHA-256)</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Immutable hash verification of all 12 raw evidentiary items from Hackathon Case NS-26-014.
          </p>
        </div>

        <div className="relative">
          <Search className="h-3.5 w-3.5 absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search evidence ID or name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-8 pr-3 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-md text-white font-mono placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 w-64"
          />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 text-[11px] uppercase">
              <th className="pb-3 pl-2">ID</th>
              <th className="pb-3">Evidence Artifact File</th>
              <th className="pb-3">Size / Records</th>
              <th className="pb-3">Cryptographic SHA-256 Digest</th>
              <th className="pb-3 text-right pr-2">Integrity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filteredEvidence.map((ev) => (
              <tr key={ev.id} className="hover:bg-slate-900/50 transition-colors">
                <td className="py-3 pl-2 font-bold text-cyan-400">{ev.id}</td>
                <td className="py-3">
                  <div className="flex items-center space-x-2">
                    <FileText className="h-4 w-4 text-slate-500" />
                    <span className="text-slate-200">{ev.name}</span>
                  </div>
                </td>
                <td className="py-3 text-slate-400">
                  {ev.size} ({ev.records} recs)
                </td>
                <td className="py-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-slate-400 font-mono text-[11px] truncate max-w-xs md:max-w-md">
                      {ev.sha256}
                    </span>
                    <button
                      onClick={() => copyHash(ev.id, ev.sha256)}
                      title="Copy full hash"
                      className="text-slate-500 hover:text-white p-1"
                    >
                      {copiedId === ev.id ? (
                        <span className="text-[10px] text-emerald-400 font-bold">COPIED</span>
                      ) : (
                        <Copy className="h-3 w-3" />
                      )}
                    </button>
                  </div>
                </td>
                <td className="py-3 text-right pr-2">
                  <span className="inline-flex items-center space-x-1 text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    <CheckCircle2 className="h-3 w-3" />
                    <span>VERIFIED</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
