let questionsNumber = -1;

function addQuestion(divId) {
    questionsNumber++;

    const div = document.getElementById(divId);

    const questionDiv = document.createElement("div");
    questionDiv.classList.add("bg-white", "p-4", "rounded-lg", "shadow-md", "mb-4");

    const questionHeader = document.createElement('div');
    questionHeader.classList.add("flex", "items-center", "gap-2", "mb-4");
    
    const questionNumber = document.createElement('span');
    questionNumber.classList.add("text-xl", "font-bold", "text-gray-800");
    questionNumber.textContent = `Question #${questionsNumber + 2}`;

    questionHeader.appendChild(questionNumber);
    questionDiv.appendChild(questionHeader);

    const questionInput = document.createElement('input');
    questionInput.type = 'text';
    questionInput.name = `questions[${questionsNumber}]`;
    questionInput.placeholder = 'Enter question text...';
    questionInput.classList.add("w-full", "p-2", "border", "border-gray-300", "rounded", "mb-4");
    questionDiv.appendChild(questionInput);

    const answerDiv = document.createElement("div");
    answerDiv.classList.add("grid", "grid-cols-2", "gap-4");

    const answerLabel = document.createElement('p');
    answerLabel.textContent = 'Answers:';
    answerLabel.classList.add("text-lg", "font-semibold", "text-gray-800", "col-span-2");
    answerDiv.appendChild(answerLabel);

    for (let i = 0; i < 4; i++) {
        const answerContainer = document.createElement('div');
        answerContainer.classList.add("flex", "items-center", "gap-2");

        const answerInput = document.createElement('input');
        answerInput.type = 'text';
        answerInput.name = `answers[${questionsNumber}][${i}]`;
        answerInput.placeholder = `Answer ${i + 1}...`;
        answerInput.classList.add("flex-1", "p-2", "border", "border-gray-300", "rounded");

        const correctCheckbox = document.createElement('input');
        correctCheckbox.type = 'checkbox';
        correctCheckbox.name = `correct_answers[${questionsNumber}]`;
        correctCheckbox.value = i;
        correctCheckbox.classList.add("w-5", "h-5", "accent-green-500");

        const checkboxLabel = document.createElement('span');
        checkboxLabel.textContent = 'Correct';
        checkboxLabel.classList.add("text-sm", "text-gray-600");

        answerContainer.appendChild(answerInput);
        answerContainer.appendChild(correctCheckbox);
        answerContainer.appendChild(checkboxLabel);
        answerDiv.appendChild(answerContainer);
    }

    questionDiv.appendChild(answerDiv);
    div.appendChild(questionDiv);
}

document.getElementById("question_form_main").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    let formBody = {
        title: null,
        description: null,
        answers: [],
        correctAnswers: [],
        questions: [],
        csrfmiddlewaretoken: formData.get('csrfmiddlewaretoken')
    }

    formBody.title = formData.get("title");
    formBody.description = formData.get("description");
    questions = []
    for (let i = 0; i <= questionsNumber; i++) {
        answers = []
        questions.push(formData.get(`questions[${i}]`))
        for (let j = 0; j < 4; j++) {
            answers.push(formData.get(`answers[${i}][${j}]`));
        }

        formBody.answers.push(answers);
    }
    formBody.questions = questions;

    for (let i = 0; i <= questionsNumber; i++) {
        correctAnswers = formData.getAll(`correct_answers[${i}]`)
        
        formBody.correctAnswers.push(correctAnswers);
    }

    fetch("/create-quiz/", {
        method: "POST",
        headers: {
           'Content-Type': 'application/json',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'), 
        },
        body: JSON.stringify(formBody)
    }).then(response => {
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert("Wystąpił błąd");
        }
    });
});
