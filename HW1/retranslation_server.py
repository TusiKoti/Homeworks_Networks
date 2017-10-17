# -*- coding: utf-8 -*-

import threading
import time
import SocketServer
import logging
import sys
import socket

import argparse

# глобальные константы
PORT_A = 5001
PORT_B = 5002
OUTPUT_PORT = 5003

# Глобальные переменные, которые вводятся через командную строку
RCVR_ADDR = ""
RCVR_PORT = 0


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    log = logging.getLogger('ThreadedTCPRequestHandler')

    def handle(self):
        data = self.request.recv(1024)
        self.log.info('request from {addr}:{port} to {reciver_addr}:{reciver_port} DATA:"{data}"'.format(
            addr = self.client_address[0],
            port = self.client_address[1],
            data = data,
            reciver_addr = RCVR_ADDR,
            reciver_port = RCVR_PORT))
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('localhost', OUTPUT_PORT))
        udp_socket.sendto(data, (RCVR_ADDR, RCVR_PORT))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def configure_log():
    # create console handler and set level to debug
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    logger = logging.getLogger('run_server')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    logger = logging.getLogger('ThreadedTCPRequestHandler')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


def run_server():
    log = logging.getLogger('run_server')
    HOST = 'localhost'
    port_A = PORT_A
    port_B = PORT_B

    server_A = ThreadedTCPServer((HOST, port_A), ThreadedTCPRequestHandler)
    server_B = ThreadedTCPServer((HOST, port_B), ThreadedTCPRequestHandler)

    server_A_thread = threading.Thread(target=server_A.serve_forever)
    server_B_thread = threading.Thread(target=server_B.serve_forever)

    server_A_thread.setDaemon(True)
    server_B_thread.setDaemon(True)

    log.info('starting thread A...')
    server_A_thread.start()
    log.info('starting thread B...')
    server_B_thread.start()

    while 1:
        time.sleep(1)


def parse_args():
    global RCVR_ADDR, RCVR_PORT
    parser = argparse.ArgumentParser(description="server for tcp packages retranslation  from ports 5001 and 5002")
    parser.add_argument("address", help = "address to retranslate to")
    parser.add_argument("port", help="port to retranslate to")
    args = parser.parse_args()
    RCVR_ADDR = args.address
    RCVR_PORT = int(args.port)


def main():
    parse_args()
    log = logging.getLogger('main')
    configure_log()
    log.info('log is configured')
    log.info('starting server...')
    run_server()


if __name__ == "__main__":
    main()


