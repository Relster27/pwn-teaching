sudo adduser pwner

sudo usermod -aG sudo pwner

sudo userdel -r pwner

--------------------------------------------------------
# Python Environment #
mkdir pyenv

python3 -m venv ~/pyenv

source ~/pyenv/bin/activate

--------------------------------------------------------
# Install pwndbg #
git clone https://github.com/pwndbg/pwndbg.git ~/pwndbg

cd ~/pwndbg

./setup.sh

echo "source /home/pwner/pwndbg/gdbinit.py" >> .gdbinit

--------------------------------------------------------
# Install gef #
git clone https://github.com/hugsy/gef.git ~/gef

echo "source /home/pwner/gef/gef.py" >> .gdbinit

--------------------------------------------------------
# Install ropper #
pip install ropper
