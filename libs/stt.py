import os
from dotenv import load_dotenv

load_dotenv()

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from rainbow_print import rprint



# import os
# os.environ["HF_TOKEN"] = "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" # Thay bằng token của bạn
os.environ["HF_TOKEN"] = os.getenv('HF_TOKEN')

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v3"

rprint.info('loading model...')
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, 
    dtype=torch_dtype, 
    # torch_dtype=torch_dtype, 
    low_cpu_mem_usage=True, 
    use_safetensors=True,
    # clean_up_tokenization_spaces=False
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
    # max_new_tokens=128,
    dtype=torch_dtype,
    # torch_dtype=torch_dtype,
    device=device,
    stride_length_s=5
)

# rprint.info('loading dataset...')
# dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
# sample = dataset[0]["audio"]
# # <class 'datasets.features._torchcodec.AudioDecoder'>
# rprint.info(str(type(sample)))

result = pipe('output/tiger.wav', generate_kwargs={"language": "english"})
rprint.info("Transcription result:")
rprint.info(result["text"])
