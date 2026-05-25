const API_URL = "https://ichokes-production.up.railway.app"

const dropZone =
    document.getElementById(
        "dropZone"
    );

const fileInput =
    document.getElementById(
        "fileInput"
    );

const canvas =
    document.getElementById(
        "canvas"
    );

const ctx =
    canvas.getContext("2d");

const loading =
    document.getElementById(
        "loading"
    );

const videoPlayer =
    document.getElementById(
        "videoPlayer"
    );

const downloadContainer =
    document.getElementById(
        "downloadContainer"
    );

dropZone.addEventListener(
    "click",
    () => {
        fileInput.click();
    }
);

dropZone.addEventListener(
    "dragover",
    (e) => {

        e.preventDefault();

        dropZone.classList.add(
            "border-cyan-400"
        );
    }
);

dropZone.addEventListener(
    "dragleave",
    () => {

        dropZone.classList.remove(
            "border-cyan-400"
        );
    }
);

dropZone.addEventListener(
    "drop",
    async (e) => {

        e.preventDefault();

        dropZone.classList.remove(
            "border-cyan-400"
        );

        const file =
            e.dataTransfer.files[0];

        if (!file) return;

        await uploadFile(file);
    }
);

fileInput.addEventListener(
    "change",
    async (e) => {

        const file =
            e.target.files[0];

        if (!file) return;

        await uploadFile(file);
    }
);

async function uploadFile(file) {

    try {

        showLoading();

        clearUI();

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        const isVideo =
            file.type.startsWith(
                "video"
            );

        const endpoint =
            isVideo
            ? "/predict-video"
            : "/predict-image";

        const response =
            await fetch(
                `${API_URL}${endpoint}`,
                {
                    method: "POST",
                    body: formData
                }
            );

        if (!response.ok) {

            throw new Error(
                "Upload failed"
            );
        }

        const data =
            await response.json();

        hideLoading();

        if (isVideo) {

            renderVideo(data);

        } else {

            renderImage(data);
        }

    } catch (error) {

        console.error(error);

        hideLoading();

        alert(
            "Error processing file"
        );
    }
}

function renderImage(data) {

    const img = new Image();

    img.src =
        `${API_URL}${data.output_path}`;

    img.onload = () => {

        canvas.width =
            img.width;

        canvas.height =
            img.height;

        ctx.drawImage(
            img,
            0,
            0
        );

        drawPredictions(
            data.predictions
        );

        createDownloadButton(
            img.src,
            "prediction.jpg"
        );
    };
}

function renderVideo(data) {

    videoPlayer.src =
        `${API_URL}${data.video_url}`;

    videoPlayer.classList.remove(
        "hidden"
    );

    createDownloadButton(
        videoPlayer.src,
        "prediction.mp4"
    );
}

function drawPredictions(
    predictions
) {

    predictions.forEach(pred => {

        const x =
            pred.x - (
                pred.width / 2
            );

        const y =
            pred.y - (
                pred.height / 2
            );

        const width =
            pred.width;

        const height =
            pred.height;

        const confidence =
            (
                pred.confidence * 100
            ).toFixed(1);

        const label =
            `${pred.class} ${confidence}%`;

        ctx.strokeStyle =
            "#22d3ee";

        ctx.lineWidth = 3;

        ctx.strokeRect(
            x,
            y,
            width,
            height
        );

        ctx.fillStyle =
            "#22d3ee";

        ctx.font =
            "bold 18px Arial";

        const textWidth =
            ctx.measureText(
                label
            ).width;

        ctx.fillRect(
            x,
            y - 35,
            textWidth + 20,
            35
        );

        ctx.fillStyle =
            "#000";

        ctx.fillText(
            label,
            x + 10,
            y - 10
        );

        drawCoordinates(
            x,
            y,
            width,
            height
        );
    });
}

function drawCoordinates(
    x,
    y,
    width,
    height
) {

    const coords =
        `x:${Math.round(x)} y:${Math.round(y)}`;

    ctx.fillStyle =
        "#ffffff";

    ctx.font =
        "14px Arial";

    ctx.fillText(
        coords,
        x,
        y + height + 20
    );
}

function createDownloadButton(
    fileUrl,
    filename
) {

    downloadContainer.innerHTML =
        "";

    const button =
        document.createElement(
            "a"
        );

    button.href =
        fileUrl;

    button.download =
        filename;

    button.innerText =
        "⬇ Download Result";

    button.className =
        `
        inline-flex
        items-center
        gap-2
        bg-cyan-500
        hover:bg-cyan-400
        transition
        px-6
        py-4
        rounded-2xl
        text-black
        font-bold
        shadow-xl
        `;

    downloadContainer.appendChild(
        button
    );
}

function clearUI() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    videoPlayer.classList.add(
        "hidden"
    );

    downloadContainer.innerHTML =
        "";
}

function showLoading() {

    loading.classList.remove(
        "hidden"
    );
}

function hideLoading() {

    loading.classList.add(
        "hidden"
    );
}