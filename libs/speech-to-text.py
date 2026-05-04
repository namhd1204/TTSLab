import os
from dotenv import load_dotenv

load_dotenv()

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, GenerationConfig
from rainbow_print import rprint

os.environ["HF_TOKEN"] = os.getenv('HF_TOKEN')

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v3"

rprint.info('loading model...')
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, 
    dtype=torch_dtype, 
    low_cpu_mem_usage=True, 
    use_safetensors=True,
    # token=os.getenv("HF_TOKEN")
)

rprint.info('loading model to device...')
model.to(device)

rprint.info('loading processor...')
processor = AutoProcessor.from_pretrained(
    model_id, 
    # token=os.getenv("HF_TOKEN"),
    clean_up_tokenization_spaces=False
)

rprint.info('creating pipeline...')
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    dtype=torch_dtype,
    device=device,
    stride_length_s=5,
    generate_kwargs={
        "language": "english",
    }
)

gen_config = GenerationConfig.from_pretrained(model_id)
gen_config.update(
    language="english",
    task="transcribe",
)

result = pipe('output/recording.wav', 
    generate_kwargs={"generation_config": gen_config}
)
rprint.info(result["text"])
