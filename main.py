import requests
import json
import uuid
import time
from datetime import datetime
import urllib.parse
import html

action_id=-48

find_url='https://mail.spbstu.ru/owa/service.svc?action=FindConversation'
create_url='https://mail.spbstu.ru/owa/service.svc?action=CreateItem'

find_cookies = {"X-BackEndCookie": "<redacted>",
                "ClientId": "<redacted>",
                "X-OWA-JS-PSD": "1",
                "UC": "<redacted>",
                "FedAuth": "<redacted>",
                "FedAuth1": "<redacted>",
                "TimeWindow": "<redacted>",
                "TimeWindowKey": "<redacted>",
                "TimeWindowIV": "<redacted>",
                "TimeWindowSig": "<redacted>",
                "X-OWA-CANARY":"<redacted>"}

find_headers = {
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/json; charset=UTF-8',
        'X-Owa-Actionname':'Browse_All',
        'User-Agent': '<redacted>',
        'X-Owa-Correlationid': "<redacted>", ##
        'Action':'FindConversation',
        'Accept-Language':'ru-RU,ru;q=0.9',
        'X-Owa-Canary':'<redacted>',
        'X-Owa-Urlpostdata': '%7B%22__type%22%3A%22FindConversationJsonRequest%3A%23Exchange%22%2C%22Header%22%3A%7B%22__type%22%3A%22JsonRequestHeaders%3A%23Exchange%22%2C%22RequestServerVersion%22%3A%22V2016_02_03%22%2C%22TimeZoneContext%22%3A%7B%22__type%22%3A%22TimeZoneContext%3A%23Exchange%22%2C%22TimeZoneDefinition%22%3A%7B%22__type%22%3A%22TimeZoneDefinitionType%3A%23Exchange%22%2C%22Id%22%3A%22Russian%20Standard%20Time%22%7D%7D%7D%2C%22Body%22%3A%7B%22__type%22%3A%22FindConversationRequest%3A%23Exchange%22%2C%22ParentFolderId%22%3A%7B%22__type%22%3A%22TargetFolderId%3A%23Exchange%22%2C%22BaseFolderId%22%3A%7B%22__type%22%3A%22DistinguishedFolderId%3A%23Exchange%22%2C%22Id%22%3A%22sentitems%22%7D%7D%2C%22ConversationShape%22%3A%7B%22__type%22%3A%22ConversationResponseShape%3A%23Exchange%22%2C%22BaseShape%22%3A%22IdOnly%22%7D%2C%22ShapeName%22%3A%22ConversationSentItemsListView%22%2C%22Paging%22%3A%7B%22__type%22%3A%22IndexedPageView%3A%23Exchange%22%2C%22BasePoint%22%3A%22Beginning%22%2C%22Offset%22%3A0%2C%22MaxEntriesReturned%22%3A25%7D%2C%22ViewFilter%22%3A%22All%22%2C%22FocusedViewFilter%22%3A-1%2C%22SortOrder%22%3A%5B%7B%22__type%22%3A%22SortResults%3A%23Exchange%22%2C%22Order%22%3A%22Descending%22%2C%22Path%22%3A%7B%22__type%22%3A%22PropertyUri%3A%23Exchange%22%2C%22FieldURI%22%3A%22ConversationLastDeliveryTime%22%7D%7D%5D%7D%7D',
        'Client-Request-Id': "<redacted>", ##
        'Accept': '*/*',
        'Origin': 'https://mail.spbstu.ru',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i',
        "X-Owa-Actionid": "-14"
    }

create_cookies={
    "X-BackEndCookie":"<redacted>",
    "ClientId":"<redacted>",
    "FedAuth":"<redacted>",
    "FedAuth1":"<redacted>",
    "UC":"<redacted>",
    "X-OWA-JS-PSD":"1",
    "TimeWindow":"<redacted>",
    "TimeWindowKey":"<redacted>",
    "TimeWindowIV":"<redacted>",
    "TimeWindowSig":"<redacted>",
    "X-OWA-CANARY":"<redacted>"
}

create_headers={
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
    'X-Owa-Serviceunavailableontransienterror':'true',
    'Sec-Ch-Ua-Mobile': '?0',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/json; charset=UTF-8',
    'X-Owa-Actionname':'CreateMessageForComposeSend',
    'X-Owa-Correlationid':'<redacted>', ##
    'Action':'CreateItem',
    'Accept-Language':'ru-RU,ru;q=0.9',
    'X-Owa-Canary':'<redacted>',
    'Client-Request-Id':'<redacted>', ##
    'X-Owa-Clientbuildversion':'15.2.1258.34',
    'User-Agent': '<redacted>',
    'X-Owa-Actionid':'-48',
    'Accept':'*/*',
    'Origin':'https://mail.spbstu.ru',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Dest':'empty',
    'Accept-Encoding':'gzip, deflate, br',
    'Priority':'u=1, i'

}

