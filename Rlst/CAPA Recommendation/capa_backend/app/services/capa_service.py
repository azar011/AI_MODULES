import json

from app.services.embedding_service import create_embedding

from app.services.paraphrase_service import paraphrase_text

from app.services.qdrant_service import (
    add_case,
    search_case,
    client,
    COLLECTION_NAME
)

from app.services.llm_service import generate_capa


SIMILARITY_THRESHOLD = 0.80


# LOAD HISTORICAL DATA ONLY ONCE
collection_info = client.get_collection(COLLECTION_NAME)


if collection_info.points_count == 0:

    with open("app/data/escalations.json", "r") as file:

        historical_cases = json.load(file)

    for item in historical_cases:

        combined_text = f"""
        {item['department']}
        {item['checklist_name']}
        {item['question']}
        {item['remarks']}
        """

        embedding = create_embedding(combined_text)

        add_case(embedding, item)


# MAIN FUNCTION
def process_escalation(data):

    combined_text = f"""
    {data['department']}
    {data['checklist_name']}
    {data['question']}
    {data['remarks']}
    """

    query_embedding = create_embedding(combined_text)


    # SEARCH BEST MATCH
    similar_cases = search_case(
        query_embedding,
        top_k=1
    )


    # HISTORICAL MATCH
    if len(similar_cases) > 0:

        best_case = similar_cases[0]

        similarity_score = best_case["score"]


        if similarity_score >= SIMILARITY_THRESHOLD:

            return {
                "source": "historical_case",
                "similarity_score": similarity_score,

                "corrective_action":
                    paraphrase_text(
                        best_case["corrective_action"]
                    ),

                "root_cause":
                    paraphrase_text(
                        best_case["root_cause"]
                    ),

                "preventive_action":
                    paraphrase_text(
                        best_case["preventive_action"]
                    )
            }


    # GENERATE AI CAPA
    ai_response = generate_capa(data)


    # OPENAI ERROR
    # if isinstance(ai_response, str):

    #     if ai_response.startswith("OpenAI Error"):

    #         return {
    #             "source": "openai_error",
    #             "error": ai_response
    #         }

    if isinstance(ai_response, dict) and "error" in ai_response:

        return {
            "source": "openai_error",
            "error": ai_response["error"]
        }


    # INVALID RESPONSE
    if not isinstance(ai_response, dict):

        return {
            "source": "invalid_ai_response",
            "error": "AI did not return proper CAPA format"
        }


    required_fields = [
        "corrective_action",
        "root_cause",
        "preventive_action"
    ]


    # CHECK ALL FIELDS EXIST
    for field in required_fields:

        if field not in ai_response:

            return {
                "source": "invalid_ai_response",
                "error": f"Missing field: {field}"
            }


        if not ai_response[field]:

            return {
                "source": "invalid_ai_response",
                "error": f"Empty value in: {field}"
            }


    # STORE ONLY VALID CAPA
    


    return {
        "source": "ai_generated",
        "similarity_score": 0,
        "corrective_action": ai_response["corrective_action"],
        "root_cause": ai_response["root_cause"],
        "preventive_action": ai_response["preventive_action"]
    }


    