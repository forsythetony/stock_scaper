import boto3

class SnsWrapper:
    
    def __init__(self, topic_arn: str, region: str):
        self.topic_arn = topic_arn
        self.region = region

        self.sns_client = self._build_client()
        self.topic = self.sns_client.Topic(topic_arn)


    def _build_client(self):
        session = boto3.Session()
        return session.resource('sns', region_name=self.region)

    def publish_message(self, subject: str, message: str):
        self.topic.publish(
            Message=message,
            Subject=subject,
            
    )

    def __str__(self) -> str:
        return f"Topic -> {self.topic_arn} ... Region -> {self.region}"
