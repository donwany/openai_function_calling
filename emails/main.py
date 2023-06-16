from utils import email_sender, draft_email

content = "Send an email to godataprof to check when he's going to upload new video on youtube"

data = draft_email(content=content)

print(data)


if __name__ == '__main__':
    email_sender(subject=data['subject'], body=data['body'])
