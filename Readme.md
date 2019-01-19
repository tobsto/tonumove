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

