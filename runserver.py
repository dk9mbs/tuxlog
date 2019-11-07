#!/usr/bin/env python
# coding: utf-8
from common.app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
