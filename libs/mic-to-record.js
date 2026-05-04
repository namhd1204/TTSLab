import record from "node-record-lpcm16";
import fs from "fs";
import path from "path";

// Enable debug logging
const debug = process.env.DEBUG === "record";

const recordingDuration = 1000 * 10;
const audioFile = path.join("output", "recording.wav");

// Ensure output directory exists
if (!fs.existsSync("output")) {
  fs.mkdirSync("output", { recursive: true });
}

if (debug) console.log("[DEBUG] DEBUG mode enabled");
console.log("Starting recording... speak into your microphone");
console.log(`Recording will stop after ${recordingDuration / 1000} seconds`);

const file = fs.createWriteStream(audioFile);

const recording = record.record({
  sampleRateHertz: 16000,
  threshold: 0,
  silence: "1.0", // Stop after 1 second of silence
  keepSilence: true,
  recordProgram: "rec", // Use 'rec' on Linux/macOS or 'sox' if available
});

if (debug) {
  recording.stream().on("data", (chunk) => {
    console.log(`[DEBUG] Recording chunk: ${chunk.length} bytes`);
  });
  recording.stream().on("error", (err) => {
    console.error(`[DEBUG] Stream error: ${err.message}`);
  });
}

recording.stream().pipe(file);

recording.start();
if (debug) console.log("[DEBUG] Recording started");

setTimeout(() => {
  recording.stop();
  if (debug) console.log("[DEBUG] Recording stopped");
  console.log(`Recording saved to ${audioFile}`);
}, recordingDuration);
