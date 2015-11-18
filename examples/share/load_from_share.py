import json
import requests


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0NDc3Nzk5MDgsInN1YiI6InRyYWNrZWQtU0hBUkV8dXNlcnMtY2hyaXMifQ.kVvJaZcIDDIzNb5hyey_7YqsrfZurZcqMH65aRysq_4'


def main():
    for x in range(0, 50000, 100):
        response = requests.get('https://staging.osf.io/api/v1/share/search/?size=100&from={}'.format(x))
        for result in response.json()['results']:
            resp = requests.post(
                'http://localhost:1212/v1/namespaces/SHARE/collections/share-data/documents',
                data=json.dumps({'data': {
                    'id': result['shareProperties']['docID'],
                    'type': 'document',
                    'attributes': result
                }}), cookies={
                    'cookie': token
                })
            try:
                assert resp.status_code in (201, 409)
            except AssertionError:
                print('{}: {}'.format(result['shareProperties']['docID'], resp.status_code))


if __name__ == '__main__':
    main()
