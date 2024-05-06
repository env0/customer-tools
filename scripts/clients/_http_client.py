import requests


class HttpClient:
    def send_request(
        self,
        method,
        url,
        headers,
        params=None,
        json_response=False,
    ):
        if not params:
            params={}

        try:
            response = method(
                url=url,
                headers=headers,
                json=params,
                verify=False,
            )
            response.raise_for_status()
        except Exception as e:
            raise e
        else:
            if json_response:
                return response.json()

            return response
