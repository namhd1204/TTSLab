import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from rainbow_print import rprint


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v3"

rprint.info('loading model...')
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, 
    dtype=torch_dtype, 
    # torch_dtype=torch_dtype, 
    low_cpu_mem_usage=True, 
    use_safetensors=True
)

rprint.info('loading model to device...')
model.to(device)

rprint.info('loading processor...')
processor = AutoProcessor.from_pretrained(model_id)

rprint.info('creating pipeline...')
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    dtype=torch_dtype,
    # torch_dtype=torch_dtype,
    device=device,
)

rprint.info('loading dataset...')
dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = dataset[0]["audio"]

rprint.info(str(type(sample)))

result = pipe(sample)
rprint.info("Transcription result:")
rprint.info(result["text"])
