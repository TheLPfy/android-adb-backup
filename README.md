# android-adb-backup
Uses ADB to extract files with specific filename

## Preperation

1. Install Python 3.x
2. pip install tk -> tkinter
3. pip install pure-python-adb
4. Install adb: https://developer.android.com/studio/releases/platform-tools
   1. Download ZIP
   2. Extract it besides backup.py
   3. Done.
5. Edit **storePath** inside backup.py
6. RUN!

## Filters used in LS
### Remove Permission denied folders
2>&1 | grep -v "Permission denied"
