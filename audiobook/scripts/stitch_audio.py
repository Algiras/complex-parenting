import os
import subprocess


def main():
    output_dir = "audiobook_output"
    final_output = "audiobook_sample.mp3"

    # Get list of mp3 files sorted by name
    files = [f for f in os.listdir(output_dir) if f.endswith(".mp3")]
    files.sort()

    if not files:
        print("No MP3 files found to stitch.")
        return

    print(f"Found {len(files)} files to stitch:")
    for f in files:
        print(f" - {f}")

    # Create a file list for ffmpeg
    list_file = "files_to_stitch.txt"
    with open(list_file, "w") as f:
        for filename in files:
            # FFmpeg requires absolute paths or safe relative paths
            f.write(f"file '{os.path.join(output_dir, filename)}'\n")

    print("\nStitching with ffmpeg...")

    # FFmpeg command to concatenate
    # -f concat: use concat demuxer
    # -safe 0: allow unsafe file paths (relative)
    # -i list_file: input list
    # -c copy: copy stream without re-encoding (fast and lossless)
    cmd = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        list_file,
        "-c",
        "copy",
        final_output,
        "-y",  # Overwrite output
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Successfully created {final_output}")

        # Clean up list file
        os.remove(list_file)

    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg: {e}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")


if __name__ == "__main__":
    main()
