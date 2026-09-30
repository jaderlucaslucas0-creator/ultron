const $=s=>document.querySelector(s);
const key=()=>localStorage.getItem("ultron_api_key")||"";
$("#apiKey").value=key();
$("#apiKey").onchange=e=>localStorage.setItem("ultron_api_key",e.target.value.trim());
function headers(){const h={};if(key())h.Authorization="Bearer "+key();return h}
async function api(path,opt={}){
  opt.headers={...headers(),...(opt.headers||{})};
  const r=await fetch(path,opt);
  if(!r.ok){let m="Erro";try{m=(await r.json()).detail||m}catch{}throw Error(m)}
  return r.headers.get("content-type")?.includes("application/json")?r.json():r.blob()
}
document.querySelectorAll("aside button[data-panel]").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".view").forEach(v=>v.classList.remove("active"));
  $("#"+b.dataset.panel).classList.add("active");
  if(b.dataset.panel==="memory")loadMemory();
  if(b.dataset.panel==="skills")loadSkills();
  if(b.dataset.panel==="system")loadSystem();
  if(b.dataset.panel==="files")loadFiles();
  if(b.dataset.panel==="automations")loadAutomations();
});
let recorder,chunks=[];
$("#recordBtn").onclick=async()=>{
  if(recorder?.state==="recording"){recorder.stop();return}
  try{
    const stream=await navigator.mediaDevices.getUserMedia({audio:true});
    recorder=new MediaRecorder(stream);chunks=[];
    recorder.ondataavailable=e=>chunks.push(e.data);
    recorder.onstop=async()=>{
      stream.getTracks().forEach(t=>t.stop());$("#recordBtn").textContent="🎙️ FALAR";
      try{const fd=new FormData();fd.append("file",new Blob(chunks,{type:"audio/webm"}),"ultron.webm");const d=await api("/api/voice/transcribe",{method:"POST",body:fd});$("#message").value=d.text;$("#chatForm").requestSubmit()}
      catch(e){addMsg(e.message,"error")}
    };
    recorder.start();$("#recordBtn").textContent="⏹️ PARAR";
  }catch(e){addMsg("Não foi possível acessar o microfone.","error")}
};
$("#chatForm").onsubmit=async e=>{
  e.preventDefault();const i=$("#message"),t=i.value.trim();if(!t)return;addMsg(t,"user");i.value="";
  try{const d=await api("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:t})});addMsg(d.answer,"bot");speak(d.answer)}
  catch(e){addMsg(e.message,"error")}
};
async function speak(text){try{const blob=await api("/api/voice/speak",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text,voice:$("#voice").value,speed:Number($("#speed").value)})});const a=new Audio(URL.createObjectURL(blob));window.ultronAudio=a;a.onended=()=>URL.revokeObjectURL(a.src);await a.play()}catch(e){addMsg("Voz indisponível: "+e.message,"error")}}
$("#stopSpeak").onclick=()=>window.ultronAudio?.pause();
function addMsg(t,c){const d=document.createElement("div");d.className="msg "+c;d.textContent=t;$("#messages").appendChild(d);$("#messages").scrollTop=$("#messages").scrollHeight}
$("#researchForm").onsubmit=async e=>{e.preventDefault();const q=$("#researchInput").value.trim();if(!q)return;$("#researchResult").textContent="Pesquisando...";try{const d=await api("/api/research",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:q})});$("#researchResult").textContent=d.answer}catch(err){$("#researchResult").textContent=err.message}};
$("#visionForm").onsubmit=async e=>{e.preventDefault();const f=$("#visionFile").files[0];if(!f)return;$("#visionResult").textContent="Analisando imagem...";try{const fd=new FormData();fd.append("file",f);fd.append("prompt",$("#visionPrompt").value);const d=await api("/api/vision/analyze",{method:"POST",body:fd});$("#visionResult").textContent=d.answer}catch(err){$("#visionResult").textContent=err.message}};
$("#fileForm").onsubmit=async e=>{e.preventDefault();const f=$("#fileInput").files[0];if(!f)return;try{const fd=new FormData();fd.append("file",f);await api("/api/files",{method:"POST",body:fd});$("#fileInput").value="";loadFiles()}catch(err){alert(err.message)}};
async function loadFiles(){try{$("#fileList").innerHTML="";(await api("/api/files")).forEach(f=>{const d=document.createElement("div");d.className="item";d.innerHTML=`#${f.id} <a href="/api/files/${f.id}" target="_blank">${f.filename}</a> — ${f.size} bytes`;$("#fileList").appendChild(d)})}catch(e){$("#fileList").textContent=e.message}}
$("#automationForm").onsubmit=async e=>{e.preventDefault();try{await api("/api/automations",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:$("#automationName").value,schedule:$("#automationSchedule").value,enabled:true})});e.target.reset();loadAutomations()}catch(err){alert(err.message)}};
async function loadAutomations(){try{$("#automationList").innerHTML="";(await api("/api/automations")).forEach(a=>{const d=document.createElement("div");d.className="item";d.textContent="#"+a.id+" "+a.name+" — "+a.schedule+" — "+(a.enabled?"ATIVA":"PAUSADA");$("#automationList").appendChild(d)})}catch(e){$("#automationList").textContent=e.message}}
$("#memoryForm").onsubmit=async e=>{e.preventDefault();const i=$("#memoryInput");if(!i.value.trim())return;try{await api("/api/memory",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({content:i.value})});i.value="";loadMemory()}catch(e){alert(e.message)}};
async function loadMemory(){try{$("#memoryList").innerHTML="";(await api("/api/memory")).forEach(m=>{const d=document.createElement("div");d.className="item";d.textContent="#"+m.id+" "+m.content;$("#memoryList").appendChild(d)})}catch(e){$("#memoryList").textContent=e.message}}
async function loadSkills(){try{$("#skillList").innerHTML="";(await api("/api/skills")).forEach(s=>{const d=document.createElement("div");d.className="item";d.textContent=s.name+" — "+s.description;$("#skillList").appendChild(d)})}catch(e){$("#skillList").textContent=e.message}}
async function loadSystem(){try{$("#systemData").textContent=JSON.stringify(await api("/api/status"),null,2)}catch(e){$("#systemData").textContent=e.message}}
