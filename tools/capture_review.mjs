#!/usr/bin/env node
/** Capture portfolio index at /portfolio/ base path — loopback only. */
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(here, "..", "site");
const reviewRoot = fs.mkdtempSync(path.join(os.tmpdir(), "portfolio-review-"));
const mount = path.join(reviewRoot, "portfolio");
fs.cpSync(siteRoot, mount, { recursive: true });
const server = spawn("python", ["-m", "http.server", "8792", "--directory", reviewRoot], {
  stdio: "ignore",
});
const ORIGIN = "http://127.0.0.1:8792";
const outDir = path.join(siteRoot, "docs", "review");

function browser() {
  for (const p of [
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ]) {
    if (fs.existsSync(p)) return p;
  }
  return "msedge";
}

async function main() {
  await new Promise((r) => setTimeout(r, 800));
  const port = 9900 + Math.floor(Math.random() * 100);
  const userData = fs.mkdtempSync(path.join(os.tmpdir(), "portfolio-cap-"));
  const proc = spawn(
    browser(),
    [
      "--headless=new",
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${userData}`,
      "--disable-extensions",
      "--no-first-run",
      "about:blank",
    ],
    { stdio: "ignore" },
  );
  try {
    await new Promise((r) => setTimeout(r, 700));
    const tabs = await new Promise((res, rej) => {
      http
        .get(`http://127.0.0.1:${port}/json/list`, (r) => {
          let d = "";
          r.on("data", (c) => (d += c));
          r.on("end", () => res(JSON.parse(d)));
        })
        .on("error", rej);
    });
    const pageTab =
      tabs.find((t) => t.type === "page" && !String(t.url).startsWith("chrome-extension:")) ||
      tabs[0];
    const ws = new WebSocket(pageTab.webSocketDebuggerUrl);
    await new Promise((res, rej) => {
      ws.addEventListener("open", res);
      ws.addEventListener("error", rej);
    });
    let id = 0;
    const pending = new Map();
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && pending.has(msg.id)) pending.get(msg.id)(msg);
    });
    const send = (method, params = {}) =>
      new Promise((resolve, reject) => {
        const mid = ++id;
        pending.set(mid, (msg) =>
          msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result),
        );
        ws.send(JSON.stringify({ id: mid, method, params }));
      });
    await send("Page.enable");
    const shot = async (name, mobile) => {
      await send("Emulation.setDeviceMetricsOverride", {
        width: mobile ? 390 : 1280,
        height: mobile ? 844 : 900,
        deviceScaleFactor: 1,
        mobile,
      });
      await send("Page.navigate", { url: `${ORIGIN}/portfolio/` });
      await new Promise((r) => setTimeout(r, 900));
      const data = (await send("Page.captureScreenshot", { format: "png", fromSurface: true })).data;
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, name), Buffer.from(data, "base64"));
    };
    await shot("index-desktop-portfolio-base.png", false);
    await shot("index-mobile-portfolio-base.png", true);
    ws.close();
    console.log("CAPTURE_OK " + outDir);
  } finally {
    proc.kill();
    try {
      fs.rmSync(userData, { recursive: true, force: true });
    } catch {
      /* ignore */
    }
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => {
    server.kill();
    try {
      fs.rmSync(reviewRoot, { recursive: true, force: true });
    } catch {
      /* ignore */
    }
  });
