machineContext = {
    'machine': {        
        'ip':'127.0.0.1',
        'domains': [
            'domain1.ua.pt',
            'domain2.ua.pt',
            'domain3.ua.pt'
        ],
        'owners': [
            'owner1@ua.pt',
            'owner2@ua.pt'
        ],
        'subscribers': [
            'subscriber1@ua.pt',
            'subscriber2@ua.pt'
        ],
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
                ]
            },
            {
                'risk': 2,
                'type': 'Injection',
                'description': 'Some description about the vulnerability',
                'location': 'www.domain2.ua.pt/some_page?filed=2',
                'status': 'Not Fixed',
                'comments': [
                ]
            },
        ]
    },
    'requests': [
        {
            'subscriber': 'subscriber1@ua.pt',
            'ip': '127.0.0.1',
            'domains': [
                'domain1.ua.pt',
                'domain2.ua.pt'
            ],
            'motive': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu. Aliquam sollicitudin cursus maximus. Maecenas vestibulum blandit enim eget placerat. Suspendisse cursus purus lorem, sit amet iaculis justo porttitor ac. Donec sem enim, interdum ut tincidunt vel, rhoncus non turpis. Praesent id justo consequat, luctus purus id, efficitur ligula. Aliquam et ipsum nibh. Sed efficitur urna ultricies bibendum bibendum.'
        },
        {
            'subscriber': 'subscriber2@ua.pt',
            'ip': '127.0.0.2',
            'domains': [
                'domain3.ua.pt',
            ],
            'motive': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu. Aliquam sollicitudin cursus maximus. Maecenas vestibulum blandit enim eget placerat. Suspendisse cursus purus lorem, sit amet iaculis justo porttitor ac. Donec sem enim, interdum ut tincidunt vel, rhoncus non turpis. Praesent id justo consequat, luctus purus id, efficitur ligula. Aliquam et ipsum nibh. Sed efficitur urna ultricies bibendum bibendum.'
        },
        {
            'subscriber': 'subscriber3@ua.pt',
            'ip': '127.0.0.3',
            'domains': [
                'domain4.ua.pt',
                'domain5.ua.pt',
                'domain6.ua.pt'
            ],
            'motive': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu. Aliquam sollicitudin cursus maximus. Maecenas vestibulum blandit enim eget placerat. Suspendisse cursus purus lorem, sit amet iaculis justo porttitor ac. Donec sem enim, interdum ut tincidunt vel, rhoncus non turpis. Praesent id justo consequat, luctus purus id, efficitur ligula. Aliquam et ipsum nibh. Sed efficitur urna ultricies bibendum bibendum.'
        },
        {
            'subscriber': 'subscriber4@ua.pt',
            'ip': '127.0.0.4',
            'domains': [
                'domain7.ua.pt',
                'domain8.ua.pt'
            ],
            'motive': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu. Aliquam sollicitudin cursus maximus. Maecenas vestibulum blandit enim eget placerat. Suspendisse cursus purus lorem, sit amet iaculis justo porttitor ac. Donec sem enim, interdum ut tincidunt vel, rhoncus non turpis. Praesent id justo consequat, luctus purus id, efficitur ligula. Aliquam et ipsum nibh. Sed efficitur urna ultricies bibendum bibendum.'
        },
        {
            'subscriber': 'subscriber5@ua.pt',
            'ip': '127.0.0.5',
            'domains': [
                'domain9.ua.pt',
            ],
            'motive': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu. Aliquam sollicitudin cursus maximus. Maecenas vestibulum blandit enim eget placerat. Suspendisse cursus purus lorem, sit amet iaculis justo porttitor ac. Donec sem enim, interdum ut tincidunt vel, rhoncus non turpis. Praesent id justo consequat, luctus purus id, efficitur ligula. Aliquam et ipsum nibh. Sed efficitur urna ultricies bibendum bibendum.'
        },
        {
            'subscriber': 'subscriber6@ua.pt',
            'ip': '127.0.0.6',
            'domains': [
                'domain10.ua.pt',
            ],
            'motive': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dolor ipsum, molestie eu sem in, vulputate molestie mi. Donec a fringilla arcu. Aliquam sollicitudin cursus maximus. Maecenas vestibulum blandit enim eget placerat. Suspendisse cursus purus lorem, sit amet iaculis justo porttitor ac. Donec sem enim, interdum ut tincidunt vel, rhoncus non turpis. Praesent id justo consequat, luctus purus id, efficitur ligula. Aliquam et ipsum nibh. Sed efficitur urna ultricies bibendum bibendum.'
        },
    ]
}