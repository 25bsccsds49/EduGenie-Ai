// =====================================================
// EduGenie - Frontend JavaScript
// =====================================================


// =====================================================
// DOM ELEMENTS
// =====================================================

const task = document.getElementById("task");

const input = document.getElementById("input");

const submitBtn = document.getElementById("submitBtn");

const clearBtn = document.getElementById("clearBtn");

const copyBtn = document.getElementById("copyBtn");

const result = document.getElementById("result");

const resultTitle = document.getElementById("resultTitle");

const status = document.getElementById("status");

const hint = document.getElementById("hint");


// =====================================================
// TASK HINTS
// =====================================================

const hints = {

    qa:
        "Ask a specific academic or general knowledge question.",

    explain:
        "Enter a concept and EduGenie will explain it in beginner-friendly language.",

    quiz:
        "Paste a passage or topic. EduGenie generates 3 MCQs with 4 options each.",

    summarize:
        "Paste a long educational passage for a concise revision summary.",

    recommend:
        "Enter a topic such as SQL, Python, Biology, or Physics."

};


// =====================================================
// TASK CHANGE
// =====================================================

task.addEventListener("change", () => {

    hint.textContent =
        hints[task.value] || "";

});


// =====================================================
// CLEAR BUTTON
// =====================================================

clearBtn.addEventListener("click", () => {

    input.value = "";

    result.className = "result empty";

    result.innerHTML = `
        <div class="empty-state">

            <div class="orb">
                ✦
            </div>

            <p>
                Choose a task and enter
                your learning material.
            </p>

        </div>
    `;

    resultTitle.textContent =
        "Your learning response will appear here";

    status.textContent =
        "Ready";

});


// =====================================================
// COPY BUTTON
// =====================================================

copyBtn.addEventListener("click", async () => {

    const text = result.innerText.trim();

    if (!text) {

        status.textContent =
            "Nothing to copy";

        return;

    }

    try {

        await navigator.clipboard.writeText(text);

        status.textContent =
            "Copied";

        setTimeout(() => {

            status.textContent =
                "Ready";

        }, 1200);

    } catch (error) {

        status.textContent =
            "Copy failed";

        console.error(
            "Copy error:",
            error
        );

    }

});


// =====================================================
// RUN BUTTON
// =====================================================

submitBtn.addEventListener(
    "click",
    runTask
);


// =====================================================
// RUN TASK
// =====================================================

async function runTask() {

    const text =
        input.value.trim();


    // -------------------------------------------------
    // EMPTY INPUT CHECK
    // -------------------------------------------------

    if (!text) {

        status.textContent =
            "Enter some text first";

        input.focus();

        return;

    }


    // -------------------------------------------------
    // DISABLE BUTTON
    // -------------------------------------------------

    submitBtn.disabled =
        true;

    clearBtn.disabled =
        true;

    status.textContent =
        "Thinking…";


    // -------------------------------------------------
    // LOADING UI
    // -------------------------------------------------

    result.className =
        "result";

    result.textContent =
        "EduGenie is generating your response…";


    resultTitle.textContent =
        titleFor(task.value);


    try {

        // -------------------------------------------------
        // SEND REQUEST TO FASTAPI
        // -------------------------------------------------

        const response =
            await fetch(
                "/api/task",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        task:
                            task.value,

                        text:
                            text

                    })

                }
            );


        // -------------------------------------------------
        // READ RESPONSE
        // -------------------------------------------------

        const data =
            await response.json();


        // -------------------------------------------------
        // DEBUG
        // -------------------------------------------------

        console.log(
            "Response status:",
            response.status
        );

        console.log(
            "Backend response:",
            data
        );


        // -------------------------------------------------
        // ERROR RESPONSE
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "The request failed."
            );

        }


        // -------------------------------------------------
        // RENDER RESULT
        // -------------------------------------------------

        renderResult(
            task.value,
            data.result
        );


        status.textContent =
            "Complete";


    } catch (error) {

        console.error(
            "EduGenie error:",
            error
        );


        result.className =
            "result error";


        result.innerHTML = `
            <div class="error-message">

                <h3>
                    Something went wrong
                </h3>

                <p>
                    ${escapeHTML(error.message)}
                </p>

                <small>
                    Please check the FastAPI terminal
                    for more details.
                </small>

            </div>
        `;


        status.textContent =
            "Error";


    } finally {

        // -------------------------------------------------
        // ENABLE BUTTONS AGAIN
        // -------------------------------------------------

        submitBtn.disabled =
            false;

        clearBtn.disabled =
            false;

    }

}


