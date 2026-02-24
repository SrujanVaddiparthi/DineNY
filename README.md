# DineNY
## Setup (Mac/Linux)

```bash
git clone <repo>
cd DineNY

python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Kaggle auth (required)
# Place kaggle.json at ~/.kaggle/kaggle.json and run:
chmod 600 ~/.kaggle/kaggle.json

# Download dataset (into repo, ignored by git)
mkdir -p data/raw
kaggle datasets download -d kwxdata/380k-restaurants-mostly-usa-based -p data/raw --unzip