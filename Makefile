STACK_NAME := alexa-cloud-shiritori
APP_DIR := cloud_shiritori
BUILD_IMAGE := lambci/lambda:build-python3.6
PACKAGED_TEMPLATE := ./packaged.yaml

.PHONY: clean
clean:
	rm -rf ./build/*
	rm -f ./requirements.txt

.PHONY: build
build:
	mkdir -p ./build
	rsync -avz --exclude='*.pyc' --prune-empty-dirs --delete ./$(APP_DIR)/ ./build/$(APP_DIR)/
	pipenv lock --requirements > ./requirements.txt

.PHONY: vendor
vendor:
	docker run -v $$PWD:/var/task --rm -it $(BUILD_IMAGE) /bin/bash -c 'pip --disable-pip-version-check install --no-binary :all: -U -t ./build -r ./requirements.txt'

.PHONY: package
package:
	aws cloudformation package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket $(S3_BUCKET_NAME)

.PHONY: deploy
deploy:
	aws cloudformation deploy --template-file packaged.yaml --stack-name $(STACK_NAME) --capabilities CAPABILITY_NAMED_IAM --s3-bucket $(S3_BUCKET_NAME)