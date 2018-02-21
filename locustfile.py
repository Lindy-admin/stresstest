import random

from faker import Faker
from locust import HttpLocust
from locust import TaskSet
from locust import task

tenants = ["c56uegGcVZUMuml27XBpgw", "LECqBnvn_cWOZIC73zyQOg"]
roles = [True, False]

class RegisterTaskSet(TaskSet):

    def __init__(self, parent):
        super(RegisterTaskSet, self).__init__(parent)
        self.fake = Faker()

    def get_tenant(self):
        return random.choice(tenants)

    def get_course(self, tenant):
        url = "/api/{}/courses".format(tenant)
        response = self.client.get(url)
        courses = response.json()

        return random.choice(courses)

    def get_ticket(self, tenant, course):
        url = "/api/{}/courses/{}".format(tenant, course["id"])
        response = self.client.get(url)
        course = response.json()
        tickets = course["tickets"]

        return random.choice(tickets)

    @task(1)
    def register(self):
        tenant = self.get_tenant()
        course = self.get_course(tenant)
        ticket = self.get_ticket(tenant, course)

        role = random.choice(roles)
        firstname = self.fake.first_name()
        lastname = self.fake.last_name()
        email = self.fake.email()
        note = self.fake.text()

        url = "/api/{}/register".format(tenant)
        payload = {
            "course": course["id"],
            "ticket": ticket["id"],
            "role": role,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "additional[note]": note
        }
        self.client.post(url, json=payload)


class WebsiteUser(HttpLocust):
    task_set = RegisterTaskSet
    min_wait = 5000
    max_wait = 9000
