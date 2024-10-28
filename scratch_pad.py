from pytube import Playlist, YouTube


# Function to download videos from a YouTube playlist
def download_playlist(playlist_url, save_path="."):
    try:
        # Create a Playlist object
        playlist = Playlist(playlist_url)

        print(f'Downloading playlist: {playlist.title}')
        
        # Loop through all videos in the playlist and download them
        for video_url in playlist.video_urls:
            print(f'Downloading: {video_url}')
            yt = YouTube(video_url)
            stream = yt.streams.get_audio_only()  # For downloading audio tracks only
            stream.download(output_path=save_path)
            print(f'Video "{yt.title}" downloaded successfully.')
        
        print("All videos in the playlist have been downloaded.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
playlist_url = 'https://www.youtube.com/playlist?list=PLGknEMhDGLFX7kqxmSfnfl7v7E4bBw41L'
download_playlist(playlist_url)
