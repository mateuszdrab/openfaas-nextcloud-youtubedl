# openfaas-nextcloud-youtubedl
A function for OpenFaaS to download videos using YouTube-DL and upload them into NextCloud

Your OpenFaaS environment will need to be configured to allow long timeouts.

## Configure
Set `<registry>` in `nextcloud-youtubedl.yml` to a registry you can push to.

## Build
`faas-cli up -f nextcloud-youtubedl.yml --build-arg ADDITIONAL_PACKAGE=ffmpeg`

## Invoke
Use the example JSON to invoke the function
`
{
	"dav_host": "",
	"dav_token": "",
	"dav_path": "",
	"video_url": ""
}
`
