import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";
import { useTheme } from "../theme/tokens";
import type { CaptionWord } from "../types";

/** Split chip text into plain/emphasized runs based on the emphasis list. */
const tokenize = (
  text: string,
  emphasis: string[]
): { text: string; emph: boolean }[] => {
  if (!emphasis.length) return [{ text, emph: false }];
  const pattern = emphasis
    .map((e) => e.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
    .join("|");
  const re = new RegExp(`(${pattern})`, "gi");
  return text
    .split(re)
    .filter((s) => s.length > 0)
    .map((s) => ({
      text: s,
      emph: emphasis.some((e) => e.toLowerCase() === s.toLowerCase()),
    }));
};

/**
 * Word-synced caption chips, Varun-sized: large bold white on black pill,
 * key tokens (numbers, prices, names) pop in accent yellow and bigger.
 */
const isEmph = (word: string, emphasis: string[]) => {
  const clean = word.replace(/[^\w$%+.'-]/g, "").toLowerCase();
  return emphasis.some((e) => {
    const el = e.toLowerCase();
    return el === clean || (el.includes(" ") && el.split(" ").includes(clean));
  });
};

/**
 * "nick-display" caption: Nick Saraev's caption system, measured from his 12
 * reels (2026-07-30 teardown). Big free-floating text, NO pill: connective
 * words in italic, the KEY word (emphasis list) lands heavier + bigger +
 * accent-colored. Words accumulate as spoken (per-word reveal). Deep soft
 * drop shadow carries legibility; `themes` ranges flip white↔ink so text
 * never blends with cream card fields. (SF Pro only — the italic voice is
 * SF Pro Italic, not a serif, per the 2026-07-29 brand font rule.)
 */
const NickDisplay: React.FC<{
  active: CaptionWord;
  emphasis: string[];
  bottom: number;
  dark: boolean;
  accent: string;
  fps: number;
  frame: number;
}> = ({ active, emphasis, bottom, dark, accent, fps, frame }) => {
  const t = frame / fps;
  const words = active.words ?? [{ t: active.start, text: active.text }];
  const base = dark ? "#141414" : "#ffffff";
  const shadow = dark
    ? "0 3px 10px rgba(0,0,0,0.22), 0 1px 3px rgba(0,0,0,0.18)"
    : "0 4px 16px rgba(0,0,0,0.85), 0 1px 3px rgba(0,0,0,0.6)";
  return (
    <div
      style={{
        position: "absolute",
        left: 40,
        right: 40,
        bottom,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "baseline",
        columnGap: 20,
        rowGap: 2,
        pointerEvents: "none",
      }}
    >
      {words.map((w, i) => {
        if (t < w.t - 0.02) return null;
        const local = frame - Math.round(w.t * fps);
        const pop = spring({
          frame: local,
          fps,
          config: { damping: 14, stiffness: 320, mass: 0.4 },
          durationInFrames: 6,
        });
        const emph = isEmph(w.text, emphasis);
        return (
          <span
            key={i}
            style={{
              fontFamily:
                "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
              fontStyle: emph ? "normal" : "italic",
              fontWeight: emph ? 900 : 700,
              fontSize: emph ? 86 : 66,
              letterSpacing: emph ? "-0.015em" : "0.005em",
              lineHeight: 1.12,
              color: emph ? accent : base,
              textShadow: shadow,
              opacity: pop,
              transform: `translateY(${(1 - pop) * 14}px) scale(${
                0.9 + 0.1 * pop
              })`,
              display: "inline-block",
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};

export const CaptionChips: React.FC<{
  captions: CaptionWord[];
  mode?: "sans" | "mono" | "chip-small" | "chip-lg" | "nick-display";
  emphasis?: string[];
  /** time-ranged bottom offsets so chips never cover a face */
  positions?: { start: number; end: number; bottom: number }[];
  /** time ranges where chips are suppressed (display-type scenes own the text) */
  hidden?: { start: number; end: number }[];
  /** time ranges where the caption text theme is dark (ink on light fields) */
  darkRanges?: { start: number; end: number }[];
}> = ({
  captions,
  mode = "sans",
  emphasis = [],
  positions = [],
  hidden = [],
  darkRanges = [],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const theme = useTheme();
  const ACCENT = theme.accent;
  const t = frame / fps;

  if (hidden.some((h) => t >= h.start && t < h.end)) return null;

  const active = captions.find((c) => t >= c.start && t < c.end);
  if (!active) return null;

  if (mode === "nick-display") {
    const dark = darkRanges.some((r) => t >= r.start && t < r.end);
    return (
      <NickDisplay
        active={active}
        emphasis={emphasis}
        bottom={positions.find((p) => t >= p.start && t < p.end)?.bottom ?? 400}
        dark={dark}
        accent={dark ? "#E8A200" : ACCENT}
        fps={fps}
        frame={frame}
      />
    );
  }

  const localFrame = frame - Math.round(active.start * fps);
  const pop = spring({
    frame: localFrame,
    fps,
    config: { damping: 13, stiffness: 300, mass: 0.35 },
    durationInFrames: 7,
  });
  const scale = 0.88 + 0.12 * pop;

  const font =
    mode === "chip-lg"
      ? {
          fontFamily:
            "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
          fontSize: 50,
          fontWeight: 800 as const,
          letterSpacing: "-0.01em",
        }
      : mode === "chip-small"
      ? {
          fontFamily:
            "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
          fontSize: 38,
          fontWeight: 700 as const,
        }
      : mode === "mono"
      ? {
          fontFamily: "'Menlo', 'Courier New', monospace",
          textTransform: "uppercase" as const,
          fontSize: 48,
          letterSpacing: "0.02em",
          fontWeight: 700 as const,
        }
      : {
          fontFamily:
            "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
          fontSize: 56,
          fontWeight: 800 as const,
        };

  const runs = tokenize(active.text, emphasis);
  const hasEmph = runs.some((r) => r.emph);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: positions.find((p) => t >= p.start && t < p.end)?.bottom ?? 400,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          ...font,
          color: "white",
          background:
            mode === "chip-small"
              ? "rgba(0,0,0,0.55)"
              : mode === "chip-lg"
              ? "rgba(0,0,0,0.82)"
              : "rgba(0,0,0,0.94)",
          padding:
            mode === "chip-small"
              ? "9px 20px"
              : mode === "chip-lg"
              ? "13px 26px"
              : "14px 30px",
          borderRadius: mode === "chip-small" ? 9 : mode === "chip-lg" ? 12 : 14,
          transform: `scale(${hasEmph ? scale * 1.04 : scale})`,
          maxWidth: 940,
          textAlign: "center",
          lineHeight: 1.18,
          boxShadow:
            mode === "chip-lg"
              ? "0 6px 26px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(255,255,255,0.08)"
              : "0 4px 22px rgba(0,0,0,0.45)",
        }}
      >
        {runs.map((r, i) =>
          r.emph ? (
            <span
              key={i}
              style={{
                color: ACCENT,
                fontSize: "1.22em",
                fontWeight: 900,
                textShadow: `0 0 22px ${ACCENT}73`,
              }}
            >
              {r.text}
            </span>
          ) : (
            <span key={i}>{r.text}</span>
          )
        )}
      </div>
    </div>
  );
};
