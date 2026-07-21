"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Users,
  Shield,
  AlertTriangle,
  Cpu,
  Sparkles,
  Play,
  RefreshCw,
  Building,
  Clock,
  CheckCircle2,
  FileText,
  Activity,
  Heart,
  AlertCircle,
  XCircle,
} from "lucide-react";
import { useAdvisory } from "@/hooks/useApi";
import PageHeader from "@/components/shared/PageHeader";
import LoadingSkeleton from "@/components/shared/LoadingSkeleton";
import { getAqiColor, getAqiLabel } from "@/lib/utils";
import { runDecision, runAdvisory } from "@/services/api";
import type { InsightInput, DecisionOutput, AdvisoryResponse } from "@/services/api";

const HEALTH_CARDS = [
  {
    status: "Safe",
    range: "0 - 50",
    color: "#22C55E",
    icon: "🌿",
    description: "Air quality is satisfactory, and air pollution poses little or no risk.",
    actions: ["Ideal for outdoor exercise", "Ventilate indoor spaces", "No special precautions needed"],
  },
  {
    status: "Moderate",
    range: "51 - 100",
    color: "#F59E0B",
    icon: "⚠️",
    description: "Air quality is acceptable; however, there may be risk for some individuals.",
    actions: ["Sensitive groups should monitor symptoms", "Reduce intense outdoor activities", "Keep windows closed during peak traffic"],
  },
  {
    status: "Poor",
    range: "101 - 200",
    color: "#EF4444",
    icon: "😷",
    description: "Sensitive groups may experience health effects. General public may feel minor discomfort.",
    actions: ["Wear protective N95 masks outdoors", "Reduce outdoor workout duration", "Run indoor HEPA air purifiers"],
  },
  {
    status: "Severe",
    range: "201 - 500+",
    color: "#A855F7",
    icon: "🚨",
    description: "Health warning of emergency conditions. Entire population is likely to be affected.",
    actions: ["Avoid all outdoor physical exertion", "Keep all windows and doors sealed", "Hospitals prepare for emergency intakes"],
  },
];

// Preset scenarios for the simulator
const PRESETS = [
  {
    name: "Severe Dust Storm (Ghaziabad)",
    data: {
      aqi: 335,
      forecast: 360,
      confidence: 0.95,
      dominant_pollutant: "PM10",
      source: "Dust",
      hotspot: true,
      nearby_schools: 5,
      nearby_hospitals: 2,
      population_density: "High" as const,
      zone_name: "Indirapuram",
    },
  },
  {
    name: "Industrial Emissions (Kanpur)",
    data: {
      aqi: 278,
      forecast: 265,
      confidence: 0.88,
      dominant_pollutant: "SO2",
      source: "Industrial",
      hotspot: true,
      nearby_schools: 3,
      nearby_hospitals: 1,
      population_density: "Medium" as const,
      zone_name: "Fazalganj",
    },
  },
  {
    name: "Traffic Congestion (Bengaluru)",
    data: {
      aqi: 120,
      forecast: 145,
      confidence: 0.91,
      dominant_pollutant: "NO2",
      source: "Vehicular",
      hotspot: false,
      nearby_schools: 2,
      nearby_hospitals: 0,
      population_density: "Medium" as const,
      zone_name: "Silk Board Junction",
    },
  },
];

