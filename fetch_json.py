from mitmproxy import http

def response(flow: http.HTTPFlow):
    """
    Intercepts URLs and writes the link to the JSON file into a log.
    """
    # Check if the URL contains the JSON file (in this case, ending with playlist.json)
    if "vimeocdn.com" in flow.request.pretty_url and "playlist.json" in flow.request.pretty_url:
        # Write the URL to a file
        with open("json_link.log", "w") as f:
            f.write(flow.request.pretty_url + "\n")
