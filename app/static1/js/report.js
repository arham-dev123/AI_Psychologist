function convertHTMLtoPDF() {
    const { jsPDF } = window.jspdf;

    let doc = new jsPDF('l', 'mm', [1200, 800]);
    let pdfjs = document.querySelector('#reportPdf');

    doc.html(pdfjs, {
        callback: function(doc) {
            doc.save("report.pdf");
        },
        x: 140,
        y: 60
    });
}

function generateAndSendPDF() {
    const { jsPDF } = window.jspdf;

    let doc = new jsPDF('l', 'mm', [1200, 800]); // Set the document size to A4 landscape
    let pdfjs = document.querySelector('#reportPdf');

    doc.html(pdfjs, {
        callback: function(doc) {
            // Get the PDF bytes as an ArrayBuffer
            var pdfBytes = doc.output('arraybuffer');

            // Get recipient email from input field
            var recipientEmail = document.getElementById('emailInput').value;

            // Create a FormData object with the PDF bytes and recipient email
            var formData = new FormData();
            formData.append('pdfBytes', new Blob([pdfBytes]), 'report.pdf');
            formData.append('recipientEmail', recipientEmail);

            // Send PDF bytes and recipient email to server
            $.ajax({
                type: "POST",
                url: "/report/share_report",
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    alert("PDF sent successfully!");
                },
                error: function(xhr, status, error) {
                    alert("Error sending PDF: " + error);
                }
            });
        },
        x: 140,
        y: 60,
        
    });
}