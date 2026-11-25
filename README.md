# Assistente virtual por voz

Projeto do desafio **Conversando por Voz Com o ChatGPT Utilizando Whisper (OpenAI) e Python**, da DIO. O assistente grava uma pergunta em português, usa o Whisper para transcrevê-la, gera uma resposta com GPT-4o mini e usa gTTS para salvar a resposta falada em MP3. Cada execução processa uma pergunta.

## Como executar

No PowerShell, na pasta do projeto, com Python 3.10 ou superior:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
$env:OPENAI_API_KEY = "SUA_CHAVE_DA_OPENAI"
.\.venv\Scripts\python assistente.py
```

Pressione Enter e faça uma pergunta, como “O que é aprendizado de máquina?”. O terminal mostra a transcrição e a resposta. Abra `resposta.mp3` para ouvir.

Com um áudio já gravado, use `--audio pergunta.wav`. Para uma gravação mais longa, use `--segundos 10`. Se o projeto da API não tiver acesso ao Whisper hospedado (`whisper-1`), execute com `--modelo-transcricao gpt-4o-mini-transcribe`.

O assistente requer internet e uma chave da API da OpenAI com acesso aos modelos escolhidos. O áudio da pergunta é enviado à OpenAI e o texto da resposta é enviado ao serviço usado pelo gTTS. Mantenha a chave fora do repositório.
