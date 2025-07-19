mpremote cp main.py :main.py
mpremote cp config.py :config.py
mpremote rm -rf lib
mpremote cp -rf lib :lib
mpremote reset
mpremote