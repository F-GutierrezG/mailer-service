# !/bin/bash
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker login -u gitlab-ci-token -p $DOCKER_TOKEN registry.gitlab.com"

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network create --subnet=172.25.0.0/16 mailer-service-network'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container stop mailer'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container stop mailer-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container rm mailer'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container rm mailer-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/mailer-service/mailer-swagger -q)'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/mailer-service/mailer -q)'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker run --log-driver=awslogs --log-opt awslogs-region=us-east-2 --log-opt awslogs-group=MailerServiceSwagger -d --restart always -e 'API_URL=definitions/swagger.yml' --name mailer-swagger --network mailer-service-network --ip 172.25.0.3 $REGISTRY_REPO/$SWAGGER:$TAG"
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker run --log-driver=awslogs --log-opt awslogs-region=us-east-2 --log-opt awslogs-group=MailerService -d --restart always -e 'FLASK_ENV=production' -e 'FLASK_APP=manage.py' -e 'APP_SETTINGS=project.config.ProductionConfig' -e SECRET_KEY=$PROD_SECRET_KEY -e SENDGRID_API_KEY=$PROD_SENDGRID_API_KEY --name mailer --network mailer-service-network --ip 172.25.0.2 $REGISTRY_REPO/$MAILER:$TAG"

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect onelike-network --ip 172.18.0.16 mailer'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect onelike-network --ip 172.18.0.17 mailer-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect users-service-network --ip 172.20.0.10 mailer'
