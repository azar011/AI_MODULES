
from openai import OpenAI
from dotenv import load_dotenv

import os
import json


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_capa(data):

    prompt = f"""
    Generate concise CAPA.

    Department: {data['department']}
    Checklist: {data['checklist_name']}
    Issue: {data['question']}
    Remarks: {data['remarks']}

    Return ONLY valid JSON:

    {{
      "corrective_action": "...",
      "root_cause": "...",
      "preventive_action": "..."
    }}
    """

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        return json.loads(content)
    
        # content = content.replace(
        #     "```json",
        #     ""
        # )

        # content = content.replace(
        #     "```",
        #     ""
        # )

        # content = content.strip()

        # return json.loads(content)

    except Exception as e:

        return {
            "error": f"OpenAI Error: {str(e)}"
        }       














# from openai import OpenAI

# from dotenv import load_dotenv

# import os


# load_dotenv()


# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )


# def generate_capa(data):

#     prompt = f""" 
#     Generate concise CAPA.
#     Department: {data['department']}
#     Checklist: {data['checklist_name']}
#     Issue: {data['question']}
#     Remarks: {data['remarks']}
#     Return:
#     - Corrective Action
#     - Root Cause
#     - Preventive Action
#     """

#     try:

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         )

#         return response.choices[0].message.content

#     except Exception as e:

#         return f"OpenAI Error: {str(e)}"

