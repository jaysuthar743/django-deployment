import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')

import django
django.setup()


## fake script
import random

from first_app.models import AccessRecord, WebPage, Topic
from faker import Faker

fakegen = Faker()
topic = ['Search', 'Social', 'MarketPlace', 'News', 'Games']


def add_topic():
    t = Topic.objects.get_or_create(top_name = random.choice(topic))[0]
    print("t: ",t)
    t.save()
    return t

def populate(N=5):
    for entry in range(N):

        # get the topic for the entry
        top = add_topic()

        # create the fake date for that entry
        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        # craete new webPage entry
        webpg = WebPage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]

        #craeet fake AccessRecord
        acc_rec = AccessRecord.objects.get_or_create(name=webpg,  date=fake_date)[0]

if __name__ == '__main__':
    print("Populating Script")
    populate(20)
    print("Populating Complete")
