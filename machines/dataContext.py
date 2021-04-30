machineContext = {
    'ip':'127.0.0.1',
    'dns': {
        'domains': [
            'domain1.ua.pt',
            'domain2.ua.pt',
            'domain3.ua.pt'
        ]
    },
    'signees': {
        'owners': [
            'owner1@ua.pt',
            'owner2@ua.pt'
        ],
        'subscribers': [
            'subscriber1@ua.pt',
            'subscriber2@ua.pt'
        ],
    },
    'os':'Alpine Linux v3.12',
    'scanLevel':'3',
    'openPorts': [
        {
            'number': 22,
            'description':'ssh',
            'scanEnabled': True,
            'version':'OpenSSH 7.6p1'
        },
        {
            'number': 80,
            'description':'http',
            'scanEnabled': True,
            'version':'nginx'
        },
        {
            'number': 110,
            'description':'pop3',
            'scanEnabled': True,
            'version':'Dovecot pop3d'
        },
        {
            'number': 143,
            'description':'imap',
            'scanEnabled': True,
            'version':'Dovecot imapd'
        },
    ],
    'vulnerabilities': [
        {
            'risk': 1,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain1.ua.pt/some_page?filed=1',
            'status': 'Fixed',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
        {
            'risk': 3,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain1.ua.pt/some_page?filed=1',
            'status': 'Not Fixed',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
        {
            'risk': 1,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain2.ua.pt/some_page?filed=5',
            'status': 'Fixing',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
        {
            'risk': 2,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain1.ua.pt/some_page?filed=2',
            'status': 'Fixed',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
        {
            'risk': 1,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain1.ua.pt/some_page?filed=3',
            'status': 'Fixing',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
        {
            'risk': 3,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain3.ua.pt/some_page?filed=1',
            'status': 'Invalid',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
        {
            'risk': 2,
            'type': 'Injection',
            'description': 'Some description about the vulnerability',
            'location': 'www.domain2.ua.pt/some_page?filed=2',
            'status': 'Not Fixed',
            'comments': [
                {
                    'date': '07/04/2021 10:14',
                    'author': 'owner1@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
                {
                    'date': '05/04/2021 19:04',
                    'author': 'owner2@ua.pt',
                    'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu.'
                },
            ]
        },
    ]
}