baseUrl = "http://127.0.0.1:8080"

async function upload() {
    const res = await fetch(`${baseUrl}/file/upload`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    }).then(res => res.json())
    return res
}

async function uploadAck(id, file) {
    const res = await fetch(`${baseUrl}/file/upload:ack`, {
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

async function listFiles() {
    const res = await fetch(`${baseUrl}/folders/root/files`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    }).then(res => res.json())
    return res
}

async function getFile(id) {
    const res = await fetch(`${baseUrl}/folders/root/files/${id}`, {
        method: "GET",
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

async function dbUpload(signedUrl, file) {
    thumbnail = await getThumbnailFile(file)
    const res = await fetch(signedUrl, {
        method: "POST",
        headers: { "Content-Type": "application/octet-stream" },
        body: thumbnail,
    })
    return res
}

async function getThumbnailFile(file) {
    filePath = URL.createObjectURL(file)
    original = await Jimp.read(filePath)
    thumbnail = await original.resize(50, Jimp.AUTO)
    data = await thumbnail.getBufferAsync(Jimp.MIME_PNG)
    return new File([data], "", {type: "image/png"})
}

const form = document.getElementById("form")

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    let signedUrlRes = await upload();
    console.log(signedUrlRes["r2_upload_url"])
    const file = document.getElementById("file").files[0]
    let r2Res = await r2Upload(signedUrlRes["r2_upload_url"], file)
    let dbRes = await dbUpload(signedUrlRes["db_upload_url"], file)
    let ackRes = await uploadAck(signedUrlRes["id"], file)
})

let grid = document.getElementById("grid")

async function showHandler() {
    data = await listFiles()
    data.forEach((item) => {
        img = document.createElement("img")
        img.src = item["url"]
        filename = document.createElement("p")
        filename.innerHTML = item["display_name"]

        child = document.createElement("div")
        child.classList.add("file")
        child.appendChild(img)
        child.appendChild(filename)
        child.dataset.id = item["id"]
        child.dataset.fileType = item["file_type"]
        child.dataset.displayName = item["display_name"]
        child.dataset.url = item["url"]
        child.addEventListener("click", clickHandler)

        grid.appendChild(child)
    })
}

let view = document.getElementById("view_file")

async function clickHandler() {
    res = await getFile(this.dataset.id)
    view.src = res["url"]
}