export default function AdvisoryPage() {
  const { data: defaultAdvisory, isLoading: isDefaultLoading } = useAdvisory();
  const [activeTab, setActiveTab] = useState<"standard" | "sandbox">("sandbox");

  // Simulator Form State
  const [formData, setFormData] = useState<InsightInput>({
    aqi: 312,
    forecast: 340,
    confidence: 0.92,
    dominant_pollutant: "PM2.5",
    source: "Construction",
    hotspot: true,
    nearby_schools: 4,
    nearby_hospitals: 2,
    population_density: "High",
    zone_name: "Anand Vihar Sector 4",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [decisionResult, setDecisionResult] = useState<DecisionOutput | null>(null);
  const [advisoryResult, setAdvisoryResult] = useState<AdvisoryResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const applyPreset = (preset: typeof PRESETS[0]["data"]) => {
    setFormData(preset);
  };

  const handleRunEvaluation = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    setDecisionResult(null);
    setAdvisoryResult(null);

    try {
      // Step 1: Run Agent 1 (Decision Engine)
      const decision = await runDecision(formData);
      setDecisionResult(decision);

      // Step 2: Run Agent 2 (LLM Advisor)
      const advisory = await runAdvisory(decision);
      setAdvisoryResult(advisory);
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || "An unexpected error occurred during execution.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-white/[0.04]">
        <PageHeader
          title="Advisory Studio"
          subtitle="Citizen public health recommendations and multi-agent AI command sandbox"
          icon={<Users className="w-5 h-5" style={{ color: "#3B82F6" }} />}
        />

        {/* Tab Selector */}
        <div
          className="flex p-1 rounded-xl self-start md:self-auto bg-zinc-900/60 border border-white/5"
        >
          <button
            onClick={() => setActiveTab("standard")}
            className={`px-4 py-1.5 rounded-lg text-[11px] font-bold transition-all ${
              activeTab === "standard"
                ? "text-blue-400 bg-blue-500/10"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            Citizen Health Guide
          </button>
          <button
            onClick={() => setActiveTab("sandbox")}
            className={`px-4 py-1.5 rounded-lg text-[11px] font-bold transition-all flex items-center gap-1.5 ${
              activeTab === "sandbox"
                ? "text-blue-400 bg-blue-500/10"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            AI Sandbox
          </button>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === "standard" ? (
          /* PRESETS CITIZEN GUIDE HEALTH CARDS */
          <motion.div
            key="standard"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
          >
            {HEALTH_CARDS.map((card, i) => (
              <motion.div
                key={card.status}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="rounded-2xl p-5 flex flex-col justify-between h-[320px] transition-all border border-white/5"
                style={{
                  background: "rgba(24, 24, 27, 0.6)",
                  backdropFilter: "blur(16px)",
                }}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-3xl">{card.icon}</span>
                    <span
                      className="text-[9px] font-bold px-2 py-0.5 rounded-full"
                      style={{ background: `${card.color}08`, color: card.color, border: `1px solid ${card.color}15` }}
                    >
                      AQI {card.range}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-zinc-100 uppercase tracking-wider mb-2" style={{ color: card.color }}>
                    {card.status}
                  </h3>
                  <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                    {card.description}
                  </p>
                </div>

                <div className="space-y-1.5 border-t border-white/[0.04] pt-4">
                  <span className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">Recommended Steps</span>
                  <div className="space-y-1">
                    {card.actions.map((act, idx) => (
                      <div key={idx} className="flex items-start gap-1.5 text-[10px] text-zinc-300 leading-normal">
                        <span className="text-[#3B82F6] font-bold">•</span>
                        <span>{act}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          /* MULTI-AGENT MODEL SANDBOX VIEW */
          <motion.div
            key="sandbox"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-6"
          >
            {/* Input Form & Presets Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Telemetry Input Panel */}
              <div
                className="lg:col-span-2 rounded-2xl p-5 sm:p-6 space-y-4 border border-white/5"
                style={{
                  background: "rgba(24, 24, 27, 0.6)",
                  backdropFilter: "blur(16px)",
                }}
              >
                <div className="flex items-center justify-between border-b border-white/[0.04] pb-3">
                  <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider flex items-center gap-2">
                    <Cpu className="w-4 h-4 text-blue-500" />
                    Telemetry Payload (InsightInput)
                  </h3>
                  <span className="text-[9px] text-zinc-500 uppercase tracking-widest font-bold">
                    Agent 1 Parameters
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {/* Zone Name */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Zone/Ward Name
                    </label>
                    <input
                      type="text"
                      value={formData.zone_name || ""}
                      onChange={(e) => setFormData({ ...formData, zone_name: e.target.value })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    />
                  </div>

                  {/* Current AQI */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Current AQI (0-500)
                    </label>
                    <input
                      type="number"
                      value={formData.aqi}
                      onChange={(e) => setFormData({ ...formData, aqi: Number(e.target.value) })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    />
                  </div>

                  {/* Forecast AQI */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Forecast AQI (0-500)
                    </label>
                    <input
                      type="number"
                      value={formData.forecast}
                      onChange={(e) => setFormData({ ...formData, forecast: Number(e.target.value) })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    />
                  </div>

                  {/* Confidence */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Forecast Confidence (0-1)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      max="1"
                      value={formData.confidence}
                      onChange={(e) => setFormData({ ...formData, confidence: Number(e.target.value) })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    />
                  </div>

                  {/* Dominant Pollutant */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Dominant Pollutant
                    </label>
                    <select
                      value={formData.dominant_pollutant}
                      onChange={(e) => setFormData({ ...formData, dominant_pollutant: e.target.value })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    >
                      {["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"].map((p) => (
                        <option key={p} value={p} className="bg-zinc-900">
                          {p}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Emission Source */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Emission Source
                    </label>
                    <select
                      value={formData.source}
                      onChange={(e) => setFormData({ ...formData, source: e.target.value })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    >
                      {["Construction", "Dust", "Industrial", "Vehicular", "Stubble Burning", "Waste Burning"].map((s) => (
                        <option key={s} value={s} className="bg-zinc-900">
                          {s}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Nearby Schools */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Nearby Schools
                    </label>
                    <input
                      type="number"
                      value={formData.nearby_schools}
                      onChange={(e) => setFormData({ ...formData, nearby_schools: Number(e.target.value) })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    />
                  </div>

                  {/* Nearby Hospitals */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Nearby Hospitals
                    </label>
                    <input
                      type="number"
                      value={formData.nearby_hospitals}
                      onChange={(e) => setFormData({ ...formData, nearby_hospitals: Number(e.target.value) })}
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    />
                  </div>

                  {/* Population Density */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[9px] font-bold uppercase tracking-wider text-zinc-500">
                      Population Density
                    </label>
                    <select
                      value={formData.population_density}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          population_density: e.target.value as "Low" | "Medium" | "High",
                        })
                      }
                      className="px-3 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50"
                    >
                      {["Low", "Medium", "High"].map((d) => (
                        <option key={d} value={d} className="bg-zinc-900">
                          {d}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Hotspot Checkbox */}
                <div className="flex items-center gap-2.5 pt-1">
                  <input
                    type="checkbox"
                    id="hotspot-checkbox"
                    checked={formData.hotspot}
                    onChange={(e) => setFormData({ ...formData, hotspot: e.target.checked })}
                    className="w-4 h-4 rounded bg-zinc-950 border-white/10 text-blue-500 focus:ring-blue-500/20"
                  />
                  <label htmlFor="hotspot-checkbox" className="text-xs text-zinc-400 font-medium cursor-pointer">
                    Flag zone as a persistent pollution hotspot (+10 risk weight)
                  </label>
                </div>

                {/* Evaluate Action Button */}
                <div className="flex justify-end border-t border-white/[0.04] pt-4">
                  <motion.button
                    whileTap={{ scale: 0.98 }}
                    onClick={handleRunEvaluation}
                    disabled={isLoading}
                    className="px-6 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 transition-all relative overflow-hidden"
                    style={{
                      background: "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)",
                      color: "#FAFAFA",
                      boxShadow: "0 4px 12px rgba(59, 130, 246, 0.25)",
                    }}
                  >
                    {isLoading ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Evaluating...</span>
                      </>
                    ) : (
                      <>
                        <Play className="w-3.5 h-3.5" />
                        <span>Run Multi-Agent Workflow</span>
                      </>
                    )}
                  </motion.button>
                </div>
              </div>

              {/* Scenarios Preset Selection */}
              <div
                className="rounded-2xl p-5 sm:p-6 flex flex-col justify-between border border-white/5"
                style={{
                  background: "rgba(24, 24, 27, 0.6)",
                  backdropFilter: "blur(16px)",
                }}
              >
                <div className="space-y-4">
                  <div className="border-b border-white/[0.04] pb-3">
                    <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">
                      Simulation Presets
                    </h3>
                    <p className="text-[10px] text-zinc-500 mt-1">
                      Seed the sandbox with specific incident contexts
                    </p>
                  </div>
                  <div className="space-y-2">
                    {PRESETS.map((preset) => (
                      <button
                        key={preset.name}
                        onClick={() => applyPreset(preset.data)}
                        className="w-full text-left p-3 rounded-xl bg-zinc-900/30 hover:bg-zinc-900/60 border border-white/5 hover:border-blue-500/20 transition-all text-xs font-semibold text-zinc-300 hover:text-white flex items-center justify-between"
                      >
                        <span>{preset.name}</span>
                        <span className="text-[9px] font-bold text-blue-400 px-2 py-0.5 rounded-full bg-blue-500/10">
                          AQI {preset.data.aqi}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>

                <div
                  className="rounded-xl p-3 bg-blue-500/5 border border-blue-500/10 text-[10px] text-blue-400 leading-relaxed mt-4"
                >
                  <strong>💡 Orchestrator Engine:</strong> Agent 1 runs a deterministic rules pipeline, then passes the resulting structured decision to Agent 2. Agent 2 triggers concurrent Groq LLM queries to synthesize text advisories.
                </div>
              </div>
            </div>

            {/* Error message */}
            {errorMsg && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 rounded-xl border border-red-500/30 bg-red-500/10 text-xs font-medium text-red-400"
              >
                ⚠️ <strong>Error executing pipeline:</strong> {errorMsg}. Ensure the backend is active at `http://localhost:8000` and `GROQ_API_KEY` is set.
              </motion.div>
            )}

            {/* AI Multi-Agent Results Section */}
            {(decisionResult || advisoryResult) && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Agent 1: Decision Intelligence Output */}
                {decisionResult && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="rounded-2xl p-5 sm:p-6 space-y-4 border border-white/5"
                    style={{
                      background: "rgba(24, 24, 27, 0.7)",
                      backdropFilter: "blur(16px)",
                    }}
                  >
                    <div className="flex items-center justify-between border-b border-white/[0.04] pb-3">
                      <div className="flex items-center gap-2">
                        <Cpu className="w-4 h-4 text-blue-500" />
                        <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">
                          Agent 1: Decision Output
                        </h3>
                      </div>
                      <span className="text-[9px] text-blue-400 font-bold tracking-wider uppercase bg-blue-500/10 px-2.5 py-0.5 rounded-full">
                        Deterministic Rules
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      {/* Risk Score Card */}
                      <div className="bg-zinc-950/40 p-4 rounded-xl border border-white/5 flex flex-col items-center justify-center text-center">
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">
                          Risk Score
                        </span>
                        <div className="text-3xl font-extrabold text-zinc-100 tracking-tight mt-1">
                          {decisionResult.risk_score}
                          <span className="text-[10px] text-zinc-500 font-normal">/100</span>
                        </div>
                      </div>

                      {/* Priority Card */}
                      <div className="bg-zinc-950/40 p-4 rounded-xl border border-white/5 flex flex-col items-center justify-center text-center">
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">
                          Priority Band
                        </span>
                        <span
                          className="text-sm font-extrabold mt-2 uppercase tracking-wide"
                          style={{
                            color:
                              decisionResult.priority === "Critical"
                                ? "#A855F7"
                                : decisionResult.priority === "High"
                                ? "#EF4444"
                                : decisionResult.priority === "Medium"
                                ? "#F59E0B"
                                : "#22C55E",
                          }}
                        >
                          {decisionResult.priority}
                        </span>
                      </div>

                      {/* Response Time SLA Card */}
                      <div className="bg-zinc-950/40 p-4 rounded-xl border border-white/5 flex flex-col items-center justify-center text-center">
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">
                          Response SLA
                        </span>
                        <span className="text-xs font-bold text-zinc-200 mt-2 flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5 text-zinc-400" />
                          {decisionResult.response_time}
                        </span>
                      </div>
                    </div>

                    {/* Authority Card */}
                    <div className="bg-zinc-950/30 p-4 rounded-xl border border-white/5 flex items-start gap-3">
                      <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-zinc-900 flex-shrink-0 mt-0.5">
                        <Building className="w-4 h-4 text-zinc-400" />
                      </div>
                      <div>
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider block">Assigned Incident Authority</span>
                        <p className="text-xs font-bold text-zinc-300 mt-0.5">
                          {decisionResult.authority}
                        </p>
                      </div>
                    </div>

                    {/* Recommended Action Card */}
                    <div className="space-y-2">
                      <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">Compliance Action directives</span>
                      <div className="space-y-1.5">
                        {decisionResult.recommended_actions.map((act, idx) => (
                          <div
                            key={idx}
                            className="text-[11px] text-zinc-300 flex items-start gap-2 bg-zinc-900/30 p-2.5 rounded-lg border border-white/[0.02]"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                            <span>{act}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Reasoning Trail */}
                    <div className="space-y-2">
                      <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">Scoring Reasoning</span>
                      <div className="space-y-1">
                        {decisionResult.reason.map((reason, idx) => (
                          <div
                            key={idx}
                            className="text-[11px] text-zinc-400 flex items-start gap-1.5"
                          >
                            <span className="text-blue-500 font-bold">•</span>
                            <span>{reason}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Agent 2: LLM Advisory Output */}
                {advisoryResult ? (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.05 }}
                    className="rounded-2xl p-5 sm:p-6 space-y-4 border border-white/5"
                    style={{
                      background: "rgba(24, 24, 27, 0.7)",
                      backdropFilter: "blur(16px)",
                    }}
                  >
                    <div className="flex items-center justify-between border-b border-white/[0.04] pb-3">
                      <div className="flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-emerald-400" />
                        <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">
                          Agent 2: LLM Advisories
                        </h3>
                      </div>
                      <span className="text-[9px] text-emerald-400 font-bold tracking-wider uppercase bg-emerald-500/10 px-2.5 py-0.5 rounded-full">
                        Llama 3.3 70B
                      </span>
                    </div>

                    {/* Authority Advisory */}
                    <div className="space-y-2">
                      <div className="flex items-center gap-1.5">
                        <Building className="w-3.5 h-3.5 text-zinc-400" />
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">
                          Operational Directive (For Authorities)
                        </span>
                      </div>
                      <div
                        className="p-4 rounded-xl text-xs text-zinc-300 leading-relaxed font-serif bg-zinc-950/40 border border-white/5"
                      >
                        {advisoryResult.authority_advisory}
                      </div>
                    </div>

                    {/* Citizen Advisory */}
                    <div className="space-y-2">
                      <div className="flex items-center gap-1.5">
                        <Users className="w-3.5 h-3.5 text-zinc-400" />
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-wider">
                          Public Health Advisory (For Citizens)
                        </span>
                      </div>
                      <div
                        className="p-4 rounded-xl text-xs text-zinc-300 leading-relaxed font-serif bg-zinc-950/40 border border-white/5"
                      >
                        {advisoryResult.citizen_advisory}
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  isLoading && (
                    <div className="rounded-2xl p-6 border border-dashed border-white/10 flex flex-col items-center justify-center text-center text-zinc-500 py-24">
                      <RefreshCw className="w-8 h-8 text-blue-500 animate-spin mb-4" />
                      <p className="text-xs font-bold uppercase tracking-wider text-zinc-400">
                        Synthesizing Natural-Language Advisories
                      </p>
                      <p className="text-[10px] text-zinc-600 mt-1 max-w-xs leading-relaxed">
                        Groq Llama model is compiling structured decision outputs into directives...
                      </p>
                    </div>
                  )
                )}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
