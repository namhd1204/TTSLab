import { pipeline } from "@xenova/transformers";
import wavefile from "wavefile";
import axios from "axios"; // Để tải file từ URL
import path from "path";
import fs from "fs";

const transcriber = await pipeline(
  "automatic-speech-recognition",
  //   "onnx-community/whisper-large-v3-turbo", // Model hỗ trợ tiếng Việt
  "distil-whisper/distil-large-v3",
);
// Đường dẫn tới file wav trên máy bạn
const filePath = path.resolve("output/tiger.wav");

// 1. Đọc file từ ổ cứng vào Buffer
const buffer = fs.readFileSync(filePath);

// 2. Giải mã file WAV bằng wavefile
const wav = new wavefile.WaveFile(buffer);

// 3. Chuyển đổi định dạng để model có thể hiểu được:
// Whisper yêu cầu 16kHz, Mono (1 kênh), và Float32
wav.toBitDepth("32f");
wav.toSampleRate(16000);

let audioData = wav.getSamples();

// Nếu là file Stereo (2 kênh), chúng ta cần gộp thành Mono
if (Array.isArray(audioData)) {
  const monoData = new Float32Array(audioData[0].length);
  for (let i = 0; i < audioData[0].length; ++i) {
    let sum = 0;
    for (let j = 0; j < audioData.length; ++j) {
      sum += audioData[j][i];
    }
    monoData[i] = sum / audioData.length;
  }
  audioData = monoData;
}

// 4. Chạy nhận diện
console.log("Đang xử lý...");
const output = await transcriber(audioData, {
  language: "vietnamese",
  task: "transcribe",
});

console.log("Kết quả:", output.text);
