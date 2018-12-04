from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    # 이 storage를 사용해서 저장되는 파일들이
    # <location 의 값 >/<추가경로> 부분에 저장이 됨.ㅌ₩
    location = 'media'
    default_acl = 'public-read'


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
