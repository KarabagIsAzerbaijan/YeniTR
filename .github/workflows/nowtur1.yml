name: NowTur1 Update

on:
  schedule:
    - cron: "*/427 * * * *"  # təxminən hər 3 saat 7 dəqiqə
  workflow_dispatch:

jobs:
  update_nowtur1:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.13

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests dropbox

      - name: Run nowtur1 script
        env:
          DROPBOX_TOKEN: ${{ secrets.DROPBOX_TOKEN }}
        run: python ressources/tur/nowtur1.py
