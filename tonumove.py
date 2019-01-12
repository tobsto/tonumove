#!/usr/bin/env python3

import argparse
import os
import shutil


def main():
    descr = """
    Script for adding folders with mp3 files or a single file to Tonuino sd card folder in the right format
    """
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("input", help='Folder with files or single file', type=str)
    parser.add_argument("-o", "--output", required=True, help='Folder where sd card is mounted', type=str)
    parser.add_argument("--superfolder", action='store_true', help='Input if folder which contains multiple folders or input files (each copied to a differnent destination folder')
    parser.add_argument("--overwrite", action='store_true', help='Clear sd-card before copying')

    args = parser.parse_args()

    if args.overwrite:
        answer = input("Are you sure you want to overwrite the sd card at %s? (y/n)" % args.output)
        if answer != 'y' and answer != 'Y':
            print('Abort')
            return
        else:
            print('Clear %s' % args.output)
            for f in [folder for folder, _, _ in os.walk(args.output)][1:]:
                shutil.rmtree(f)

    if not args.superfolder:
        copy2Tonuino(args.input, args.output)
    else:
        for folder, subfolders, files in os.walk(args.input):
            notRoot = folder is not args.input
            hasMp3 = len([f for f in os.listdir(folder) if f.endswith('.mp3')]) > 0
            if notRoot and hasMp3:
                print ('Processing %s' % folder)
                result = copy2Tonuino(folder, args.output)
                if result != 0:
                    print('Error while processing %s. Abort.' % folder)
                    return


def commonprefix(m):
    "Given a list of pathnames, returns the longest common leading component"
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1


def fixFileOrder(files):
    # get common prefix
    prefix = commonprefix(files)
    lp = len(prefix)
    # get track numbers
    trackNumberWidths = []
    trackNumbers = []
    for f in files:
        i = 0
        while str.isdigit(f[lp + i]):
            i = i + 1
            if i > 10:
                raise RunTimeError('Error while extracting track number')
        trackNumbers.append(int(f[lp:lp + i]))
        trackNumberWidths.append(i)
    trackNumberWidth = max(trackNumberWidths)
    newfiles = []
    for n, f in enumerate(files):
        newfile = prefix
        newfile += '{num:0{width}}'.format(num=trackNumbers[n], width=trackNumberWidth)
        newfile += f[lp + trackNumberWidths[n]:]
        newfiles.append(newfile)
    return newfiles


def checkSanity(sdcard):
    for n, (folder, subfolders, files) in enumerate(os.walk(sdcard)):
        if n == 0:
            for s in subfolders:
                if not len(s) == 2:
                    print('Warning: Subfolder %s has length > 2' % s)
                    return False
                if not str.isdigit(s[0]) and str.isdigit(s[1]):
                    print('Warning: Subfolder %s has non-digit characters' % s)
                    return False
                if not int(s) >= 0 and int(s) < 256:
                    print('Warning: Subfolder %s number is not between 1 and 255' % s)
                    return False
        if n > 0:
            for f in files:
                if not len(f) == 7:
                    print('Warning: File %s in folder %s does not have length 7' % (f, folder))
                    return False
                track = f[:3]
                if not f.endswith('.mp3'):
                    print('Warning: File %s in folder %s  does not end with .mp3' % (f, folder))
                    return False
                if not str.isdigit(track[0]) and str.isdigit(track[1]) and str.isdigit(track[2]):
                    print('Warning: File %s in folder %s is not comprised of digits' % (f, folder))
                    return False
    return True


def copy2Tonuino(input, output):
    """
    copy folders with mp3 files or a single file to Tonuino sd card folder in the right format

    input: file or folder with mp3 files
    output: mount point of sd card
    """
    # maximum number of folders on sd card
    maxNFolders = 100
    # maximum number of files in folders
    maxNFiles = 255
    # collect input files
    ifiles = []
    if os.path.isdir(input):
        ifiles = sorted([f for f in os.listdir(input) if f.endswith('.mp3')])
        ifiles_fixed = fixFileOrder(ifiles)
        ifiles = [f for _, f in sorted(zip(ifiles_fixed, ifiles))]

        if len(ifiles) == 0:
            print("Error: No mp3 files found in folder %s" % input)
            return -1
        if len(ifiles) > maxNFiles:
            print("Error: Too many (>%i) files in input folder folder %s" % (maxNFiles, input))
            return -1
    else:
        ifiles = [input]

    # get unused folder
    foldernames = ['%02i/' % n for n in range(maxNFolders)]
    foldersExists = [os.path.exists(os.path.join(output, name)) for name in foldernames]
    if all(foldersExists):
        print("Error: All %i folders exists. Free up space by removing at least one folder" % maxNFolders)
        return -1
    foldername = os.path.join(output, foldernames[foldersExists.index(False)])
    os.makedirs(foldername)

    # move files and rename them
    print('Copying files')
    for n, ifile in enumerate(ifiles):
        src = os.path.join(input, ifile)
        dest = os.path.join(foldername, "%03i.mp3" % (n + 1))
        print("%s->%s" % (src, dest))
        shutil.copy(src, dest)
    if not checkSanity(output):
        print("Warning content of sd-card does not meet format requirements. Please check")

    return 0


if __name__ == '__main__':
    main()
