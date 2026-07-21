"use client";

export const dynamic = "force-dynamic";

import { motion } from "framer-motion";
import { Globe, Download, ExternalLink } from "lucide-react";
import PageHeader from "@/components/shared/PageHeader";
import { mockLocations } from "@/services/mockData";
import { getAqiLabel } from "@/lib/utils";

function generateKml(): string {
  const placemarks = mockLocations
    .map(
      (loc) => `
    <Placemark>
      <name>${loc.city} (AQI: ${loc.currentAqi})</name>
      <description><![CDATA[
        <b>State:</b> ${loc.state}<br/>
        <b>AQI:</b> ${loc.currentAqi}<br/>
        <b>Status:</b> ${getAqiLabel(loc.currentAqi)}<br/>
        <b>Pollutant:</b> ${loc.dominantPollutant}<br/>
        <b>Recommendation:</b> ${loc.recommendation}
      ]]></description>
      <Point>
        <coordinates>${loc.longitude},${loc.latitude},0</coordinates>
      </Point>
      <Style>
        <IconStyle>
          <color>${loc.currentAqi > 200 ? "ff0000ff" : loc.currentAqi > 100 ? "ff00aaff" : "ff00ff00"}</color>
          <scale>1.2</scale>
        </IconStyle>
      </Style>
    </Placemark>`
    )
    .join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>AERIS - Air Quality India</name>
    <description>AI-Powered Urban Air Quality Intelligence Platform</description>
    ${placemarks}
  </Document>
</kml>`;
}

function downloadKml() {
  const kml = generateKml();
  const blob = new Blob([kml], { type: "application/vnd.google-earth.kml+xml" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "AQI.kml";
  a.click();
  URL.revokeObjectURL(url);
}

function openGoogleEarth() {
  window.open("https://earth.google.com/web/", "_blank");
}

export default function EarthPage() {
  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      <div className="pb-4 border-b border-white/[0.04]">
        <PageHeader
          title="GIS Exporter"
          subtitle="Export air quality geospatial vectors to KML datasets for Google Earth integration"
          icon={<Globe className="w-5 h-5" style={{ color: "#3B82F6" }} />}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Export KML */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          whileHover={{ y: -3 }}
          className="rounded-2xl p-8 cursor-pointer group border border-white/5"
          style={{
            background: "rgba(24, 24, 27, 0.6)",
            backdropFilter: "blur(16px)",
          }}
          onClick={downloadKml}
        >
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mb-5 transition-transform group-hover:scale-105"
            style={{ background: "rgba(59, 130, 246, 0.08)" }}
          >
            <Download className="w-6 h-6 text-blue-500" />
          </div>
          <h3 className="text-sm font-bold text-zinc-100 uppercase tracking-wider mb-2">Export to KML</h3>
          <p className="text-xs text-zinc-400 mb-6 leading-relaxed">
            Download AQI coordinates for all {mockLocations.length} active stations as standard KML vectors.
            Import directly into Google Earth Pro or standard GIS meshes.
          </p>
          <span
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all bg-blue-500/10 text-blue-400 border border-blue-500/10"
          >
            <Download className="w-3.5 h-3.5" />
            Download AQI.kml
          </span>
        </motion.div>

        {/* View in Google Earth */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
          whileHover={{ y: -3 }}
          className="rounded-2xl p-8 cursor-pointer group border border-white/5"
          style={{
            background: "rgba(24, 24, 27, 0.6)",
            backdropFilter: "blur(16px)",
          }}
          onClick={openGoogleEarth}
        >
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mb-5 transition-transform group-hover:scale-105"
            style={{ background: "rgba(34, 197, 94, 0.08)" }}
          >
            <Globe className="w-6 h-6 text-emerald-500" />
          </div>
          <h3 className="text-sm font-bold text-zinc-100 uppercase tracking-wider mb-2">View in Google Earth</h3>
          <p className="text-xs text-zinc-400 mb-6 leading-relaxed">
            Open Google Earth Studio to visualize air quality nodes on an interactive 3D globe coordinate model.
            KML overlay packages can be imported manually.
          </p>
          <span
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all bg-emerald-500/10 text-emerald-400 border border-emerald-500/10"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            Open Google Earth Web
          </span>
        </motion.div>
      </div>

      {/* Preview */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.16 }}
        className="rounded-2xl p-5 border border-white/5"
        style={{
          background: "rgba(24, 24, 27, 0.6)",
          backdropFilter: "blur(16px)",
        }}
      >
        <h3 className="text-xs font-bold text-zinc-300 uppercase tracking-wider mb-4">Vector Data Preview</h3>
        <div className="max-h-60 overflow-y-auto rounded-xl p-4 font-mono text-[10px] text-zinc-500 leading-relaxed bg-zinc-950/50 border border-white/5">
          <pre>{generateKml().slice(0, 1500)}...</pre>
        </div>
      </motion.div>
    </div>
  );
}
