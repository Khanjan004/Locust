
import json
from faker import Faker
from faker.providers import DynamicProvider

fake = Faker()

with open('temp.json') as json_file:
    data = json.load(json_file)


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


# now you can use:
print(mod)
print(sub_mod)
print(action)