# android-adb-backup
Uses ADB to extract files with specific filename

## Filters used in LS
### Remove Permission denied folders
2>&1 | grep -v "Permission denied"
