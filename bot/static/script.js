// script.js

let historyList = [];
let isDarkMode = false;

// Verificar se estava em modo escuro ao recarregar
window.onload = function () {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
        isDarkMode = true;
    }
};

function sendQuestion() {
    const questionInput = document.getElementById("question");
    const userQuestion = questionInput.value.trim();
    if (userQuestion === "") return;

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userQuestion }),
    })
    .then(response => response.json())
    .then(data => {
        const answerDiv = document.getElementById("answer");
        answerDiv.innerHTML = `<strong>Cogni IA:</strong> ${data.answer}`;

        // Guardar no histórico
        historyList.push({ question: userQuestion, answer: data.answer });
        updateHistory();

        questionInput.value = "";
    })
    .catch(error => {
        console.error("Erro:", error);
    });
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    isDarkMode = !isDarkMode;
    localStorage.setItem("darkMode", isDarkMode);  // Salvar a preferência
}

function updateHistory() {
    const historyDiv = document.getElementById("history");
    historyDiv.innerHTML = "<h3>Histórico de Conversas</h3>";

    historyList.slice().reverse().forEach(item => {
        const entry = document.createElement("div");
        entry.classList.add("history-item");
        entry.innerHTML = `
            <div><strong>Você:</strong> ${item.question}</div>
            <div><strong>Cogni IA:</strong> ${item.answer}</div>
            <hr>
        `;
        historyDiv.appendChild(entry);
    });
}

function toggleHistory() {
    const historyDiv = document.getElementById("history");
    historyDiv.classList.toggle("visible");
}
