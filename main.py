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

find_cookies = {"X-BackEndCookie": "S-1-5-21-1410376585-1421542451-2469044373-147122=u56Lnp2ejJqBxs+Zmciays3SnMjOytLLnsqZ0sfJxsvSz8zPms7PxpmdzJrPgYHNz83K0s7P0s3Lq8/GxcvHxc/H",
                "ClientId": "62046F1A91D347F1BAF69E2AB4DA72FF",
                "X-OWA-JS-PSD": "1",
                "UC": "b5faf18f42c34f7380e973cefac2f9e8",
                "FedAuth": "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U2VjdXJpdHlDb250ZXh0VG9rZW4gcDE6SWQ9Il8zOWJmZWYzOS1iNTRlLTQ0ZGYtOTg3YS00MzdkZTFkODQ1MzQtOTNDQUVCMDY5NUUwRkIyMTFCOEM4NTFFRUUyMTRCRDQiIHhtbG5zOnAxPSJodHRwOi8vZG9jcy5vYXNpcy1vcGVuLm9yZy93c3MvMjAwNC8wMS9vYXNpcy0yMDA0MDEtd3NzLXdzc2VjdXJpdHktdXRpbGl0eS0xLjAueHNkIiB4bWxucz0iaHR0cDovL2RvY3Mub2FzaXMtb3Blbi5vcmcvd3Mtc3gvd3Mtc2VjdXJlY29udmVyc2F0aW9uLzIwMDUxMiI+PElkZW50aWZpZXI+dXJuOnV1aWQ6NmM5YzY2OTItYzMwMy00NGU2LThjMDYtYTY2ZTk5MjcyZTFkPC9JZGVudGlmaWVyPjxJbnN0YW5jZT51cm46dXVpZDpiMzVhYTZjOS0zZjU4LTQzZWMtOWIwMi02MTBkNjI0NWZiMTc8L0luc3RhbmNlPjxDb29raWUgeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwNi8wNS9zZWN1cml0eSI+M3NkWjZlTFBUWGZqMlNyZnRQR3kzZGtIZGhZQkF1NG9SYU1oMTcvYXBwZ0FBUUFBV1BDdkh5OWtUbGtWL1NQT0lwNkJmS1dKb1ZIY3pwQVBWYjFOSlpVbjRkSEtyVGoyS2U2eVFDSmE0NHVUZnRObzZ4ZS9OM2VNZ1YrY0pDRUVOTjRHZmozcElUWDdlRkx2THhMb3gyRGhBOHJrRDl1VG9URlo4T3N6Y1BNUWl3SVVITDNMNUY5b1VYRUdKQ08wbDliV3RNWUNHS1N0WFd1cnZlUENNMzFFTlcwTWk4TGtNeHBxMDZ4WWljcHpJL2FTYUNKUXlBbjdOenJTdXBxcDZSMUJqQWhqRmNKS01FMFpzMHBwa1pIcGM1M2JJQzR1Y3V5enZ4aERjUWU2Q3hhL2JheEkvY1VDZmlPUnV2VjZQZ0R2dTE4SC9NNXFRd1ZYNndMWlBxajY3RkMyK1dVN2pmYVJUNnlRdkFNTWc5dDd1NmJYRmlIOXRLTmFuckxCSEVQNExLQURBQUJUVDNiZU1ySkZhMUVBZmFyeXFqMkVaeEpNRmNISUxhdTQyVjBycnk5SnBENUFHQlRPbFUxRE1nMExTU2Fvdm1FWVNKT21vUkRaaWlPU3Fqc2c1ZC8xVEhZM3pYNmdzWTVwRHBBUUVZcUN0VE1qZHBsOEhNMFE5T0RyT2htb1lZdXd6bXRocXdqU211ZHFZcnNwckFXQmEyS3FIbE9KMUZyNHBOWW1TYVo4VERTNG5TMTY2ZkpUQkQwUUxILytGK2JzbUZBNzZINjV6M3MxeXA0VUI5S1h5Q3JmSUhUZHIzYzYzb2VBZU51amozWHZrc3dzYmF4bU5Dc05taW1Cb1JJZzdyQThrbjNNZ3NEYlZRL3hSQmw5Q09aTURPbERTUmlYZ1lySS9SdjA3QkJRdXlCZTdKUWFtN24wM1ppdnNlYnlTL1RPVHlTQUVQUDVNcWtwendkSmExa05JY0pvcmVEd1dWWC9sNGZOR1kwcjh6dndwb2F0Rko5b1FVS2ZvbElBMkZOc2c1VkhPTHE5TVZvazRhdW4xN0wzeUFlNDhtallqbUdORC9DNTBRSlhJN0Jab2s0d205UFNrTldGZHA1U3NNTThaVVJTUFd4bXRVVldNRjdpT0MwVTRMVWkyTGQrWFUzQWVqVG0rdG1GNGdHUVdoLzB5OTlmditxd1N6T2xZMGNVNHlhdS9HM0QyYlg5a2tpWXp2K1JVaXRTdlcvR0tEU2JSdzViSTdIVVc1MHBlMUphSEpZMmtTZEJrNWZTeXBlYUhVV3hsRHhyY1k2Y3BiZzQr",
                "FedAuth1": "ZkdTWFIyZVhTMThnQWxNS0c4eElUWW1kenNBb0d2ZCtFbzM3Skc5YWVORS8yUFhIYmVCZlphWXNacGZBQi9HcVB6Nk03V05MK1NmMnBEc2hFSVh1Q2FQSEVhUjFUa1VlVVQ4a2M2Nyt1SFVkclpSK1ZPSVpoV0J1OVBZZFN6dUt6S2N0MldDVkJhZitLSEg3U29XUFBJNTkvN1cxWFlkelhnQ2d6OHpZU3crb1JZcUFoQlUzQlFobC95YWFBOVVzbUNFTU05R1dUUjJhbW95SkhBNnRVbTNkeHNMeHpwV0NHWlV5d0Y2TzRNcWVDWmFNSjl4enVlaGwwTVdBcURqd1M5VEhYaGQ0Q2pwcVJCTXROd0VBaGkwSks1TGVEQUNVcndTRmc4WWNsclM4L0hUQzBQVUtZTFZNSC9walVUNy9iSE9JbVBRWWhGUVVUQlV0ZVhzanpkanBDSDcveWNBRloySjBGOUR0Mjh2azV0MlNQeVRZeFdDWEpsRGxoSHVFS1ROejl1bnIyWUE2ZFY1bUxncTYxUEFLNWRjM0V0dHNCQjdQdlR3OHh6SDFuS20rNDEvTlhaamU1YzBQWjNtd3VQL0tDdTBTUTJiZkwvS1YxMGg0a21IaHRkMlZPTzVTeHRjWitTejBwTHVpc3lGSExJS0JVTzBBZG5iVWFNK0lCZGkzQVRxYldKSmJ5cjdYaWZHU3l1TG1CakVTTFp6ZldNVnRBY0IvN09LM3VRTTRnNE5SSVg2bXlJanRZRHF5bnBtVGV3djZrTjBZVHA3MWJQeVIwblVQV2crTG1PbW9qVTJyUVpWdUlhdHUwWTh2eXFlczNscmltamJ6Si9CPC9Db29raWU+PC9TZWN1cml0eUNvbnRleHRUb2tlbj4=",
                "TimeWindow": "6Frp6Y0tKhLI6ZMi6fJfGMLJ1wq+f5h+T/ZLGjIALlnVFTEIZAeLvmUdg5Ql7zldm2sYoHQ/JDPUSciogouhErMkjBbfHDBFn0TVHZnqS/c=",
                "TimeWindowKey": "MmFv7OcFKFxzoV6X0Jq+/ErByguHRel9jzFyBhlRdV5nZVG5ANVVKQyBf6mwYOw5uvuxOmOETamFJKPaMdabNmf1+T96vLA5Z57Xe06zQx2YA+1bvE5SZpEPdq/Rbwsoe8nNYxlCo8HLkMyQaXrG8fDhXMq7gDvm+h4XhpNTYPg0AjQH7ihMIAifR1lTB9D5lwURMA12oI2PhAQG0XLZMfFOmp2ZBKgpxBcFoyuDkogdTkXcOjmw3YlLHFTuVQT4xKMlStsSICyd10Eozt/6XXzJ4KRO3BUNUIDLGBuFGzE1ECt/ZDvZplKpO3c5bONArZyQ8DtlG3Fkf0vR3i5FIQ==",
                "TimeWindowIV": "fHKpTO0i9jBkb3C3R7J0ZILAqj3qSA6nRYHxHNOjFtbQxh5DVDHu77pCbAFzOvHIcBogBsVv1wRU7MdmKZygO2QYvBnc1TQsLrFpJEpNDfLhUh6NnDgd1+18dNci/aMi48qhXNGaZm0X3L0EfEGE2SkK9fb6a2LzEPPuQcVoXkWbQguqBZCBkOuFXM8iaLS9tL0abU+2vU/18uu/wDq3OzbRU2MJNnnDoHdDGVd1GWEXoFSKuLdKvZK4FXYz1AyaHwo0IbMfDkQxNALXNnlFyVVdsPJK3daPgVp9jByLJ+2x2Y0WZ3o+Jwm6JgO26tCfiPugpfXTW4Z6tkW+GQ0cWw==",
                "TimeWindowSig": "YThjyhelkfYSU/d+g03wPWFTRNpQI9oYiJlgESZm/5fP0TTVfNncrrJhq4TVRDZukvwJ0sKorGyj6FeMItcMIfCID/XtiHRCEAVJz2uB2D6vSoqV8xOli1EZRZXxdCF8GPxMUnFCqX2mMZUkQ/ZancOlmzJPSW3JEG260d6wIfWrTk9NRaPB4C5hB+Wa+AiSVohzYofj0dUBRnyP00e8R/X95RZDtVM20ohtLYx8Pys+rhugsv3H5StQBXbD4Q4cO5hvFRNL8nyyj24PNPKctZ0yjXKANl73p6zeoSBr/ApPCLjNwVou9GczolChTPu/O3UlKs6R7hs78Sxa8oShVQ==",
                "X-OWA-CANARY":"Yyabj4txSUmLQ-k8P8jCNpANh3BP-90Ivffi9wHWhZcl8nFhPP8n4i7CT-k9X9Dso15AVleQu1U."}

