pyinstaller -F -w mainFrame.py -n SignalTools

pause

echo del build
rmdir /S/Q build

echo del *.spec
del *.spec