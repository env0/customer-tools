class HttpClient:
    def send_request(
        self,
        method,
        url,
        headers,
        params=None,
        json_response=False,
        use_json=True
    ):
        if not params:
            params={}
            
        kwargs = {
            'url': url,
            'headers': headers,
            'verify': False,
            'json' if use_json else 'params': params
        }

        try:
            response = method(
                **kwargs,
            )
            response.raise_for_status()
        except Exception as e:
            raise e
        else:
            if json_response:
                return response.json()

            return response
