# -*- coding: utf-8 -*-
# Minimal Object Storage Library, (C) 2015 Minio, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from nose.tools import eq_
from unittest import TestCase

from minio.generators import ListUploadParts
from .minio_mocks import MockResponse, MockConnection

__author__ = 'minio'

class ListPartsTest(TestCase):
    @mock.patch('urllib3.PoolManager')
    def test_empty_list_parts_works(self, mock_connection):
        mock_data = '''<?xml version="1.0"?>
                       <ListPartsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
                         <Bucket>bucket</Bucket>
                         <Key>go1.4.2</Key>
                         <UploadId>ntWSjzBytPT2xKLaMRonzXncsO10EH4Fc-Iq2-4hG-ulRYB</UploadId>
                         <Initiator>
                           <ID>minio</ID>
                           <DisplayName>minio</DisplayName>
                         </Initiator>
                         <Owner>
                           <ID>minio</ID>
                           <DisplayName>minio</DisplayName>
                         </Owner>
                         <StorageClass>STANDARD</StorageClass>
                         <PartNumberMarker>0</PartNumberMarker>
                         <NextPartNumberMarker>0</NextPartNumberMarker>
                         <MaxParts>1000</MaxParts>
                         <IsTruncated>false</IsTruncated>
                       </ListPartsResult>
                    '''
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('GET', 'http://localhost:9000/bucket/key?max-parts=1000&uploadId=upload_id', {}, 200, content=mock_data))
        part_iter = ListUploadParts(mock_server, 'http://localhost:9000', 'bucket', 'key', 'upload_id')
        parts = []
        for part in part_iter:
            parts.append(part)
        eq_(0, len(parts))

    @mock.patch('urllib3.PoolManager')
    def test_list_objects_works(self, mock_connection):
        mock_data = '''<?xml version="1.0"?>
                       <ListPartsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
                         <Bucket>bucket</Bucket>
                         <Key>go1.4.2</Key>
                         <UploadId>ntWSjzBytPT2xKLaMRonzXncsO10EH4Fc-Iq2-4hG-ulRYB</UploadId>
                         <Initiator>
                           <ID>minio</ID>
                           <DisplayName>minio</DisplayName>
                         </Initiator>
                         <Owner>
                           <ID>minio</ID>
                           <DisplayName>minio</DisplayName>
                         </Owner>
                         <StorageClass>STANDARD</StorageClass>
                         <PartNumberMarker>0</PartNumberMarker>
                         <NextPartNumberMarker>0</NextPartNumberMarker>
                         <MaxParts>1000</MaxParts>
                         <IsTruncated>false</IsTruncated>
                         <Part>
                           <PartNumber>1</PartNumber>
                           <ETag>79b281060d337b9b2b84ccf390adcf74</ETag>
                           <LastModified>2015-06-03T03:12:34.756Z</LastModified>
                           <Size>5242880</Size>
                         </Part>
                         <Part>
                           <PartNumber>2</PartNumber>
                           <ETag>79b281060d337b9b2b84ccf390adcf74</ETag>
                           <LastModified>2015-06-03T03:12:34.756Z</LastModified>
                           <Size>5242880</Size>
                         </Part>
                       </ListPartsResult>
                    '''
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(MockResponse('GET', 'http://localhost:9000/bucket?max-uploads=1000&uploadId=upload_id', {}, 200,
                                                  content=mock_data))
        part_iter = ListUploadParts(mock_server, 'http://localhost:9000', 'bucket', 'key', 'upload_id')
        parts = []
        for part in part_iter:
            parts.append(part)
        eq_(2, len(parts))

    @mock.patch('urllib3.PoolManager')
    def test_list_objects_works(self, mock_connection):
        mock_data1 = '''<?xml version="1.0"?>
                        <ListPartsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
                          <Bucket>bucket</Bucket>
                          <Key>go1.4.2</Key>
                          <UploadId>ntWSjzBytPT2xKLaMRonzXncsO10EH4Fc-Iq2-4hG-ulRYB</UploadId>
                          <Initiator>
                            <ID>minio</ID>
                            <DisplayName>minio</DisplayName>
                          </Initiator>
                          <Owner>
                            <ID>minio</ID>
                            <DisplayName>minio</DisplayName>
                          </Owner>
                          <StorageClass>STANDARD</StorageClass>
                          <PartNumberMarker>0</PartNumberMarker>
                          <NextPartNumberMarker>2</NextPartNumberMarker>
                          <MaxParts>1000</MaxParts>
                          <IsTruncated>true</IsTruncated>
                          <Part>
                            <PartNumber>1</PartNumber>
                            <ETag>79b281060d337b9b2b84ccf390adcf74</ETag>
                            <LastModified>2015-06-03T03:12:34.756Z</LastModified>
                            <Size>5242880</Size>
                          </Part>
                          <Part>
                            <PartNumber>2</PartNumber>
                            <ETag>79b281060d337b9b2b84ccf390adcf74</ETag>
                            <LastModified>2015-06-03T03:12:34.756Z</LastModified>
                            <Size>5242880</Size>
                          </Part>
                        </ListPartsResult>
                        '''
        mock_data2 = '''<?xml version="1.0"?>
                        <ListPartsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
                          <Bucket>bucket</Bucket>
                          <Key>go1.4.2</Key>
                          <UploadId>ntWSjzBytPT2xKLaMRonzXncsO10EH4Fc-Iq2-4hG-ulRYB</UploadId>
                          <Initiator>
                            <ID>minio</ID>
                            <DisplayName>minio</DisplayName>
                          </Initiator>
                          <Owner>
                            <ID>minio</ID>
                            <DisplayName>minio</DisplayName>
                          </Owner>
                          <StorageClass>STANDARD</StorageClass>
                          <PartNumberMarker>0</PartNumberMarker>
                          <NextPartNumberMarker>0</NextPartNumberMarker>
                          <MaxParts>1000</MaxParts>
                          <IsTruncated>false</IsTruncated>
                          <Part>
                            <PartNumber>3</PartNumber>
                            <ETag>79b281060d337b9b2b84ccf390adcf74</ETag>
                            <LastModified>2015-06-03T03:12:34.756Z</LastModified>
                            <Size>5242880</Size>
                          </Part>
                          <Part>
                            <PartNumber>4</PartNumber>
                            <ETag>79b281060d337b9b2b84ccf390adcf74</ETag>
                            <LastModified>2015-06-03T03:12:34.756Z</LastModified>
                            <Size>5242880</Size>
                          </Part>
                        </ListPartsResult>
                     '''
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(MockResponse('GET', 'http://localhost:9000/bucket/key?max-parts=1000&uploadId=upload_id', {}, 200,
                                                  content=mock_data1))
        part_iter = ListUploadParts(mock_server, 'http://localhost:9000',
                                    'bucket', 'key', 'upload_id')
        parts = []
        for part in part_iter:
            mock_server.mock_add_request(
                MockResponse('GET', 'http://localhost:9000/bucket/key?max-parts=1000&part-number-marker=2&uploadId=upload_id', {}, 200,
                             content=mock_data2))
            parts.append(part)
        eq_(4, len(parts))