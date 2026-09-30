from app.services.desktop import desktop

async def desktop_agent(message: str) -> str:
    text = message.strip()
    lower = text.lower()

    if lower.startswith(("abra ", "abrir ")):
        target = text.split(" ", 1)[1].strip()
        aliases = {"bloco de notas":"notepad", "calculadora":"calculator", "paint":"paint", "explorador":"explorer"}
        key = aliases.get(target.lower(), target.lower())
        if key in {"notepad","calculator","paint","explorer"}:
            result = await desktop.command("open_app", key)
            return "Aplicativo aberto." if result.get("ok") else f"Não consegui abrir: {result.get('message','erro')}."
        if target.startswith(("http://","https://")):
            result = await desktop.command("open_url", target)
            return "Site aberto." if result.get("ok") else f"Não consegui abrir: {result.get('message','erro')}."
        return "Posso abrir bloco de notas, calculadora, Paint, explorador ou uma URL."

    if lower.startswith("digite "):
        result = await desktop.command("type_text", text[7:])
        return "Texto digitado." if result.get("ok") else f"Não consegui digitar: {result.get('message','erro')}."

    if lower.startswith(("pressione ", "atalho ")):
        hotkey = text.split(" ", 1)[1].strip()
        result = await desktop.command("hotkey", hotkey)
        return "Atalho executado." if result.get("ok") else f"Não consegui executar: {result.get('message','erro')}."

    return "Comando não reconhecido. Tente: 'abra a calculadora', 'abra https://...' ou 'digite olá'."
