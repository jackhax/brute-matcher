import json
from random import randint
import pymysql.cursors
from tabulate import tabulate

name_id = {
    'adn512': 'M. Adnan Jakati',
    'nir451': 'Niranjana Kumaravel',
    'suc785': 'Suchit KumarGS',
    'abh145': 'U S Abhiram',
    'dee412': 'Deeksha D LNU',
    'sur023': 'Suraj Meharwade',
    'ada025': 'Adarsh Shanbhag',
    'pra852': 'Prateek Jain',
    'dil987': 'Abburi Dileep',
    'san951': 'Sai Sanath Erram'
}


def connect(host, user, passw):
    mydb = pymysql.connect(
        host=host,
        user=user,
        password=passw
    )
    return mydb


def match(id):
    db = connect('brute-matcher.cbcy6xtxnhv3.ap-south-1.rds.amazonaws.com', 'admin', '786jak786')
    cursor = db.cursor()
    cursor.execute('use team')
    cursor.execute('select * from match_details where introduced_by = "TBD"')
    to_match = []

    for x in cursor:
        if x[1] != name_id[id]:
            to_match.append(x[1])

    already_selected = []
    cursor.execute('select * from match_details where introducing != "TBD"')
    for x in cursor:
        print(x)
        already_selected.append(x[0])

    if id in already_selected:
        return 'You have used your chance'

    li = to_match
    n = len(li)
    i = randint(0, n - 1)
    matched = to_match[i]
    cursor.execute('use team')
    cursor.execute(f'update match_details set introducing = "{matched}" where mem_id = "{id}"')
    cursor.execute(
        f'update match_details set introduced_by = "{name_id[id]}" where mem_id = "{[x[0] for x in name_id.items() if x[1] == matched][0]}"')
    db.commit()
    return matched


def lambda_handler(event, context):
    body = ""
    action = event['queryStringParameters']['action']
    if action == 'match':
        id = event['queryStringParameters']['id']
        if id not in name_id.keys():
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': json.dumps(f'Invalid ID')
            }
        body = f"Matched with: {match(id)}"
    elif action == 'listall':
        db = connect('brute-matcher.cbcy6xtxnhv3.ap-south-1.rds.amazonaws.com', 'admin', '786jak786')
        cursor = db.cursor()
        cursor.execute('use team')
        cursor.execute('select * from match_details')
        li = cursor.fetchall()
        body = []
        for x in li:
            x = list(x)
            body.append(x)

        body = '<pre>' + tabulate(body, headers=['ID', 'NAME', 'Intorducing', 'Introduced By']) + '</pre>'
        body = body.replace('\n', '<br>')

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(body)
    }
