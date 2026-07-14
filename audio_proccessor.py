import yt_dlp
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

#----> for small Audio FILES duration(5 to 6 minutes approximately

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)  # ✅ fixed
        filename = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
    return filename



import os
from pydub import AudioSegment

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


#---->This Code Will Be for Large Vedio extraction Approximately 50 to 60 minutes
#----That is why we need chunking in order to divide our vedio in to sgements and chunks

def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i , start in enumerate (range(0,len(audio),chunk_ms)):
        chunk = audio[start: start +chunk_ms]
        chunk_path = f"{wav_path}_chunk{i}.wav"
        chunk.export(chunk_path,format="wav")

        chunks.append(chunk_path)
    
    return chunks

#this function is mainly for detecting url menas we dont want to put url in manuall way we created seprate function for it thats it 


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks

