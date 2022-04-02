# Todolist Application
This is a full stack application with Vue.js as the front-end and Django REST Framework as the backend. I worked on this application to test my abilities to build a full stack application from scratch and implement DevOps practices such as CI and CD.

## Vue.js Frontend
This part of the application is created with Vue.js and continuously deployed with Gitlab CI/CD to an AWS S3 bucket. The link no longer works as I had to shutdown my AWS account because I ran out of the free trial.
### Next Steps
I plan to containerize this whole application and later continuously deploy it to my [own Kubernetes cluster](https://github.com/chakraborty29/Personal-Projects/blob/main/kubernetes/setup-with-kubeadm.md) using Gitlab CI/CD and using my own Gitlab runners instead of using the free limited runner given by Gitlab. Gitlab only allows about 200 minutes of pipelines and with my own runner I can get unlimited. 

## Django REST Framework Backend
This part of the application is created with DRF and continuously deployed with Gitlab CI/CD to an AWS EC2 Instance and the database to a RDS Instance. For the same reason state above, I do not have this API running. 
### Next steps
I plan to first complete the Kubernetes project, figure out persistent data storage with Minio and then figure out creating websocket connections with Redis for real-time data and make this into a real time API. I also need to figure out how I would create persistent database management with SQL on Kubernetes before I can host this API on my own servers. 