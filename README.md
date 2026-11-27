# NetEase radio quality plugin for yt-dlp

This third-party plugin lets yt-dlp check the 128, 192, and 320 kbps tiers for NetEase Cloud Music radio episodes. When a playable response omits its `level` field, the built-in extractor stops checking for additional formats. The plugin keeps checking the free tiers, lists the bitrates NetEase reports, and filters out duplicate streams and trial clips.

On Windows with yt-dlp `2026.11.23`, episode `2541901866` listed 128, 192, and 320 kbps MP3 without a paid membership. Available formats vary by episode. For episodes that omit `level`, the plugin checks the free tiers only.

[Background: yt-dlp issue #16169](https://github.com/yt-dlp/yt-dlp/issues/16169)

## Install

Download `netease-program-quality.zip` from this repository's Releases page. On Windows, put the ZIP in a folder named `yt-dlp-plugins` next to `yt-dlp.exe`. Leave the ZIP packed.

```text
yt-dlp.exe
yt-dlp-plugins/
  netease-program-quality.zip
```

For other layouts, pass the directory containing the ZIP to `--plugin-dirs`, or use a default location from the [yt-dlp plugin installation guide](https://github.com/yt-dlp/yt-dlp#installing-plugins).

## Use

Run these examples in PowerShell from the folder containing `yt-dlp.exe`. Replace the example URL with your episode URL.

```powershell
# List available formats and confirm the plugin loaded
.\yt-dlp.exe --no-playlist -v -F 'https://music.163.com/#/program?id=2541901866'

# Download the available audio with the highest reported bitrate
.\yt-dlp.exe --no-playlist -f ba -S abr 'https://music.163.com/#/program?id=2541901866'
```

The first command should show `netease:program+netease-program-quality` in the log. Read the `ABR` column for the reported audio bitrate. If you need to require 320 kbps or higher, use `-f 'ba[abr>=320]'`.

## Build the plugin ZIP

From the repository root, run:

```powershell
python -m zipfile -c netease-program-quality.zip yt_dlp_plugins
```

The archive must contain `yt_dlp_plugins/extractor/netease_program_quality.py` with no extra top-level folder.

## Credits

The extractor extends yt-dlp's built-in NetEase program extractor. The plugin was developed with AI assistance and manually tested on Windows.
