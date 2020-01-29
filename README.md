# video-editor

Video cutter based on `Python3` and `PyQt5`.

## Usage

```
python main.py
```

-   Select `Open` option in the menu bar to open a video.
-   Click `Start` button to set the starting time and click `End` button to set the ending time.
-   Click `Finish` button to start cutting the video.
-   After finishing cutting the video, a successful message will show on the message bar.

## Requirements

-   `PyQt5`.
-   `moviepy`.
-   [ImageMagic](https://imagemagick.org/script/download.php).
    -   Windows: Set `IMAGEMAGICK_BINARY = "C:\Program Files\ImageMagick-*VERSION*\magick.exe"` as an environment variable (default installation folder).

## License

-   MIT License.



