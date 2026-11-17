import React from "react";
import { Users, Database, Clock, ShieldAlert, Cpu, HardDrive } from "lucide-react";
import { INCIDENT_METRICS } from "../data/incidentData";

export default function MetricsOverview() {
  const cards = [
    {
      title: "Impacted Records",
      value: "2,300",
      sub: "100% of Active Learners (PII)",
      icon: Users,
      color: "rose",
      border: "border-rose-500/30",
      bg: "bg-rose-500/10",
      textColor: "text-rose-400"
    },
    {
      title: "Data Exfiltration Egress",
      value: "972.4 KB",
      sub: "2x Downloads (learners-20261012.csv)",
      icon: HardDrive,
      color: "amber",
      border: "border-amber-500/30",
      bg: "bg-amber-500/10",
      textColor: "text-amber-400"
    },
    {
      title: "Latency Spike Peak",
      value: "8,420 ms",
      sub: "Normal Baseline: 45 ms (~187x surge)",
      icon: Clock,
      color: "cyan",
      border: "border-cyan-500/30",
      bg: "bg-cyan-500/10",
      textColor: "text-cyan-400"
    },
    {
      title: "Attacker Vector",
      value: "203.0.113.77",
      sub: "Replaying svc_rollcall API Key",
      icon: ShieldAlert,
      color: "purple",
      border: "border-purple-500/30",
      bg: "bg-purple-500/10",
      textColor: "text-purple-400"
    },
    {
      title: "Cryptographic Evidence",
      value: "12 / 12",
      sub: "SHA-256 Hashes Verified (100%)",
      icon: Database,
      color: "emerald",
      border: "border-emerald-500/30",
      bg: "bg-emerald-500/10",
      textColor: "text-emerald-400"
    },
    {
      title: "Sentinel PEP Shield",
      value: "ACTIVE",
      sub: "Zero-Trust Enforcement Online",
      icon: Cpu,
      color: "emerald",
      border: "border-emerald-500/30",
      bg: "bg-emerald-500/10",
      textColor: "text-emerald-400"
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className={`bg-[#0d131f] p-3 rounded-lg border ${card.border} flex flex-col justify-between`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-mono text-slate-400 font-medium uppercase tracking-wide">
                {card.title}
              </span>
              <div className={`p-1 rounded ${card.bg} ${card.textColor}`}>
                <Icon className="h-4 w-4" />
              </div>
            </div>
            <div>
              <div className={`text-xl font-bold font-mono ${card.textColor}`}>
                {card.value}
              </div>
              <div className="text-[10px] text-slate-400 font-sans mt-0.5 truncate">
                {card.sub}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
