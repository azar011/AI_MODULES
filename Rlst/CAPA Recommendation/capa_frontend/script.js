const recommendBtn =
    document.getElementById("recommendBtn")

const acceptBtn =
    document.getElementById("acceptBtn")

const jsonInput =
    document.getElementById("jsonInput")

const sourceLabel =
    document.getElementById("sourceLabel")

const correctiveAction =
    document.getElementById("correctiveAction")

const rootCause =
    document.getElementById("rootCause")

const preventiveAction =
    document.getElementById("preventiveAction")


let currentEscalation = null
let originalRecommendation = null


// Disable Accept initially
acceptBtn.disabled = true


recommendBtn.addEventListener(
    "click",
    async () => {

        try {

            acceptBtn.disabled = false

            currentEscalation =
                JSON.parse(
                    jsonInput.value
                )

            sourceLabel.value =
                "Generating..."

            const response = await fetch(
                "http://127.0.0.1:8002/generate-capa",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(currentEscalation)
                }
            );

            const task = await response.json();

            const taskId = task.task_id;

            const interval = setInterval(async () => {

                const statusResponse = await fetch(
                    `http://127.0.0.1:8002/status/${taskId}`
                );

                const data = await statusResponse.json();

                if (data.status === "SUCCESS") {

                    clearInterval(interval);

                    const result = data.result;

                    if (result.error) {

                        sourceLabel.value = result.error;

                        correctiveAction.value = "";
                        rootCause.value = "";
                        preventiveAction.value = "";

                        acceptBtn.disabled = true;

                        return;
                    }

                    sourceLabel.value =
                        `${result.source} | Similarity: ${result.similarity_score}`;

                    correctiveAction.value =
                        result.corrective_action || "";

                    rootCause.value =
                        result.root_cause || "";

                    preventiveAction.value =
                        result.preventive_action || "";

                    originalRecommendation = {

                        source: result.source || "",

                        corrective_action:
                            result.corrective_action || "",

                        root_cause:
                            result.root_cause || "",

                        preventive_action:
                            result.preventive_action || ""
                    };

                    acceptBtn.disabled = false;
                }

                else if (data.status === "FAILURE") {

                    clearInterval(interval);

                    sourceLabel.value = "CAPA Generation Failed";

                    acceptBtn.disabled = true;

                    alert(data.error);
                }

            }, 1000);

            

        }
        catch (error) {

            alert(
                "Invalid JSON or Server Error\n\n" +
                error.message
            )

        }

    }
)


acceptBtn.addEventListener(
    "click",
    async () => {

        try {

            if (!currentEscalation) {

                alert(
                    "Generate recommendation first"
                )

                return
            }

            const payload = {

                ...currentEscalation,

                source:
                    originalRecommendation.source,

                original_corrective_action:
                    originalRecommendation.corrective_action,

                original_root_cause:
                    originalRecommendation.root_cause,

                original_preventive_action:
                    originalRecommendation.preventive_action,

                corrective_action:
                    correctiveAction.value,

                root_cause:
                    rootCause.value,

                preventive_action:
                    preventiveAction.value
            }

            const response =
                await fetch(
                    "http://127.0.0.1:8002/save-capa",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                )

            const result =
                await response.json()

            alert(
                result.message
            )

            acceptBtn.disabled = true

        }
        catch (error) {

            alert(
                "Save Failed\n\n" +
                error.message
            )

        }

    }
)


// Re-enable Accept when recommendation is edited

function enableAcceptButton() {

    if (currentEscalation) {

        acceptBtn.disabled = false

    }
}

correctiveAction.addEventListener(
    "input",
    enableAcceptButton
)

rootCause.addEventListener(
    "input",
    enableAcceptButton
)

preventiveAction.addEventListener(
    "input",
    enableAcceptButton
)