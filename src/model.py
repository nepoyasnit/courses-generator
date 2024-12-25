from transformers import AutoModelForCausalLM, AutoTokenizer


class Model:
    def __init__(self, model_name: str, hf_token: str, model_dtype: str = "auto", device: str = "auto"):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=model_dtype,
            device_map=device,
            token=hf_token
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