// =====================================================
// RESULT TITLE
// =====================================================

function titleFor(value) {

    const titles = {

        qa:
            "Answer",

        explain:
            "Simple Explanation",

        quiz:
            "Practice Quiz",

        summarize:
            "Quick Summary",

        recommend:
            "Learning Path"

    };


    return (
        titles[value] ||
        "Learning Response"
    );

}


// =====================================================
// RENDER RESULT
// =====================================================

function renderResult(
    type,
    data
) {

    // -------------------------------------------------
    // CLEAR OLD RESULT
    // -------------------------------------------------

    result.className =
        "result";

    result.innerHTML =
        "";


    // =================================================
    // QUIZ RESULT
    // =================================================

    if (
        type === "quiz" &&
        data &&
        Array.isArray(data.questions)
    ) {

        const wrapper =
            document.createElement(
                "div"
            );


        wrapper.className =
            "quiz";


        data.questions.forEach(
            (q, index) => {

                const card =
                    document.createElement(
                        "section"
                    );


                card.className =
                    "quiz-question";


                // -----------------------------------------
                // QUESTION
                // -----------------------------------------

                const heading =
                    document.createElement(
                        "h3"
                    );


                heading.textContent =
                    `${index + 1}. ${q.question}`;


                card.appendChild(
                    heading
                );


                // -----------------------------------------
                // OPTIONS
                // -----------------------------------------

                if (
                    Array.isArray(q.options)
                ) {

                    q.options.forEach(
                        option => {

                            const button =
                                document.createElement(
                                    "button"
                                );


                            button.type =
                                "button";


                            button.className =
                                "quiz-option";


                            button.textContent =
                                option;


                            button.addEventListener(
                                "click",
                                () => {

                                    handleQuizAnswer(
                                        card,
                                        button,
                                        option,
                                        q
                                    );

                                }
                            );


                            card.appendChild(
                                button
                            );

                        }
                    );

                }


                // -----------------------------------------
                // ADD QUESTION CARD
                // -----------------------------------------

                wrapper.appendChild(
                    card
                );

            }
        );


        result.appendChild(
            wrapper
        );


        return;

    }


    // =================================================
    // NORMAL TEXT RESULT
    // =================================================

    if (
        typeof data === "string"
    ) {

        result.textContent =
            data;

        return;

    }


    // =================================================
    // OBJECT RESULT
    // =================================================

    if (
        data !== null &&
        typeof data === "object"
    ) {

        result.textContent =
            JSON.stringify(
                data,
                null,
                2
            );

        return;

    }


    // =================================================
    // FALLBACK
    // =================================================

    result.textContent =
        String(data);

}


// =====================================================
// QUIZ ANSWER HANDLER
// =====================================================

function handleQuizAnswer(
    card,
    selectedButton,
    selectedOption,
    question
) {

    // -------------------------------------------------
    // GET ALL OPTION BUTTONS
    // -------------------------------------------------

    const buttons =
        [
            ...card.querySelectorAll(
                ".quiz-option"
            )
        ];


    // -------------------------------------------------
    // PREVENT MULTIPLE ANSWERS
    // -------------------------------------------------

    buttons.forEach(
        button => {

            button.disabled =
                true;

        }
    );


    // -------------------------------------------------
    // CHECK ANSWER
    // -------------------------------------------------

    if (
        selectedOption ===
        question.correct_answer
    ) {

        selectedButton.classList.add(
            "correct"
        );

    } else {

        selectedButton.classList.add(
            "wrong"
        );


        // ---------------------------------------------
        // FIND CORRECT ANSWER BUTTON
        // ---------------------------------------------

        const correctButton =
            buttons.find(
                button =>
                    button.textContent ===
                    question.correct_answer
            );


        if (correctButton) {

            correctButton.classList.add(
                "correct"
            );

        }

    }


    // -------------------------------------------------
    // EXPLANATION
    // -------------------------------------------------

    const explanation =
        document.createElement(
            "div"
        );


    explanation.className =
        "quiz-explanation";


    const explanationText =
        question.explanation ||
        "No explanation was provided.";


    explanation.textContent =
        `Correct answer: ${question.correct_answer}. ${explanationText}`;


    card.appendChild(
        explanation
    );

}


// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHTML(value) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        String(value);


    return div.innerHTML;

}


// =====================================================
// INITIAL STATE
// =====================================================

hint.textContent =
    hints[task.value] || "";

status.textContent =
    "Ready";