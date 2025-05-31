document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('file');
    const output = document.getElementById('output');
    const spinner = document.getElementById('spinner');

    form.onsubmit = async function(e) {
        e.preventDefault();
        if (!fileInput.files.length) return;
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        output.style.display = 'none';
        output.innerHTML = '';
        spinner.style.display = 'block';
        try {
            const res = await fetch('/classify-file/', { method: 'POST', body: formData });
            const data = await res.json();
            spinner.style.display = 'none';
            if (res.ok) {
                output.innerHTML = `<b>Format:</b> ${data.format}<br><b>Intent:</b> ${data.intent}<br><b>Extracted:</b><pre>${JSON.stringify(data.extracted, null, 2)}</pre>`;
            } else {
                output.innerHTML = `<span class='error'>Error: ${data.detail || 'Unknown error'}</span>`;
            }
        } catch (err) {
            spinner.style.display = 'none';
            output.innerHTML = `<span class='error'>Error: ${err}</span>`;
        }
        output.style.display = 'block';
    };
});
