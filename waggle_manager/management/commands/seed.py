import codecs
import csv
import os
import re
import shutil
from datetime import date, datetime

import requests
import pytz
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError

from nodes.models import Tag, Node, Location, Description, SSHConfig


info_url = 'https://www.mcs.anl.gov/research/projects/waggle/downloads/beehive1/node-info.txt'

tarball_url = 'https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.recent.tar'


class Command(BaseCommand):
    def handle(self, *args, **options):
        # self.download_tarball_and_rip_nodes()
        self.get_port_numbers()

    def download_tarball_and_rip_nodes(self):
        self.stdout.write('Downloading chicago tarball and adding nodes, locations and descriptions')

        tarball_name = tarball_url.split('/')[-1]
        
        with requests.get(tarball_url, stream=True) as res:
            with open(tarball_name, 'wb') as fh:
                shutil.copyfileobj(res.raw, fh)
        
        shutil.unpack_archive(tarball_name)
        dirname = f'AoT_Chicago.complete.{date.today()}'

        with codecs.open(f'{dirname}/nodes.csv', 'r', 'utf8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                node = Node.objects.create(id=row['node_id'], vsn=row['vsn'])
                self.stdout.write(f'- created node {node}')

                pt = Point(x=float(row['lon']), y=float(row['lat']), srid=4326)
                Location.objects.create(node=node, location=pt, address=row['address'], effective_as_of=datetime.now().replace(tzinfo=pytz.UTC))
                self.stdout.write('  - created location')

                Description.objects.create(node=node, description=row['description'], effective_as_of=datetime.now().replace(tzinfo=pytz.UTC))
                self.stdout.write('  - created description')
        
        os.remove(tarball_name)
        shutil.rmtree(dirname)

    def get_port_numbers(self):
        self.stdout.write('Downloading node info txt and adding port numbers')

        nodes = dict((n.vsn, n) for n in Node.objects.all())

        with requests.get(info_url) as res:
            for line in res.content.decode('utf8').split('\n'):
                if line.startswith('|'):
                    if line.startswith('| name'):
                        continue
                    
                    parts = [x.strip() for x in line.split('|')]
                    _, vsn, port = parts[:3]

                    if vsn in nodes:
                        node = nodes.get(vsn)
                        SSHConfig.objects.create(node=node, port=port, effective_as_of=datetime.now().replace(tzinfo=pytz.UTC))
                        self.stdout.write(f'- created port for {vsn}')
