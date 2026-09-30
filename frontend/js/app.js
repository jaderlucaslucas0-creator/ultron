const $ = (s) => document.querySelector(s);
const apiKey = () => localStorage.getItem("hermes_api_key") || "";

function headers() {
  const h = {};
  if (apiKey()) h.Authorization = "Bearer " + apiKey();
  return h;
}

async function api(path, options = {}) {
  options.headers = { ...headers(), ...(options.headers || {}) };
  const response = await fetch(path, options);
  if (!response.ok) {
    let message = "Erro " + response.status;
    try { message = (await response.json()).detail || message; } catch {}
    throw new Error(message);
  }
  return response.headers.get("content-type")?.includes("application/json")
    ? response.json() : response.blob();
}

function addMsg(text, type) {
  const el = document.createElement("div");
  el.className = "msg " + type;
  el.textContent = text;
  $("#messages").appendChild(el);
  $("#messages").scrollTop = $("#messages").scrollHeight;
}

document.querySelectorAll("aside button[data-panel]").forEach((button) => {
  button.onclick = () => {
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    $("#" + button.dataset.panel).classList.add("active");
    if (button.dataset.panel === "memory") loadMemory();
    if (button.dataset.panel === "skills") loadSkills();
    if (button.dataset.panel === "files") loadFiles();
    if (button.dataset.panel === "automations") loadAutomations();
    if (button.dataset.panel === "system") loadSystem();
  };
});

$("#chatForm").onsubmit = async (event) => {
  event.preventDefault();
  const input = $("#message");
  const text = input.value.trim();
  if (!text) return;
  addMsg(text, "user");
  input.value = "";
  try {
    const data = await api("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: text})
    });
    addMsg(data.answer, "bot");
    speak(data.answer);
  } catch (error) {
    addMsg(error.message, "error");
  }
};

let recognition = null;
$("#recordBtn").onclick = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    addMsg("Seu navegador não oferece reconhecimento de voz. Use Chrome ou Edge.", "error");
    return;
  }
  if (recognition) {
    recognition.stop();
    recognition = null;
    $("#recordBtn").textContent = "🎙️ FALAR";
    return;
  }
  recognition = new SpeechRecognition();
  recognition.lang = "pt-BR";
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.onstart = () => $("#recordBtn").textContent = "⏹️ PARAR";
  recognition.onresult = (event) => {
    $("#message").value = event.results[0][0].transcript;
    $("#chatForm").requestSubmit();
  };
  recognition.onerror = () => addMsg("Não consegui reconhecer sua voz.", "error");
  recognition.onend = () => {
    recognition = null;
    $("#recordBtn").textContent = "🎙️ FALAR";
  };
  recognition.start();
};

function speak(text) {
  if (!("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "pt-BR";
  utterance.rate = Number($("#speed").value);
  const voices = speechSynthesis.getVoices();
  const voice = voices.find(v => v.lang?.toLowerCase() === "pt-br") ||
                voices.find(v => v.lang?.toLowerCase().startsWith("pt"));
  if (voice) utterance.voice = voice;
  speechSynthesis.speak(utterance);
}

$("#stopSpeak").onclick = () => speechSynthesis?.cancel();

$("#researchForm").onsubmit = async (event) => {
  event.preventDefault();
  $("#researchResult").textContent = "Pesquisando...";
  try {
    const data = await api("/api/research", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({query: $("#researchInput").value.trim()})
    });
    $("#researchResult").textContent = data.answer;
  } catch (error) { $("#researchResult").textContent = error.message; }
};

$("#memoryForm").onsubmit = async (event) => {
  event.preventDefault();
  const input = $("#memoryInput");
  if (!input.value.trim()) return;
  try {
    await api("/api/memory", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({content: input.value.trim()})
    });
    input.value = "";
    loadMemory();
  } catch (error) { alert(error.message); }
};

async function loadMemory() {
  try {
    $("#memoryList").innerHTML = "";
    (await api("/api/memory")).forEach(m => {
      const el = document.createElement("div");
      el.className = "item";
      el.textContent = "#" + m.id + " — " + m.content;
      $("#memoryList").appendChild(el);
    });
  } catch (error) { $("#memoryList").textContent = error.message; }
}

async function loadSkills() {
  try {
    $("#skillList").innerHTML = "";
    (await api("/api/skills")).forEach(s => {
      const el = document.createElement("div");
      el.className = "item";
      el.textContent = s.name + " — " + s.description;
      $("#skillList").appendChild(el);
    });
  } catch (error) { $("#skillList").textContent = error.message; }
}

$("#fileForm").onsubmit = async (event) => {
  event.preventDefault();
  const file = $("#fileInput").files[0];
  if (!file) return;
  try {
    const form = new FormData();
    form.append("file", file);
    await api("/api/files", {method: "POST", body: form});
    $("#fileInput").value = "";
    loadFiles();
  } catch (error) { alert(error.message); }
};

async function loadFiles() {
  try {
    $("#fileList").innerHTML = "";
    (await api("/api/files")).forEach(f => {
      const el = document.createElement("div");
      el.className = "item";
      el.textContent = "#" + f.id + " — ";
      const link = document.createElement("a");
      link.href = "/api/files/" + f.id;
      link.target = "_blank";
      link.textContent = f.filename;
      el.appendChild(link);
      $("#fileList").appendChild(el);
    });
  } catch (error) { $("#fileList").textContent = error.message; }
}

$("#automationForm").onsubmit = async (event) => {
  event.preventDefault();
  try {
    await api("/api/automations", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: $("#automationName").value,
        schedule: $("#automationSchedule").value,
        enabled: true
      })
    });
    event.target.reset();
    loadAutomations();
  } catch (error) { alert(error.message); }
};

async function loadAutomations() {
  try {
    $("#automationList").innerHTML = "";
    (await api("/api/automations")).forEach(a => {
      const el = document.createElement("div");
      el.className = "item";
      el.textContent = "#" + a.id + " " + a.name + " — " + a.schedule + " — " + (a.enabled ? "ATIVA" : "PAUSADA");
      $("#automationList").appendChild(el);
    });
  } catch (error) { $("#automationList").textContent = error.message; }
}

async function loadSystem() {
  try {
    $("#systemData").textContent = JSON.stringify(await api("/api/status"), null, 2);
  } catch (error) { $("#systemData").textContent = error.message; }
}
