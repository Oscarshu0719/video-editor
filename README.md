# video-editor

Video cutter based on `Python3` and `PyQt5`.

## Usage

```
python main.py
```

-   Select `Open` option in the menu bar to open a video.
-   Click `Start` button to set the starting time and click `End` button to set the ending time. Click `Clear` to clear the recorded time.
-   Click `Subclip (Video)` button to start cutting the video or `Subclip (Audio)` for only audio.

## Requirements

-   `PyQt5`.
-   `moviepy`.
-   ImageMagick
    -   Windows: Download and install [ImageMagick](https://imagemagick.org/script/download.php).
    And set `IMAGEMAGICK_BINARY = "C:\Program Files\ImageMagick-*VERSION*\magick.exe"` as an environment variable (default installation folder).
    -   Ubuntu: See [ImageMagick - Community Help Wiki](https://help.ubuntu.com/community/ImageMagick).
    ``` 
    sudo apt-get update
    sudo apt-get install imagemagick --fix-missing
    ```
> Notice: (Ubuntu environment)
> 
> Change `'-i', '-', '-an'` to `'-an', '-i', '-'` in list type variable `cmd` in `/home/*USER*/anaconda3/envs/*ENV*/lib/python3.7/site-packages/moviepy/video/io/ffmpeg_writer.py`. (Probably in line `87`)

## License

-   MIT License.



