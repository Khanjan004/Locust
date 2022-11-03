import csv
from faker import Faker
import json
from faker import Faker
from faker.providers import DynamicProvider


with open('temp.json') as json_file:
    data = json.load(json_file)

def datagenerate(records, headers):
    with open("Fake_data.csv", 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            fake = Faker()

            module_provider = DynamicProvider(
                provider_name = "module",
                elements = data.keys()
            )
            # then add new provider to faker instance
            fake.add_provider(module_provider)
            mod = fake.module()

            sub_module_provider = DynamicProvider(
                    provider_name = "sub_module",
                    elements = data[f'{mod}'].keys()
                )
            # then add new provider to faker instance
            fake.add_provider(sub_module_provider)
            sub_mod = fake.sub_module()

            actions_provider = DynamicProvider(
                provider_name = "actions",
                # elements = [["list","get","create","update","delete"]],
                elements = [data[f'{mod}'][f'{sub_mod}']]
            )
            # then add new provider to faker instance
            fake.add_provider(actions_provider)
            action = fake.actions()

            # if i%500 == 0:
            #     print(i)
            #     print(type(mod))
            #     print(type(sub_mod))
            #     print(type(action))

            writer.writerow({
                "User Id" : i,
                "Module" : mod,
                "Sub Module" : sub_mod,
                "Actions" : action,
                })


if __name__ == '__main__':
    records = 5000
    headers = ["User Id", "Module", "Sub Module", "Actions"]
    datagenerate(records, headers)
    print("CSV generation complete!")