import argparse
import os
import tempfile
import wave
from pathlib import Path


def gravar_audio(destino, segundos):
    import sounddevice as sd

    taxa = 16000
    with sd.RawInputStream(samplerate=taxa, channels=1, dtype="int16") as microfone:
        print(f"Gravando por {segundos} segundos. Pode falar!", flush=True)
        amostras, houve_perda = microfone.read(taxa * segundos)

    if houve_perda:
        raise RuntimeError("A gravação perdeu amostras. Tente gravar novamente.")

    with wave.open(str(destino), "wb") as arquivo:
        arquivo.setparams((1, 2, taxa, 0, "NONE", "not compressed"))
        arquivo.writeframes(amostras)


def responder(client, caminho_audio, modelo_transcricao):
    with caminho_audio.open("rb") as arquivo:
        transcricao = client.audio.transcriptions.create(
            model=modelo_transcricao, file=arquivo, language="pt"
        )

    pergunta = transcricao.text.strip()
    if not pergunta:
        raise ValueError("Nenhuma fala foi reconhecida. Tente gravar novamente.")
    print(f"Você: {pergunta}")

    resposta = client.responses.create(
        model="gpt-4o-mini",
        instructions="Responda em português brasileiro, em até três frases curtas, sem Markdown.",
        input=pergunta,
        store=False,
    ).output_text.strip()
    if not resposta:
        raise ValueError("A API não retornou uma resposta em texto.")
    return resposta


def main():
    parser = argparse.ArgumentParser(description="Assistente de voz em português")
    parser.add_argument("--audio", type=Path, help="Arquivo de entrada WAV, MP3 ou M4A")
    parser.add_argument("--segundos", type=int, default=5, help="Duração da gravação (1–30 s)")
    parser.add_argument("--saida", type=Path, default=Path("resposta.mp3"))
    parser.add_argument("--modelo-transcricao", default="whisper-1")
    args = parser.parse_args()
    if args.audio is None and not 1 <= args.segundos <= 30:
        parser.error("--segundos deve estar entre 1 e 30.")
    if args.audio and not args.audio.is_file():
        parser.error(f"Arquivo de áudio não encontrado: {args.audio}")
    if args.audio and args.audio.resolve() == args.saida.resolve():
        parser.error("O arquivo de saída deve ser diferente do áudio de entrada.")
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        parser.error("Defina a variável de ambiente OPENAI_API_KEY antes de executar.")

    from gtts import gTTS
    from openai import OpenAI

    try:
        with OpenAI(timeout=45.0) as client, tempfile.TemporaryDirectory() as pasta:
            caminho_audio = args.audio
            if caminho_audio is None:
                caminho_audio = Path(pasta) / "pergunta.wav"
                input("Pressione Enter para iniciar a gravação.")
                gravar_audio(caminho_audio, args.segundos)

            resposta = responder(client, caminho_audio, args.modelo_transcricao)
            print(f"Assistente: {resposta}")
            gTTS(text=resposta, lang="pt", tld="com.br", timeout=20).save(str(args.saida))
    except Exception as erro:
        parser.exit(1, f"Falha ao executar o assistente ({type(erro).__name__}): {erro}\n")

    print(f"Abra o MP3 para ouvir a resposta: {args.saida.resolve()}")


if __name__ == "__main__":
    main()
