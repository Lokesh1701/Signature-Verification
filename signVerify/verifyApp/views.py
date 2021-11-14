from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from rest_framework import status 
from core.modelTrain import modelTraining
from core.modelTest import modelTesting
import os
import pytz 
import time
import logging
import datetime

from signVerify.configuration import getFileSize
from signVerify.configuration import getChecksum

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

class signVerify(ViewSet):

    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        response = {}
        try: 
            inputFile = request.data.get("inputFile")
            Project = request.data.get("Project")
            modelName = request.data.get("modelName")

            fileName, fileExtension = os.path.splitext(inputFile)
            fileName=fileName.split('/')
            fileName=fileName[-1]

            fileSize = getFileSize(inputFile)
            checksum = getChecksum(inputFile)

            processStart=datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            startSec = time.time()

            output = modelTesting(inputFile,modelName,Project)

            processStop=datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            stopSec = time.time()

            elapsedTime = stopSec - startSec
                   
            response["status"] = status.HTTP_200_OK   
            response["signatureVerification"] = True
            response["fileName"] = fileName
            response["fileExtension"] = fileExtension
            response["fileSize"] = fileSize
            response["fileChecksum"] = checksum
            response['elapsedTime'] = elapsedTime
            response['extractionProcessStart'] = processStart
            response['extractionProcessStop'] =processStop
            response["Class"] = output[0]
            response["outputAccuracy"] = output[1]     

        except Exception as e:
            print(e)
            response["status"] = status.HTTP_404_NOT_FOUND
            response["signatureVerification"] = False
            response["error_message"] = [str(e),'Error occured while evalating given file. Please check the debug logs']

        return Response(response)

class ModelTrain(ViewSet):

    serializer_class = UploadSerializer

    def list(self, request):
        return Response("POST API")

    def create(self, request):
        response = {}
        try:
            trainDir = request.data.get('trainDir')
            testDir = request.data.get('testDir')
            project = request.data.get('project')

            processStart=datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            startSec = time.time()

            modelName = modelTraining(trainDir,testDir,project)

            processStop=datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            stopSec = time.time()

            elapsedTime = stopSec - startSec

            logging.info(f'projectName {project}')
            logging.info(f'elapsedTime {elapsedTime}')
            logging.info(f'extractionProcessStart {extractionProcessStart}')
            logging.info(f'extractionProcessStop {extractionProcessStop}')
            logging.info(f'ModelName {ModelName}')
    

            response['status'] = status.HTTP_200_OK   
            response['ModelTrain'] = True      
            response['project'] = project
            response['elapsedTime'] = elapsedTime
            response['extractionProcessStart'] = processStart
            response['extractionProcessStop'] =processStop
            response['ModelName'] = modelName

        except Exception as e:
            logging.critical(e)
            response['status'] = status.HTTP_404_NOT_FOUND
            response['ModelTrain'] = False
            response['project'] = project
            response['error_message'] = [str(e),'Error occured while evalating given file. Please check the debug logs']

        return Response(response)
