
from flask import jsonify, request
from requests import ConnectionError, Session

class Task:
    @classmethod
    def forward(url, method=None):
        try:
            s = Session()
            if method == 'POST':
                return s.post(url, data=request.data, headers=request.headers)
            elif method == 'GET':
                return s.get(url, headers=request.headers)
            elif method == 'PUT':
                return s.put(url, data=request.data, headers=request.headers)
            elif method == 'DELETE':
                return s.delete(url, headers=request.headers)
        except ConnectionError as e:
            return jsonify({'data': [], 'reason': 'MS unreachable', 'status_code': 503})

