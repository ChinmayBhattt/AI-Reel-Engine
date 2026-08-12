import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "checklist" }>;

const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: "#f2ecdf",
  gradient: "linear-gradient(160deg,#e6edf7 0%,#f3e6dc 55%,#ecdcf1 100%)",
};
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";
const GREEN = "#2fb98a";

export const Checklist: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const dark = (scene.bg ?? "gradient") === "black";

  return (
    <AbsoluteFill style={{ background: BGS[scene.bg ?? "gradient"], justifyContent: "center", alignItems: "center", fontFamily: SANS }}>
      {scene.headline && (
        <div style={{ position: "absolute", top: 260, fontSize: 42, fontWeight: 900, color: dark ? "#fff" : "#111", letterSpacing: 1, textAlign: "center" }}>
          {scene.headline}
        </div>
      )}
      <div style={{ display: "flex", flexDirection: "column", gap: scene.compact ? 18 : 40, marginTop: scene.compact && scene.headline ? 120 : 0 }}>
        {scene.rows.map((r, i) => {
          const at = 0.25 + i * (scene.stagger ?? 0.55);
          const en = spring({ frame: frame - Math.round(at * fps), fps, config: { damping: 15, stiffness: 160 }, durationInFrames: 12 });
          const q = r.state === "q";
          const big = q && !scene.compact; // the ? row is emphasized
          const pulse = q ? 1 + 0.03 * Math.sin(t * 5) : 1;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 28, opacity: en, transform: `translateY(${(1 - en) * 20}px) scale(${big ? pulse : 1})` }}>
              <div
                style={{
                  width: big ? 92 : scene.compact ? 52 : 70,
                  height: big ? 92 : scene.compact ? 52 : 70,
                  borderRadius: 50,
                  background: q ? CYAN : GREEN,
                  color: "#fff",
                  fontSize: big ? 54 : scene.compact ? 30 : 42,
                  fontWeight: 900,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}
              >
                {q ? "?" : "✓"}
              </div>
              <div style={{ fontSize: big ? 88 : scene.compact ? 52 : 64, fontWeight: 900, color: q ? (dark ? "#fff" : "#111") : dark ? "#cfcfcf" : "#333", letterSpacing: 1 }}>
                {r.label}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
