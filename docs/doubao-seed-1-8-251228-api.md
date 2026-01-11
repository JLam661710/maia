curl https://ark.cn-beijing.volces.com/api/v3/responses \
-H "Authorization: Bearer a10addaa-4bf9-43f2-a19c-f8603eafd38e" \
-H 'Content-Type: application/json' \
-d '{
    "model": "doubao-seed-1-8-251228",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png"
                },
                {
                    "type": "input_text",
                    "text": "你看见了什么？"
                }
            ]
        }
    ]
}'