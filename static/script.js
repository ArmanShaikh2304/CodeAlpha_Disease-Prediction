const predictionForm = document.querySelector("#predictionForm");
const resetButton = document.querySelector("#resetButton");
const fillSampleButton = document.querySelector("#fillSampleButton");

if (predictionForm) {
    predictionForm.addEventListener("submit", (event) => {
        const inputs = predictionForm.querySelectorAll("input");
        let hasInvalidInput = false;

        // Simple browser-side validation before the form is sent to Flask.
        inputs.forEach((input) => {
            if (input.value.trim() === "" || Number.isNaN(Number(input.value))) {
                hasInvalidInput = true;
                input.classList.add("invalid");
            } else {
                input.classList.remove("invalid");
            }
        });

        if (hasInvalidInput) {
            event.preventDefault();
            alert("Please enter a valid number for every field.");
        }
    });
}

if (resetButton && predictionForm) {
    resetButton.addEventListener("click", () => {
        predictionForm.querySelectorAll("input").forEach((input) => {
            input.classList.remove("invalid");
        });
    });
}

if (fillSampleButton && predictionForm) {
    fillSampleButton.addEventListener("click", () => {
        predictionForm.querySelectorAll("input").forEach((input) => {
            input.value = input.dataset.sample;
            input.classList.remove("invalid");
        });
    });
}
