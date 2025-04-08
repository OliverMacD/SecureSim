@echo off
REM Set your Python module source path and output path
set SOURCE=..\..
set OUTPUT=source\api

echo 🛠 Generating Sphinx API documentation...
sphinx-apidoc -o %OUTPUT% %SOURCE%\process_sim
sphinx-apidoc -o %OUTPUT% %SOURCE%\control_logic
sphinx-apidoc -o %OUTPUT% %SOURCE%\servers

REM Optional: manually include top-level scripts like main.py
echo. > %OUTPUT%\main.rst
echo Main Script > %OUTPUT%\main.rst
echo ========== >> %OUTPUT%\main.rst
echo. >> %OUTPUT%\main.rst
echo .. automodule:: main >> %OUTPUT%\main.rst
echo     :members: >> %OUTPUT%\main.rst
echo     :undoc-members: >> %OUTPUT%\main.rst

echo ✅ Done! API docs generated in %OUTPUT%.
