baseUrl = "http://127.0.0.1:8080"

async function upload() {
    const res = await fetch(`${baseUrl}/upload`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    }).then(res => res.json())
    return res
}
async function r2Upload(r2SignedUrl, file) {
    const res = await fetch(r2SignedUrl, {
        method: "PUT",
        headers: { "Content-Type": "image/png" },
        body: file,
    })
    return res
}

async function uploadAck(id, file) {
    const res = await fetch(`${baseUrl}/upload/ack`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "id": id,
            "file_type": file.type,
            "display_name": file.name,
        })
    }).then(res => res.json())
    return res
}

const form = document.getElementById("form")

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    let signedUrlRes = await upload();
    console.log(signedUrlRes["r2_upload_url"])
    const file = document.getElementById("file").files[0]
    let r2Res = await r2Upload(signedUrlRes["r2_upload_url"], file)
    let ackRes = await uploadAck(signedUrlRes["id"], file)
})
