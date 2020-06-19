def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    import json
    import http.client
    import youtube_dl
    import os
    import urllib.parse

    # Variables to enable cleanup in case of errors
    f = None
    download_target = None

    try:
        if not req:
            raise Exception("No input provided")
        req = json.loads(req)

        if "dav_host" not in req:
            raise Exception("Argument dav_host is required.")
        if "dav_token" not in req:
            raise Exception("Argument dav_token is required.")
        if "video_url" not in req:
            raise Exception("Argument video_url is required.")

        dav_host = req["dav_host"]
        dav_token = req["dav_token"]
        dav_path = req["dav_path"]
        video_url = req["video_url"]
        dav_path = dav_path.strip("/")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo[ext=webm]+bestaudio[ext=webm]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_target = ydl.prepare_filename(info)
            ydl.download([video_url])

        headers = {"Authorization": "Bearer " + dav_token}
        conn = http.client.HTTPSConnection(dav_host)
        f = open(download_target, "rb")
        upload_filename = download_target.encode('ascii', 'ignore').decode("ascii")
        conn.request("PUT", "/remote.php/webdav/" + urllib.parse.quote(dav_path + "/" + upload_filename), body=f, headers=headers)
        response = conn.getresponse()
        if response.getcode() != 201:
            raise Exception("Failed to upload file to DAV server. Response code: " + str(response.getcode()))
        return json.dumps({"fileName": upload_filename, "code": 200})
    except Exception as e:
        return json.dumps({"error": str(e), "code": 500})
    finally:
        if f is not None:
            f.close()
        if download_target is not None and os.path.exists(download_target):
            os.remove(download_target)

