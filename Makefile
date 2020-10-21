docker-build:
	bash shell/docker-build.sh

docker-push:
	bash shell/docker-build.sh push

run:
	bash shell/run.sh select-picture-sequentially