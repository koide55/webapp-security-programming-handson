#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");

const [, , inputPath, outputPath] = process.argv;

if (!inputPath || !outputPath) {
  console.error("Usage: node tools/build_slide_deck.mjs <input.md> <output.pptx>");
  process.exit(1);
}

function stripFrontmatter(text) {
  if (!text.startsWith("---\n")) return text;
  const end = text.indexOf("\n---\n", 4);
  return end === -1 ? text : text.slice(end + 5);
}

function splitSlides(markdown) {
  return stripFrontmatter(markdown)
    .split(/\n---\n/g)
    .map((slide) => slide.trim())
    .filter(Boolean);
}

function cleanTextLine(line) {
  return line
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1")
    .trimEnd();
}

function parseSlide(raw) {
  const lines = raw
    .split(/\r?\n/)
    .filter((line) => !line.trim().startsWith("<!--"));
  const titleLine = lines.find((line) => line.startsWith("# "));
  const title = titleLine ? titleLine.replace(/^#\s+/, "").trim() : "Slide";
  const bodyLines = [];
  let inTitle = false;
  for (const line of lines) {
    if (!inTitle && line === titleLine) {
      inTitle = true;
      continue;
    }
    bodyLines.push(line);
  }

  const segments = [];
  let codeBuffer = [];
  let textBuffer = [];
  let inCode = false;

  function flushText() {
    const text = textBuffer.join("\n").trim();
    if (text) segments.push({ type: "text", text });
    textBuffer = [];
  }

  function flushCode() {
    segments.push({ type: "code", text: codeBuffer.join("\n") });
    codeBuffer = [];
  }

  for (const line of bodyLines) {
    const fence = line.match(/^```/);
    if (fence) {
      if (inCode) {
        flushCode();
        inCode = false;
      } else {
        flushText();
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeBuffer.push(line);
    } else {
      textBuffer.push(line);
    }
  }

  if (inCode) flushCode();
  flushText();
  return { title, segments };
}

function normalizeTextBlock(text) {
  return text
    .split(/\r?\n/)
    .map((line) => {
      const trimmed = cleanTextLine(line.trim());
      if (!trimmed) return "";

      const unordered = trimmed.match(/^[-*]\s+(.*)$/);
      if (unordered) return `- ${unordered[1]}`;

      const nested = line.match(/^\s{2,}[-*]\s+(.*)$/);
      if (nested) return `  - ${cleanTextLine(nested[1])}`;

      return trimmed;
    })
    .join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function estimateHeight(text, fontSize, widthInches) {
  const charsPerLine = Math.max(24, Math.floor(widthInches * 12));
  const lines = text.split(/\n/).reduce((count, line) => {
    const len = Math.max(1, line.length);
    return count + Math.ceil(len / charsPerLine);
  }, 0);
  return Math.max(0.28, (lines * fontSize * 1.24) / 72);
}

function addFooter(pptx, slide, page, total) {
  slide.addText("webapp-security-programming-handson", {
    x: 0.67,
    y: 7.18,
    w: 4.2,
    h: 0.15,
    fontFace: "Aptos",
    fontSize: 6.5,
    color: "7b8794",
    margin: 0,
  });
  slide.addText(`${String(page).padStart(2, "0")} / ${total}`, {
    x: 11.9,
    y: 7.18,
    w: 0.75,
    h: 0.15,
    fontFace: "Aptos",
    fontSize: 6.5,
    color: "7b8794",
    align: "right",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.67,
    y: 7.04,
    w: 11.95,
    h: 0,
    line: { color: "e5e7eb", width: 1 },
  });
}

function buildDeck(slides, outFile) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "webapp-security-programming-handson";
  pptx.subject = "Web Application Security Programming Hands-on";
  pptx.title = path.basename(outFile, ".pptx");
  pptx.company = "koide55";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: "Aptos Display",
    bodyFontFace: "Aptos",
    lang: "en-US",
  };
  pptx.defineLayout({ name: "LAYOUT_WIDE", width: 13.333, height: 7.5 });

  const total = slides.length;
  slides.forEach((raw, index) => {
    const slide = pptx.addSlide();
    const parsed = parseSlide(raw);

    slide.background = { color: "ffffff" };
    slide.addShape(pptx.ShapeType.rect, {
      x: 0,
      y: 0,
      w: 0.22,
      h: 7.5,
      fill: { color: "0f766e" },
      line: { color: "0f766e" },
    });
    slide.addText("FOUNDATION", {
      x: 0.66,
      y: 0.36,
      w: 2.3,
      h: 0.18,
      fontFace: "Aptos",
      fontSize: 7,
      color: "0f766e",
      bold: true,
      margin: 0,
    });
    slide.addText(parsed.title, {
      x: 0.66,
      y: 0.67,
      w: 11.9,
      h: 0.48,
      fontFace: "Aptos Display",
      fontSize: parsed.title.length > 46 ? 23 : 26,
      color: "111827",
      bold: true,
      margin: 0,
      breakLine: false,
      fit: "shrink",
    });
    slide.addShape(pptx.ShapeType.line, {
      x: 0.66,
      y: 1.28,
      w: 11.95,
      h: 0,
      line: { color: "cbd5e1", width: 1 },
    });

    let y = 1.55;
    const contentX = 0.82;
    const contentW = 11.55;

    for (const segment of parsed.segments) {
      if (segment.type === "code") {
        const code = segment.text.replace(/\t/g, "    ").trimEnd();
        const lines = code.split(/\n/);
        const maxLen = Math.max(...lines.map((line) => line.length), 1);
        const fontSize = maxLen > 90 || lines.length > 14 ? 7.4 : maxLen > 70 || lines.length > 10 ? 8.4 : 9.4;
        const height = Math.min(4.55, Math.max(0.65, (lines.length * fontSize * 1.34) / 72 + 0.22));
        slide.addShape(pptx.ShapeType.roundRect, {
          x: contentX - 0.03,
          y,
          w: contentW,
          h: height,
          rectRadius: 0.06,
          fill: { color: "f3f4f6" },
          line: { color: "e5e7eb", width: 0.7 },
        });
        slide.addText(code, {
          x: contentX + 0.16,
          y: y + 0.18,
          w: contentW - 0.32,
          h: height - 0.26,
          fontFace: "Menlo",
          fontSize,
          color: "111827",
          margin: 0,
          fit: "shrink",
          breakLine: false,
        });
        y += height + 0.23;
      } else {
        const text = normalizeTextBlock(segment.text);
        if (!text) continue;
        const lines = text.split(/\n/).length;
        const fontSize = lines > 10 ? 13 : 14.8;
        const height = Math.min(5.2 - (y - 1.55), estimateHeight(text, fontSize, contentW));
        slide.addText(text, {
          x: contentX,
          y,
          w: contentW,
          h: Math.max(0.25, height),
          fontFace: "Aptos",
          fontSize,
          color: "1f2937",
          breakLine: false,
          fit: "shrink",
          margin: 0,
          valign: "top",
        });
        y += Math.max(0.25, height) + 0.18;
      }
    }

    addFooter(pptx, slide, index + 1, total);
  });

  fs.mkdirSync(path.dirname(outFile), { recursive: true });
  return pptx.writeFile({ fileName: outFile });
}

const markdown = fs.readFileSync(inputPath, "utf8");
const slides = splitSlides(markdown);
buildDeck(slides, outputPath).then(() => {
  console.log(outputPath);
  console.log(`slides=${slides.length}`);
});
