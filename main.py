from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LM_API_URL = "http://localhost:1234/v1/chat/completions"

# 風險與成長潛力排序權重
risk_order = {"Low": 0, "Moderate": 1, "High": 2}
growth_order = {"High": 0, "Medium": 1, "Low": 2}


@app.post("/chat")
async def chat_with_lmstudio(req: Request):
    body = await req.json()
    response = requests.post(LM_API_URL, json=body)
    result = response.json()

    content = result["choices"][0]["message"]["content"]

    # 拆分每個推薦區塊（**1.、**2. 開頭）
    recommendations = re.findall(r'(\*\*\d+\..*?)(?=\*\*\d+\.|\Z)', content, re.DOTALL)

    def extract_fields(text):
        risk_match = re.search(r"Risk Level:\s*(.+)", text)
        risk = risk_match.group(1).strip() if risk_match else "Moderate"

        growth_match = re.search(r"Growth Potential:\s*(.+)", text)
        growth = growth_match.group(1).strip() if growth_match else "Medium"

        industry_match = re.search(r"Industry:\s*(.+)", text)
        industry = industry_match.group(1).strip() if industry_match else ""

        return risk, growth, industry

    def sort_key(text):
        risk, growth, industry = extract_fields(text)
        return (
            risk_order.get(risk, 1),
            growth_order.get(growth, 1),
            industry.lower()
        )

    sorted_recommendations = sorted(recommendations, key=sort_key)

    disclaimer_match = re.search(r"(\*\*Disclaimer:.*)", content, re.DOTALL)
    disclaimer_text = disclaimer_match.group(1) if disclaimer_match else ""

    # 將換行符號改為 <br>，讓前端能正確顯示
    formatted_recommendations = [
        "<br><br>" + rec.replace("\n", "<br>") for rec in sorted_recommendations
    ]

    final_content = "".join(formatted_recommendations)
    if disclaimer_text:
        final_content += "<br><br>" + disclaimer_text.replace("\n", "<br>")

    result["choices"][0]["message"]["content"] = final_content
    return result
