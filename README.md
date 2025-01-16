# RimuTrackRecord

This is just another financial tracking app. It uses pywebvies as GUI backend. So it's highly cross-platform by theory.

## Installation

```sh
git clone https://github.com/RimuEirnarn/RimuTrackRecord
cd RimuTrackRecord
# If you want to use virtual environment, please do so.
pip install -r ./requirements.txt
python main.py
```

The app should have been opened up.

## Issues & Features

You can create issues if you found a funky bugs or you want to request specific features.

## Quirks

The project uses sqlite-database as database manager and EnigmaRimu.js as JavaScript framework.

Most of the code still uses combination of `document.querySelector` and `$` (jQuery). They're pretty stable at the moment, still relatively slow.

Sure it also uses bootstrap for UI. On top of that, the backend doesn't have much going on. The project structure isn't definitely common, and how stuff works are probably different than any JavaScript frameworks that has ever existed.

For more information on WHAT the project uses, please see `requirements.txt` and `webui_dependencies.json`. You don't have to do `npm install` as it's all just typings. The app already handles client-side dependencies as well and will download stuff for you (it's required for obvious reason).