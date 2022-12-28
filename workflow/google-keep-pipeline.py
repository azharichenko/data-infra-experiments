from prefect import flow

from connectors.google import get_keep_data

@flow
def my_favorite_function():
    print("What is your favorite number?")
    return 42

print(my_favorite_function())