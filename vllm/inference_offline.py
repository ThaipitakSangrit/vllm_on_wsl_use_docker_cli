from vllm import LLM, SamplingParams
from PIL import Image

def main():
    llm = LLM(
        model="Qwen/Qwen2.5-VL-7B-Instruct",
        max_model_len=8192,
        limit_mm_per_prompt={"image": 1},  # จำกัด 1 ภาพต่อ prompt
    )

    # โหลดภาพจากไฟล์
    image = Image.open("sample.jpg")

    prompt = (
        "<|im_start|>user\n<|vision_start|><|image_pad|><|vision_end|>"
        "อ่านข้อความทั้งหมดในภาพนี้ให้หน่อย<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    sampling_params = SamplingParams(temperature=0.0, max_tokens=512)

    outputs = llm.generate(
        {
            "prompt": prompt,
            "multi_modal_data": {"image": image},
        },
        sampling_params,
    )

    print(outputs[0].outputs[0].text)

if __name__ == "__main__":
    main()