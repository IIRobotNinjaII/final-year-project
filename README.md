sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev git libssl-dev openssl


curl https://pyenv.run | bash

sudo nano  ~/.bashrc

#paste the below lines in bashrc
export PATH="${HOME}/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
#open a new terminal

pyenv install 3.7-dev
pyenv global 3.7-dev

python --version
# it should say 3.7+
export PATH="/home/antony/abe/fabric/bin:$PATH"
mkdir abe
cd abe

wget https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz --no-check-certificate
tar -xf gmp-6.3.0.tar.xz
cd gmp-6.3.0
sudo ./configure
sudo make
sudo make install

cd ..
wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz --no-check-certificate
tar -xzf pbc-0.5.14.tar.gz
cd pbc-0.5.14
sudo ./configure
sudo make
sudo make install

cd ..
sudo apt-get install libssl-dev openssl

git clone https://github.com/JHUISI/charm.git
cd charm
python -m venv project
source project/bin/activate
./configure.sh
sudo make install 

cd ..
git clone https://github.com/IIRobotNinjaII/final-year-project.git
cd final-year-project
cd flask_application
pip install -r requirements.txt
export FLASK_APP=server 
export FLASK_DEBUG=1
flask run --port=8081


#make sure to pull latest git repo and your work is saved properly somewhere just in case of merge conflicts

sudo apt-get install git

sudo apt-get install curl

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose

sudo usermod -aG docker $USER

wget "https://go.dev/dl/go1.22.2.linux-amd64.tar.gz" --no-check-certificate
sudo tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz
cd 
sudo nano .bashrc
#add this to the end
export PATH=$PATH:/usr/local/go/bin

sudo apt install jq
#open new terminal after this

mkdir hyp
cd hyp
curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh && chmod +x install-fabric.sh
./install-fabric.sh
cd fabric-samples/test-networks
./network.sh down
./network.sh up createChannel -c mychannel
#put those 2 chaincodes into fabric-samples/asset-transfer-basic/chaincode-go/chaincode
#only deploy one at a time, so rename one to comment.go.example and deploy the complaint.go
#run this command to deploy
./network.sh deployCC -ccn complaint -ccp ../asset-transfer-basic/chaincode-go/ -ccl go
#now rename complaint.go to complaint.go.example and rename comment.go.example to comment.go
#run this
./network.sh deployCC -ccn comment -ccp ../asset-transfer-basic/chaincode-go/ -ccl go

cd /final-year-project/rest-api-go/
go run main.go

#now run python backend as normal

