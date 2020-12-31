import boto3

class Session:
    def session(self,client_name):
        self.ses = boto3.session.Session(profile_name="default", region_name="us-east-2")
        self.client_name = client_name
        return None
    def client(self):
        clnt = self.ses.client(self.client_name)
        return clnt


def main():
    s3_obj = Session()
    s3_obj.session("s3")
    lb = s3_obj.client().list_buckets()
    lb = lb['Buckets']
    buck = []
    for i in lb:
       buck.append(i['Name'])
    return buck


if __name__ == '__main__':
    list_buckets = main()
    print(list_buckets)
