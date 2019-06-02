Script for moving files to tonuino sd-card
==========================================

Script for adding folders with mp3 files or a single file to Tonuino sd card
folder in the right format

Usage: 

    tonumove.py [-h] -o OUTPUT [--superfolder] [--overwrite] input


positional arguments:

    input                 Folder with files or single file

optional arguments:

    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                          Folder where sd card is mounted (default: None)
    --superfolder         Input if folder which contains multiple folders or
                          input files (each copied to a differnent destination
                          folder (default: False)
    --overwrite           Clear sd-card before copying (default: False)
    --fixFileOrder        Fix order of files (experimental) (default: False)




Examples:
--------

Suppose we have the following file structure on our computer

    forTonuino/
        |- BibiBocksberg/
                |- Bibi01.mp3
                |- Bibi02.mp3
                |- Bibi03.mp3
        |- OmaSpricht.mp3
        |- KarlssonVomDach/
                |- Karlsson01.mp3
                |- Karlsson02.mp3
                |- Karlsson03.mp3

and the card is mounted at ``/mnt/sdcard``
Then we can add the folder ``BibiBlocksberg`` by 

    ./tonumove.py forTonuino/BibiBlockberg -o /mnt/sdcard/

We can move the whole content of ``forTonuino`` to the sd card by

    ./tonumove.py forTonuino/ -o /mnt/sdcard/ --superfolder


The experimental fixing of the file order works for files like this:

    |- BibiBocksberg/
            |- Bibi - 10 - Folge1.mp3
            |- Bibi - 1 - Folge1.mp3
            |- Bibi - 2 - Folge1.mp3
            |- Bibi - 3 - Folge1.mp3
            |- Bibi - 4 - Folge1.mp3
            |- Bibi - 5 - Folge1.mp3
            |- Bibi - 6 - Folge1.mp3
            |- Bibi - 7 - Folge1.mp3
            |- Bibi - 8 - Folge1.mp3
            |- Bibi - 9 - Folge1.mp3

With ``--fixFileOrder`` enabled the track 10 will be moved to the end where it belongs.
However, this feature does not work for files without digits or files with not digits (cf. #1)
