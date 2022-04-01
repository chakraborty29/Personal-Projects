# Setup with Kubeadm (in progress)
**Description:** Installing and setting up VMs in Hyper-V to launch a Kubernetes Cluster locally and exposing the cluster to the public internet.
 
#### Table of Contents
- [VM Setup](#vm-setup)
- [ONLY ON HAPROXY](#only-on-haproxy)
- [Setting up Docker](#setting-up-docker)
- [Install Kubernetes](#install-kubernetes)
- [Setting up Kubernetes](#setting-up-kubernetes)
- [Installing Cert Manager and NGINX Ingress](#installing-cert-manager-and-nginx-ingress)
- [Enabling public access with Cloudflare](#enabling-public-access-with-cloudflare)
- [Potential Issues (in progress)](#potential-issues)
- [References](#references)
- [Next steps](#next-steps)
## VM Setup

### Install all updates
```
sudo apt update && sudo apt dist-upgrade
```
### Enable ssh for VMs
```
sudo apt install -y nano net-tools openssh-server && sudo systemctl enable ssh && sudo ufw allow ssh && sudo systemctl start ssh
```
```
sudo reboot
```

### Add kube-master host on NODE  VMs
```
sudo nano /etc/hosts
```
Add
```
<IP-ADDRESS-OF-FIRST-MASTER-NODE> kube-master
```

## ONLY ON HAPROXY
```
sudo apt install -y haproxy
```
Edit haproxy config
```
sudo nano /etc/haporxy.haproxy.cfg
```
which follows this [example](https://github.com/kubernetes/kubeadm/blob/main/docs/ha-considerations.md#haproxy-configuration)
Use the ip address of your nodes for master and worker nodes
```
# /etc/haproxy/haproxy.cfg
#---------------------------------------------------------------------
# Global settings
#---------------------------------------------------------------------
global
    log /dev/log local0
    log /dev/log local1 notice
    daemon

#---------------------------------------------------------------------
# common defaults that all the 'listen' and 'backend' sections will
# use if not designated in their block
#---------------------------------------------------------------------
defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 1
    timeout http-request    10s
    timeout queue           20s
    timeout connect         5s
    timeout client          20s
    timeout server          20s
    timeout http-keep-alive 10s
    timeout check           10s
#---------------------------------------------------------------------
# apiserver frontend which proxys to the masters
#---------------------------------------------------------------------
frontend apiserver
    bind *:6443
    mode tcp
    option tcplog
    default_backend apiserver

#---------------------------------------------------------------------
# round robin balancing for apiserver
#---------------------------------------------------------------------
backend apiserver
    option httpchk GET /healthz
    http-check expect status 200
    mode tcp
    option ssl-hello-chk
    balance     roundrobin
        server master-node-01 192.168.1.130:6443 check
        server master-node-02 192.168.1.149:6443 check

frontend proxy_http
  bind *:80
  stats uri /haproxy?stats
  use_backend proxy_http

backend proxy_http
  balance roundrobin
  server worker-node-01 192.168.1.131:80 check
  server worker-node-02 192.168.1.146:80 check
  server worker-node-03 192.168.1.147:80 check

frontend proxy_https
    bind *:443
    mode tcp
    option tcplog
    default_backend proxy_https

backend proxy_https
  mode tcp
  option ssl-hello-chk
  balance     roundrobin
  server worker-node-01 192.168.1.131:443 check
  server worker-node-02 192.168.1.146:443 check
  server worker-node-03 192.168.1.147:443 check
```

## Setting up Docker

### Install Docker
```
sudo curl -sSL get.docker.com | sh
```
```
sudo usermod -aG docker $(whoami)
```
Then edit:
```
sudo nano /etc/docker/daemon.json
```
Add:
```
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
```
Then edit:
```
sudo nano /etc/sysctl.conf
```
Uncomment:
```
#net.ipv4.ip_forward=1
```
then
```
sudo reboot
```

### Check Docker status
```
systemctl status docker
```

## Install Kubernetes
### Add Kubernetes Repository
Edit:
```
sudo nano /etc/apt/sources.list.d/kubernetes.list
```
Add:
```
deb http://apt.kubernetes.io/ kubernetes-xenial main
```
### Add GCP keys
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
``` 
### Install Kubernetes Packages
```
sudo apt update
```
```
sudo apt install kubeadm kubectl kubelet
```

## Setting up Kubernetes

### Create first control plane
First run
```
sudo kubeadm init --control-plane-endpoint kube-master:6443 --pod-network-cidr=10.244.0.0/16
```
Then run the following to add the required config files
```
mkdir -p $HOME/.kube && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config && sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
### Add Kubernetes flannel for networking
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

### Add worker nodes
On the **master node** we need to generate a new token
```
sudo kubeadm token generate
```
Then
```
sudo kubeadm token create <TOKEN-FROM-GENERATE-STEP> --ttl 1h --print-join-command
```
Copy the output and paste it to your worker nodes. **Sample output:**
```
sudo kubeadm join kube-master:6443 --token w33hha.ww9jxt7t7gwnziqn --discovery-token-ca-cert-hash sha256:c5b4ef8a6dfb9da6f76f7938a92306f990a4532c81217a031042b3477da1c327
```

### Add Control Plane
Get the certificate key
```
sudo kubeadm init phase upload-certs --upload-certs
```
Generate new token
```
sudo kubeadm token generate
```
Then
```
sudo kubeadm token create <TOKEN-FROM-GENERATE-STEP> --ttl 1h --print-join-command
```
You want to take the output and add the following at the end
```
--control-plane --certificate-key <KEY-FROM-UPLOAD-CERT-STEP>
```
This is an example of what it should look like
```
sudo kubeadm join kube-master:6443 --token w33hha.ww9jxt7t7gwnziqn --discovery-token-ca-cert-hash sha256:c5b4ef8a6dfb9da6f76f7938a92306f990a4532c81217a031042b3477da1c327 --control-plane --certificate-key 19b998a889623fff6a1a786f3b9f5ca92b2d885f4a30b546f17d73b2f7287d1d
```
Then run the following to get the correct config files
```
mkdir -p $HOME/.kube && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config && sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Installing Cert Manager and NGINX Ingress

Install cert-manager
```
helm install cert-manager
```
Install nginx-ingress
```
git clone https://github.com/nginxinc/kubernetes-ingress.git
```
Then
```
cd kubernetes-ingress/deployments/helm-chart
```
Finally
```
helm upgrade -i nginx-ingress . --namespace nginx-ingress --set controller.kind=daemonset --create-namespace
```
## Enabling public access with Cloudflare
- Buy a domain name with whatever provider and transfer the domain to Cloudflare
- Get your public IP address and add it as an A record to your domain name
- Port forward ports, 80, 443, 6443 and 22 on your router for your Haproxy Loadbalancer

### Adding Letsencrypt with Cloudflare
To launch services with ingress endpoints and SSL Certificates you need to set up letsencrypts cert issuer with cloudflare.

Create a Cloudflare API key with the permission to create dns records for the given zone. Then create a secrets in Kubernetes.

Create a file, cloudflare-api-secret.yaml
```
apiVersion: v1  
kind: Secret  
metadata:  
  name: cloudflare-api-token-secret  
  namespace: cert-manager  
type: Opaque  
stringData:  
  apiKey: <your cloudflare api key>
```
Let's apply it
```
kubectl apply -f cloudflare-api-secret.yaml
```
Lets create a file, issuer.yaml
```
apiVersion:  cert-manager.io/v1  
kind:  ClusterIssuer  
metadata:  
  name:  letsencrypt-prod  
  namespace:  cert-manager  
spec:  
  acme:  
    server:  https://acme-v02.api.letsencrypt.org/directory  
	email:  name@yourname.xzy  
	privateKeySecretRef:  
	  name:  letsencrypt-prod  
	solvers:  
	  - dns01:  
	    cloudflare:  
		  email:  <cloudflare  account  email>  
		  apiTokenSecretRef:  
		    name:  cloudflare-api-token-secret  
		    key:  apiKey
```
Let's apply it
```
kubectl apply -f issuer.yaml
```
## Potential Issues
in progress ...

### Kubelet not running on reboot
```
sudo swapoff -a
```

### Resetting a Cluster
If you need to **reset** a cluster, run the following
```
sudo kubeadm reset -f && sudo rm -rf /etc/cni /etc/kubernetes /var/lib/dockershim /var/lib/etcd /var/lib/kubelet /var/run/kubernetes ~/.kube/* && sudo systemctl restart containerd && sudo systemctl restart kubelet
```

### Resetting Network
Can't remember what exactly causes this, but if you get an error with any pods that has to do with CIDR: < ip-address >, you might need to reset your network
```
sudo ip link set cni0 down && sudo ip link set flannel.1 down && sudo ip link delete cni0 && sudo ip link delete flannel.1
```

### Tainting and Untainting Nodes
#### Taint
```
kubectl taint nodes <name of node> node-role.kubernetes.io/master=:NoSchedule
```
#### Untaint
```
kubectl taint node <name of node> node-role.kubernetes.io/master-
```

### Deleting namespaces that are stuck on terminating
When installing big services like Rancher and you need to delete the namespace, but it gets stuck on terminating, the following code removes that namespace.
You can see it [here](https://stackoverflow.com/questions/52369247/namespace-stuck-as-terminating-how-i-removed-it/58644787#58644787)
```
(
NAMESPACE=your-rogue-namespace
kubectl proxy &
kubectl get namespace $NAMESPACE -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
)
```
## References
- https://github.com/marcel-dempers/docker-development-youtube-series/tree/master/kubernetes/rancher
- https://www.learnlinux.tv/building-a-10-node-raspberry-pi-kubernetes-cluster/
- https://www.techrunnr.com/how-to-reset-kubernetes-cluster/
- https://someweb.github.io/devops/cert-manager-kubernetes/
- https://rudimartinsen.com/2020/08/14/scaling-out-a-kubernetes-cluster/
- https://community.cloudflare.com/t/examples-ingress-cloudflared-configuration-when-exposing-via-ingress-kubernetes/331844/2

## Next steps
I have a lot planned for this project. This is just a basic overview on getting a cluster running and exposing it to the public internet to run services, apis or whatever your heart desires. My next steps are to implement this with K3s instead of Kubeadm, and to add a persistent storage with minio and slowly start running all my web based personal projects on my own servers instead of AWS. I will be moving my [Todo list application](https://github.com/chakraborty29/Todo-List-Full-Stack)  into this cluster and adding a README to everything.