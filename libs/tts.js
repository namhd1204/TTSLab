import { KokoroTTS } from "kokoro-js";

const model_id = "onnx-community/Kokoro-82M-ONNX";
const tts = await KokoroTTS.from_pretrained(model_id, {
  dtype: "q8", // Options: "fp32", "fp16", "q8", "q4", "q4f16"
  device: "cpu",
});

// max

const text = `Once upon a time, a magical forest hidden behind the clouds was home to the **Tiger-Duck**. It had the orange stripes of a brave tiger and the yellow beak of a friendly duck. 

Every morning, it ran fast through the tall grass. Then, it jumped into the blue lake to swim. It didn't roar; it made a loud, funny "Quack-Roar!" All the other animals loved the Tiger-Duck because it was both strong and very kind.`;
const audio = await tts.generate(text, {
  // Use `tts.list_voices()` to list all available voices
  voice: "af_bella",
  speed: 0.8,
});
audio.save("output/tiger2.wav");
