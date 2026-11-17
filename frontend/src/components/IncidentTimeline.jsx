import React, { useState } from "react";
import { Clock, Filter, AlertCircle, ArrowRight, ShieldCheck } from "lucide-react";
import { TIMELINE_EVENTS } from "../data/incidentData";

export default function IncidentTimeline() {
  const [filter, setFilter] = useState("ALL");

  const filteredEvents = TIMELINE_EVENTS.filter((ev) => {
    if (filter === "ALL") return true;
    if (filter === "API" && ev.source.includes("API Gateway")) return true;
    if (filter === "STORAGE" && ev.source.includes("CampusVault")) return true;
    if (filter === "IDENTITY" && ev.source.includes("Identity")) return true;
    if (filter === "CONFIG" && ev.source.includes("Config")) return true;
    if (filter === "NETWORK" && ev.source.includes("Network")) return true;
    return true;
  });

  return (
    <div className="bg-[#0d131f] border border-slate-800 rounded-xl p-5 mb-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 mb-6 gap-3">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center space-x-2 font-mono">
            <Clock className="h-5 w-5 text-cyan-400" />
            <span>INCIDENT RECONSTRUCTION TIMELINE (12-OCT-2026)</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Correlated sequence from Initial Ingress (03:15:55 IST) to Legitimate Node Resumption (03:25:00 IST).
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center space-x-2 overflow-x-auto">
          <Filter className="h-3.5 w-3.5 text-slate-500 mr-1" />
          {["ALL", "NETWORK", "IDENTITY", "CONFIG", "API", "STORAGE"].map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-2.5 py-1 text-[11px] font-mono rounded-md transition-colors ${
                filter === cat
                  ? "bg-cyan-500 text-black font-bold"
                  : "bg-slate-800/80 text-slate-400 hover:text-white"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-800">
        {filteredEvents.map((ev, index) => {
          const isDanger = ev.badgeColor === "rose";
          const isWarning = ev.badgeColor === "amber";
          const isSuccess = ev.badgeColor === "emerald";
          const isBlue = ev.badgeColor === "blue";

          const dotColor = isDanger
            ? "bg-rose-500 ring-rose-500/20"
            : isWarning
            ? "bg-amber-500 ring-amber-500/20"
            : isSuccess
            ? "bg-emerald-500 ring-emerald-500/20"
            : "bg-cyan-500 ring-cyan-500/20";

          const badgeBg = isDanger
            ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
            : isWarning
            ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
            : isSuccess
            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
            : "bg-cyan-500/10 text-cyan-400 border-cyan-500/30";

          return (
            <div key={index} className="relative group">
              {/* Timeline Indicator Dot */}
              <div
                className={`absolute -left-[27px] top-1.5 h-3.5 w-3.5 rounded-full ring-4 ${dotColor}`}
              />

              <div className="bg-[#111827]/80 hover:bg-[#131d30] border border-slate-800/80 hover:border-slate-700 p-4 rounded-lg transition-all">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                  <div className="flex items-center space-x-3">
                    <span className="text-xs font-mono font-bold text-cyan-400">
                      {ev.time}
                    </span>
                    <span className="text-xs font-mono text-slate-500">|</span>
                    <span className="text-xs font-mono text-slate-400">
                      {ev.source}
                    </span>
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      {ev.id}
                    </span>
                  </div>

                  <span
                    className={`text-[10px] font-mono font-bold uppercase px-2.5 py-0.5 rounded border ${badgeBg}`}
                  >
                    {ev.badge}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs font-mono mb-2">
                  <div>
                    <span className="text-slate-500">Actor: </span>
                    <span className="text-slate-200 font-semibold">{ev.actor}</span>
                  </div>
                  <div>
                    <span className="text-slate-500">Source IP: </span>
                    <span
                      className={`font-semibold ${
                        ev.ip === "203.0.113.77" ? "text-rose-400" : "text-emerald-400"
                      }`}
                    >
                      {ev.ip}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Action: </span>
                    <span className="text-slate-300">{ev.action}</span>
                  </div>
                  <div>
                    <span className="text-slate-500">Target: </span>
                    <span className="text-slate-400">{ev.endpoint}</span>
                  </div>
                </div>

                <p className="text-xs text-slate-300 font-sans leading-relaxed">
                  {ev.details}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