find_headers = {
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/json; charset=UTF-8',
        'X-Owa-Actionname':'Browse_All',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'X-Owa-Correlationid': "62046F1A91D347F1BAF69E2AB4DA72FF_175870728876026", ##
        'Action':'FindConversation',
        'Accept-Language':'ru-RU,ru;q=0.9',
        'X-Owa-Canary':'Yyabj4txSUmLQ-k8P8jCNpANh3BP-90Ivffi9wHWhZcl8nFhPP8n4i7CT-k9X9Dso15AVleQu1U.',
        'X-Owa-Urlpostdata': '%7B%22__type%22%3A%22FindConversationJsonRequest%3A%23Exchange%22%2C%22Header%22%3A%7B%22__type%22%3A%22JsonRequestHeaders%3A%23Exchange%22%2C%22RequestServerVersion%22%3A%22V2016_02_03%22%2C%22TimeZoneContext%22%3A%7B%22__type%22%3A%22TimeZoneContext%3A%23Exchange%22%2C%22TimeZoneDefinition%22%3A%7B%22__type%22%3A%22TimeZoneDefinitionType%3A%23Exchange%22%2C%22Id%22%3A%22Russian%20Standard%20Time%22%7D%7D%7D%2C%22Body%22%3A%7B%22__type%22%3A%22FindConversationRequest%3A%23Exchange%22%2C%22ParentFolderId%22%3A%7B%22__type%22%3A%22TargetFolderId%3A%23Exchange%22%2C%22BaseFolderId%22%3A%7B%22__type%22%3A%22DistinguishedFolderId%3A%23Exchange%22%2C%22Id%22%3A%22sentitems%22%7D%7D%2C%22ConversationShape%22%3A%7B%22__type%22%3A%22ConversationResponseShape%3A%23Exchange%22%2C%22BaseShape%22%3A%22IdOnly%22%7D%2C%22ShapeName%22%3A%22ConversationSentItemsListView%22%2C%22Paging%22%3A%7B%22__type%22%3A%22IndexedPageView%3A%23Exchange%22%2C%22BasePoint%22%3A%22Beginning%22%2C%22Offset%22%3A0%2C%22MaxEntriesReturned%22%3A25%7D%2C%22ViewFilter%22%3A%22All%22%2C%22FocusedViewFilter%22%3A-1%2C%22SortOrder%22%3A%5B%7B%22__type%22%3A%22SortResults%3A%23Exchange%22%2C%22Order%22%3A%22Descending%22%2C%22Path%22%3A%7B%22__type%22%3A%22PropertyUri%3A%23Exchange%22%2C%22FieldURI%22%3A%22ConversationLastDeliveryTime%22%7D%7D%5D%7D%7D',
        'Client-Request-Id': "62046F1A91D347F1BAF69E2AB4DA72FF_175870728876026", ##
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
    "X-BackEndCookie":"S-1-5-21-1410376585-1421542451-2469044373-147122=u56Lnp2ejJqBxs+Zmciays3SnMjOytLLnsqZ0sfJxsvSz8zPms7PxpmdzJrPgYHNz83K0s7P0s3Lq8/GxcrMxc/N",
    "ClientId":"62046F1A91D347F1BAF69E2AB4DA72FF",
    "FedAuth":"77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U2VjdXJpdHlDb250ZXh0VG9rZW4gcDE6SWQ9Il8zOWJmZWYzOS1iNTRlLTQ0ZGYtOTg3YS00MzdkZTFkODQ1MzQtOTNDQUVCMDY5NUUwRkIyMTFCOEM4NTFFRUUyMTRCRDQiIHhtbG5zOnAxPSJodHRwOi8vZG9jcy5vYXNpcy1vcGVuLm9yZy93c3MvMjAwNC8wMS9vYXNpcy0yMDA0MDEtd3NzLXdzc2VjdXJpdHktdXRpbGl0eS0xLjAueHNkIiB4bWxucz0iaHR0cDovL2RvY3Mub2FzaXMtb3Blbi5vcmcvd3Mtc3gvd3Mtc2VjdXJlY29udmVyc2F0aW9uLzIwMDUxMiI+PElkZW50aWZpZXI+dXJuOnV1aWQ6NmM5YzY2OTItYzMwMy00NGU2LThjMDYtYTY2ZTk5MjcyZTFkPC9JZGVudGlmaWVyPjxJbnN0YW5jZT51cm46dXVpZDpiMzVhYTZjOS0zZjU4LTQzZWMtOWIwMi02MTBkNjI0NWZiMTc8L0luc3RhbmNlPjxDb29raWUgeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwNi8wNS9zZWN1cml0eSI+M3NkWjZlTFBUWGZqMlNyZnRQR3kzZGtIZGhZQkF1NG9SYU1oMTcvYXBwZ0FBUUFBV1BDdkh5OWtUbGtWL1NQT0lwNkJmS1dKb1ZIY3pwQVBWYjFOSlpVbjRkSEtyVGoyS2U2eVFDSmE0NHVUZnRObzZ4ZS9OM2VNZ1YrY0pDRUVOTjRHZmozcElUWDdlRkx2THhMb3gyRGhBOHJrRDl1VG9URlo4T3N6Y1BNUWl3SVVITDNMNUY5b1VYRUdKQ08wbDliV3RNWUNHS1N0WFd1cnZlUENNMzFFTlcwTWk4TGtNeHBxMDZ4WWljcHpJL2FTYUNKUXlBbjdOenJTdXBxcDZSMUJqQWhqRmNKS01FMFpzMHBwa1pIcGM1M2JJQzR1Y3V5enZ4aERjUWU2Q3hhL2JheEkvY1VDZmlPUnV2VjZQZ0R2dTE4SC9NNXFRd1ZYNndMWlBxajY3RkMyK1dVN2pmYVJUNnlRdkFNTWc5dDd1NmJYRmlIOXRLTmFuckxCSEVQNExLQURBQUJUVDNiZU1ySkZhMUVBZmFyeXFqMkVaeEpNRmNISUxhdTQyVjBycnk5SnBENUFHQlRPbFUxRE1nMExTU2Fvdm1FWVNKT21vUkRaaWlPU3Fqc2c1ZC8xVEhZM3pYNmdzWTVwRHBBUUVZcUN0VE1qZHBsOEhNMFE5T0RyT2htb1lZdXd6bXRocXdqU211ZHFZcnNwckFXQmEyS3FIbE9KMUZyNHBOWW1TYVo4VERTNG5TMTY2ZkpUQkQwUUxILytGK2JzbUZBNzZINjV6M3MxeXA0VUI5S1h5Q3JmSUhUZHIzYzYzb2VBZU51amozWHZrc3dzYmF4bU5Dc05taW1Cb1JJZzdyQThrbjNNZ3NEYlZRL3hSQmw5Q09aTURPbERTUmlYZ1lySS9SdjA3QkJRdXlCZTdKUWFtN24wM1ppdnNlYnlTL1RPVHlTQUVQUDVNcWtwendkSmExa05JY0pvcmVEd1dWWC9sNGZOR1kwcjh6dndwb2F0Rko5b1FVS2ZvbElBMkZOc2c1VkhPTHE5TVZvazRhdW4xN0wzeUFlNDhtallqbUdORC9DNTBRSlhJN0Jab2s0d205UFNrTldGZHA1U3NNTThaVVJTUFd4bXRVVldNRjdpT0MwVTRMVWkyTGQrWFUzQWVqVG0rdG1GNGdHUVdoLzB5OTlmditxd1N6T2xZMGNVNHlhdS9HM0QyYlg5a2tpWXp2K1JVaXRTdlcvR0tEU2JSdzViSTdIVVc1MHBlMUphSEpZMmtTZEJrNWZTeXBlYUhVV3hsRHhyY1k2Y3BiZzQr",
    "FedAuth1":"ZkdTWFIyZVhTMThnQWxNS0c4eElUWW1kenNBb0d2ZCtFbzM3Skc5YWVORS8yUFhIYmVCZlphWXNacGZBQi9HcVB6Nk03V05MK1NmMnBEc2hFSVh1Q2FQSEVhUjFUa1VlVVQ4a2M2Nyt1SFVkclpSK1ZPSVpoV0J1OVBZZFN6dUt6S2N0MldDVkJhZitLSEg3U29XUFBJNTkvN1cxWFlkelhnQ2d6OHpZU3crb1JZcUFoQlUzQlFobC95YWFBOVVzbUNFTU05R1dUUjJhbW95SkhBNnRVbTNkeHNMeHpwV0NHWlV5d0Y2TzRNcWVDWmFNSjl4enVlaGwwTVdBcURqd1M5VEhYaGQ0Q2pwcVJCTXROd0VBaGkwSks1TGVEQUNVcndTRmc4WWNsclM4L0hUQzBQVUtZTFZNSC9walVUNy9iSE9JbVBRWWhGUVVUQlV0ZVhzanpkanBDSDcveWNBRloySjBGOUR0Mjh2azV0MlNQeVRZeFdDWEpsRGxoSHVFS1ROejl1bnIyWUE2ZFY1bUxncTYxUEFLNWRjM0V0dHNCQjdQdlR3OHh6SDFuS20rNDEvTlhaamU1YzBQWjNtd3VQL0tDdTBTUTJiZkwvS1YxMGg0a21IaHRkMlZPTzVTeHRjWitTejBwTHVpc3lGSExJS0JVTzBBZG5iVWFNK0lCZGkzQVRxYldKSmJ5cjdYaWZHU3l1TG1CakVTTFp6ZldNVnRBY0IvN09LM3VRTTRnNE5SSVg2bXlJanRZRHF5bnBtVGV3djZrTjBZVHA3MWJQeVIwblVQV2crTG1PbW9qVTJyUVpWdUlhdHUwWTh2eXFlczNscmltamJ6Si9CPC9Db29raWU+PC9TZWN1cml0eUNvbnRleHRUb2tlbj4=",
    "UC":"b5faf18f42c34f7380e973cefac2f9e8",
    "X-OWA-JS-PSD":"1",
    "TimeWindow":"6Frp6Y0tKhLI6ZMi6fJfGMLJ1wq+f5h+T/ZLGjIALlnVFTEIZAeLvmUdg5Ql7zldm2sYoHQ/JDPUSciogouhErMkjBbfHDBFn0TVHZnqS/c=",
    "TimeWindowKey":"MmFv7OcFKFxzoV6X0Jq+/ErByguHRel9jzFyBhlRdV5nZVG5ANVVKQyBf6mwYOw5uvuxOmOETamFJKPaMdabNmf1+T96vLA5Z57Xe06zQx2YA+1bvE5SZpEPdq/Rbwsoe8nNYxlCo8HLkMyQaXrG8fDhXMq7gDvm+h4XhpNTYPg0AjQH7ihMIAifR1lTB9D5lwURMA12oI2PhAQG0XLZMfFOmp2ZBKgpxBcFoyuDkogdTkXcOjmw3YlLHFTuVQT4xKMlStsSICyd10Eozt/6XXzJ4KRO3BUNUIDLGBuFGzE1ECt/ZDvZplKpO3c5bONArZyQ8DtlG3Fkf0vR3i5FIQ==",
    "TimeWindowIV":"fHKpTO0i9jBkb3C3R7J0ZILAqj3qSA6nRYHxHNOjFtbQxh5DVDHu77pCbAFzOvHIcBogBsVv1wRU7MdmKZygO2QYvBnc1TQsLrFpJEpNDfLhUh6NnDgd1+18dNci/aMi48qhXNGaZm0X3L0EfEGE2SkK9fb6a2LzEPPuQcVoXkWbQguqBZCBkOuFXM8iaLS9tL0abU+2vU/18uu/wDq3OzbRU2MJNnnDoHdDGVd1GWEXoFSKuLdKvZK4FXYz1AyaHwo0IbMfDkQxNALXNnlFyVVdsPJK3daPgVp9jByLJ+2x2Y0WZ3o+Jwm6JgO26tCfiPugpfXTW4Z6tkW+GQ0cWw==",
    "TimeWindowSig":"YThjyhelkfYSU/d+g03wPWFTRNpQI9oYiJlgESZm/5fP0TTVfNncrrJhq4TVRDZukvwJ0sKorGyj6FeMItcMIfCID/XtiHRCEAVJz2uB2D6vSoqV8xOli1EZRZXxdCF8GPxMUnFCqX2mMZUkQ/ZancOlmzJPSW3JEG260d6wIfWrTk9NRaPB4C5hB+Wa+AiSVohzYofj0dUBRnyP00e8R/X95RZDtVM20ohtLYx8Pys+rhugsv3H5StQBXbD4Q4cO5hvFRNL8nyyj24PNPKctZ0yjXKANl73p6zeoSBr/ApPCLjNwVou9GczolChTPu/O3UlKs6R7hs78Sxa8oShVQ==",
    "X-OWA-CANARY":"Yyabj4txSUmLQ-k8P8jCNpANh3BP-90Ivffi9wHWhZcl8nFhPP8n4i7CT-k9X9Dso15AVleQu1U."
}

create_headers={
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
    'X-Owa-Serviceunavailableontransienterror':'true',
    'Sec-Ch-Ua-Mobile': '?0',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/json; charset=UTF-8',
    'X-Owa-Actionname':'CreateMessageForComposeSend',
    'X-Owa-Correlationid':'62046F1A91D347F1BAF69E2AB4DA72FF_175870760218435', ##
    'Action':'CreateItem',
    'Accept-Language':'ru-RU,ru;q=0.9',
    'X-Owa-Canary':'il9lwFtOD06w9Ak_uQjP2uDQXQqW-t0IPSQijdM4tAJSm1W3FnZwsv80bd-K5ugwYugWVyDWXTo.',
    'Client-Request-Id':'62046F1A91D347F1BAF69E2AB4DA72FF_175870760218435', ##
    'X-Owa-Clientbuildversion':'15.2.1258.34',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
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