def make_recipients_list(emails):
    return [
        {
            "__type": "EmailAddress:#Exchange",
            "MailboxType": "OneOff",
            "RoutingType": "SMTP",
            "EmailAddress": email,
            "Name": email
        } for email in emails if email.strip()
    ]

def create_json(subject, value, to_emails):
    return {
        "__type": "CreateItemJsonRequest:#Exchange",
        "Header": {
            "__type": "JsonRequestHeaders:#Exchange",
            "RequestServerVersion": "V2015_10_15",
            "TimeZoneContext": {
                "__type": "TimeZoneContext:#Exchange",
                "TimeZoneDefinition": {
                    "__type": "TimeZoneDefinitionType:#Exchange",
                    "Id": "Russian Standard Time"
                }
            }
        },
        "Body": {
            "__type": "CreateItemRequest:#Exchange",
            "Items": [
                {
                    "__type": "Message:#Exchange",
                    "Subject": subject,
                    "Body": {
                        "__type": "BodyContentType:#Exchange",
                        "BodyType": "HTML",
                        "Value": value
                    },
                    "DocLinks": [],
                    "Importance": "Normal",
                    "From": None,
                    "ToRecipients": make_recipients_list(to_emails or []),
                    "CcRecipients": [],
                    "BccRecipients": [],
                    "Sensitivity": "Normal",
                    "IsDeliveryReceiptRequested": False,
                    "IsReadReceiptRequested": False,
                    "PendingSocialActivityTagIds": []
                }
            ],
            "ClientSupportsIrm": True,
            "OutboundCharset": "AutoDetect",
            "PromoteEmojiContentToInlineAttachmentsCount": 0,
            "UnpromotedInlineImageCount": 0,
            "MessageDisposition": "SendAndSaveCopy",
            "ComposeOperation": "newMail"
        }
    }




