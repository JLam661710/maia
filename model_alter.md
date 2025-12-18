以下大模型接口均来自火山引擎-火山方舟
api key 已经自动填入

# 1. 访谈专员: 
# 拥有顶级的对话能力和情商，适合作为直接面向用户的接口
MODEL_INTERVIEWER=doubao-1-5-pro-32k-250115

接口示例：
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a10addaa-4bf9-43f2-a19c-f8603eafd38e" \
  -d '{
    "model": "doubao-1-5-pro-32k-250115",
    "messages": [
      {"role": "system","content": "你是人工智能助手."},
      {"role": "user","content": "你好"}
    ]
  }'

# 2. 后台分析师: 
# Google 最新的思维链模型，具备深度推理能力，适合处理复杂的 JSON 状态逻辑
MODEL_ANALYST=deepseek-v3-2-251201

接口示例：
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a10addaa-4bf9-43f2-a19c-f8603eafd38e" \
  -d '{
    "model": "deepseek-v3-2-251201",
    "messages": [
      {"role": "system","content": "你是人工智能助手."},
      {"role": "user","content": "你好"}
    ]
  }'

# 3. 解决方案架构师: 
# 拥有惊人的上下文窗口，能轻松吃透整个项目的几百轮对话历史，生成详尽文档
MODEL_ARCHITECT=doubao-seed-1-8-251215

接口示例：

curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a10addaa-4bf9-43f2-a19c-f8603eafd38e" \
  -d $'{
    "model": "doubao-seed-1-8-251215",
    "messages": [
        {
            "content": [
                {
                    "image_url": {
                        "url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
                    },
                    "type": "image_url"
                },
                {
                    "text": "图片主要讲了什么?",
                    "type": "text"
                }
            ],
            "role": "user"
        }
    ]
}'

# 4. 认知压缩器 (Summary Agent): 
# 负责长对话的摘要提取，需要极高的处理速度和极低的成本
MODEL_SUMMARY=doubao-seed-1-6-flash-250828

接口示例：

curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a10addaa-4bf9-43f2-a19c-f8603eafd38e" \
  -d $'{
    "model": "doubao-seed-1-6-flash-250828",
    "messages": [
        {
            "content": [
                {
                    "image_url": {
                        "url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
                    },
                    "type": "image_url"
                },
                {
                    "text": "图片主要讲了什么?",
                    "type": "text"
                }
            ],
            "role": "user"
        }
    ]
}'
