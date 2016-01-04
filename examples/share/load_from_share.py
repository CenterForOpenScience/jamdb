import json
import hashlib
import requests


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0NDc3Nzk5MDgsInN1YiI6InRyYWNrZWQtU0hBUkV8dXNlcnMtY2hyaXMifQ.kVvJaZcIDDIzNb5hyey_7YqsrfZurZcqMH65aRysq_4'

times = []


def main():
    for x in range(0, 500000, 100):
        response = requests.get('https://staging.osf.io/api/v1/share/search/?size=100&from={}'.format(x))
        for result in response.json()['results']:
            docId = hashlib.sha1('{}{}'.format(result['shareProperties']['source'], result['shareProperties']['docID']).encode('utf-8')).hexdigest()
            result['contributors'] = [
                requests.post(
                    'http://localhost:1212/v1/namespaces/SHARE/collections/authors/documents',
                    json={'data': {
                        'type': 'documents',
                        'attributes': {**contrib, 'sourceDocument': docId}
                    }}, cookies={'cookie': token}).json()['data']
                for contrib in result['contributors']
            ]

            resp = requests.post(
                'http://localhost:1212/v1/namespaces/SHARE/collections/normalized/documents',
                data=json.dumps({'data': {
                    'id': docId,
                    'type': 'documents',
                    'attributes': result
                }}), cookies={
                    'cookie': token
                })

            try:
                assert resp.status_code in (201, 409)
                times.append(resp.elapsed.microseconds/1000)
                if resp.elapsed.microseconds > 50000:
                    print('{} {:.3f} ms'.format(result['shareProperties']['docID'], resp.elapsed.microseconds/1000))
            except AssertionError:
                print('FAILED ON {}: {}'.format(result['shareProperties']['docID'], resp.status_code))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Average: {}\nMax: {}\nMin: {}\nSize: {}'.format(sum(times)/len(times), max(times), min(times), len(times)))