def send_email():
    email_list=input("\nВведите список получателей (через запятую):\n").split(',')
    topic=input("Введите тему письма:\n")
    text=input("Введите содержимое письма:\n")

    escaped_body = html.escape(text)
    formatted_body = escaped_body.replace('\n', '<br>')

    # формирование HTML-тела письма
    html_text = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <style type="text/css" style="display:none;">
                <!-- P {{margin-top:0;margin-bottom:0;}} -->
            </style>
        </head>
        <body dir="ltr">
            <div id="divtagdefaultwrapper" style="font-size:12pt;color:#000000;font-family:Calibri,Helvetica,sans-serif;" dir="ltr">
                <p>{formatted_body}</p>
            </div>
        </body>
        </html>
        """
    data=create_json(topic,html_text,email_list)

    headers=create_headers.copy()

    timestamp = int(datetime.now().timestamp() * 1000)
    client_request_id = f"{create_cookies['ClientId']}_{timestamp}"

    headers.update({
        'Client-Request-Id': client_request_id,
        'X-Owa-Correlationid': client_request_id,
        'X-Owa-Actionid': str(action_id-1),
        "X-Owa-Clientbegin": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
    })

    response = requests.post(url=create_url, headers=headers, cookies=create_cookies, json=data)
    if response.status_code == 200:
        print("\nПисьмо успешно отправлено\n")
    else:
        print(f'\nПроизошла ошибка: {response.status_code}\n')
    return

def get_emails_list():
    conversations = []
    current_offset = 0
    action_id=-13
    headers = find_headers.copy()

    while True:
        timestamp = int(datetime.now().timestamp() * 1000)
        client_request_id = f"{find_cookies['ClientId']}_{timestamp}"
        action_id-=1

        payload = {
            "__type": "FindConversationJsonRequest:#Exchange",
            "Header": {
                "__type": "JsonRequestHeaders:#Exchange",
                "RequestServerVersion": "V2016_02_03",
                "TimeZoneContext": {
                    "__type": "TimeZoneContext:#Exchange",
                    "TimeZoneDefinition": {
                        "__type": "TimeZoneDefinitionType:#Exchange",
                        "Id": "Russian Standard Time"
                    }
                }
            },
            "Body": {
                "__type": "FindConversationRequest:#Exchange",
                "ParentFolderId": {
                    "__type": "TargetFolderId:#Exchange",
                    "BaseFolderId": {
                        "__type": "DistinguishedFolderId:#Exchange",
                        "Id": "inbox"
                    }
                },
                "ConversationShape": {
                    "__type": "ConversationResponseShape:#Exchange",
                    "BaseShape": "Default"
                },
                "ShapeName": "ConversationListView",
                "Paging": {
                    "__type": "IndexedPageView:#Exchange",
                    "BasePoint": "Beginning",
                    #"MaxEntriesReturned": page_size,
                    "Offset": current_offset
                },
                "ViewFilter": "All",
                "FocusedViewFilter": -1,
                "SortOrder": [
                    {
                        "__type": "SortResults:#Exchange",
                        "Order": "Descending",
                        "Path": {
                            "__type": "PropertyUri:#Exchange",
                            "FieldURI": "ConversationLastDeliveryOrRenewTime"
                        }
                    }
                ]
            }
        }

        payload_json = json.dumps(payload, separators=(',', ':'))  # Компактный JSON
        urlencoded_payload = urllib.parse.quote(payload_json)

        headers.update({
            'Client-Request-Id': client_request_id,
            'X-Owa-Correlationid': client_request_id,
            'X-Owa-Actionid': str(action_id),
            'X-Owa-Clientbegin': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'X-Owa-Actionname': 'Browse_All',
            'X-Owa-Attempt': '1',
            'X-Owa-Urlpostdata': urlencoded_payload
        })

        response = requests.post(
            url=find_url,
            headers=headers,
            cookies=find_cookies,
            json=payload
        )

        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            break

        data = response.json()
        batch = data.get("Body", {}).get("Conversations", [])
        max_count = data.get("Body", {}).get("TotalConversationsInView", "")

        if (len(batch)==0):
            break

        if not batch:
            print("Больше писем нет.")
            break

        conversations.extend(batch)
        if len(conversations)>=max_count:
            break

        current_offset += len(batch)

    return conversations

def print_info(filtered):
    for email in filtered:
        #print("-" * 40)
        print("Тема:", email.get("ConversationTopic", ""))
        print("Отправитель:", ", ".join(email.get("UniqueSenders", [])))
        iso_str = email.get("LastDeliveryTime", "")
        dt = str(datetime.fromisoformat(iso_str))
        print("Дата и время получения письма:", ", ".join(dt.split(' ')))
        flag=email.get("HasAttachments", False)
        #print(flag)
        if (flag==False):
            print("Вложения: отсутствуют\n")
        else:
            attachments=email.get("ItemIds", [])
            print(f'Вложения: {attachments}\n')
        print("Предпросмотр:", email.get("Preview", ""))
        print("-" * 80)
    print(f"\nВсего {len(filtered)} писем.\n")
    return

def print_list_by_filter(number):

    emails_list= get_emails_list()

    match number:
        case 1:
            author=input("Введите имя автора: ").lower()
            filtered_emails=[
                email for email in emails_list
                if any(author in sender.lower() for sender in email.get('UniqueSenders', []))
            ]
            if not filtered_emails:
                print("Писем от указанного автора не найдено.")
                return
            else:
                print_info(filtered_emails)
                return
        case 2:
        #Вы представили ответ на задание
            topic = input("Введите тему: ").lower()
            filtered_emails = [
                email for email in emails_list
                if topic in email.get('ConversationTopic', '').lower()
            ]
            if not filtered_emails:
                print("Не найдены письма с указанной темой.")
                return
            else:
                print_info(filtered_emails) #21.09.2023 2023-09-21
                return
        case 3:
        #2025-03-15
            date = input("Введите дату в формате ГГГГ-ММ-ДД: ")
            filtered_emails = [
                email for email in emails_list
                if date in email.get('LastDeliveryTime', '')
            ]
            if not filtered_emails:
                print("Не найдены письма с указанной датой.")
                return
            else:
                print_info(filtered_emails)
                return
        case 4:
            text = input("Введите ключевое слово: ").lower()
            filtered_emails = [
                email for email in emails_list
                if text in email.get('Preview', '').lower()
            ]
            if not filtered_emails:
                print("Не найдены письма с указанным текстом.")
                return
            else:
                print_info(filtered_emails)
                return
        case 5:
            print_info(emails_list)
        case _:
            print("Некорректный ввод\n")
            return

def main():

    while 1:
        print("Выберите опцию:\n1 - Вывести список писем\n2 - Отправить письмо\n3 - Выход\n")
        num=int(input())
        if num==1:
            print("Выберите тип фильтрации:\n1 - Автор\n2 - Тема\n3 - Дата\n4 - Текст\n5 - Все письма\n")
            num=int(input())
            if (0 < num <= 5):
                print_list_by_filter(num)
            else:
                print("\nНеверный ввод. Попробуйте еще раз.\n")
        elif num==2:
            send_email()
        elif num==3:
            return 0
        else:
            print("\nНеверный ввод. Попробуйте еще раз.\n")

if __name__ == "__main__":
    main()
