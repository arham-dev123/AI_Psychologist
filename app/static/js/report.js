function createReportPdf(callback) {
    const reportElement = document.querySelector('#reportPdf');

    html2canvas(reportElement, {
        scale: 1.1,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false
    }).then(function(canvas) {
        const imageData = canvas.toDataURL('image/jpeg', 0.72);
        const pdf = new window.jspdf.jsPDF({
            orientation: 'p',
            unit: 'mm',
            format: 'a4',
            compress: true
        });
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const margin = 10;
        const imageWidth = pageWidth - (margin * 2);
        const imageHeight = (canvas.height * imageWidth) / canvas.width;

        if (imageHeight <= pageHeight - (margin * 2)) {
            pdf.addImage(imageData, 'JPEG', margin, margin, imageWidth, imageHeight, undefined, 'FAST');
        } else {
            let remainingHeight = imageHeight;
            let position = margin;

            pdf.addImage(imageData, 'JPEG', margin, position, imageWidth, imageHeight, undefined, 'FAST');
            remainingHeight -= pageHeight - (margin * 2);

            while (remainingHeight > 0) {
                pdf.addPage();
                position = remainingHeight - imageHeight + margin;
                pdf.addImage(imageData, 'JPEG', margin, position, imageWidth, imageHeight, undefined, 'FAST');
                remainingHeight -= pageHeight - (margin * 2);
            }
        }

        callback(pdf);
    });
}

function convertHTMLtoPDF() {
    createReportPdf(function(pdf) {
        pdf.save('AI-Psychologist-Report.pdf');
    });
}

function generateAndSendPDF() {
    const recipientEmail = document.getElementById('emailInput').value;

    if (!recipientEmail) {
        alert('Please enter an email address first.');
        return;
    }

    createReportPdf(function(pdf) {
        const pdfBytes = pdf.output('arraybuffer');
        const formData = new FormData();

        formData.append('pdfBytes', new Blob([pdfBytes], { type: 'application/pdf' }), 'AI-Psychologist-Report.pdf');
        formData.append('recipientEmail', recipientEmail);

        $.ajax({
            type: 'POST',
            url: '/report/share_report',
            data: formData,
            processData: false,
            contentType: false,
            success: function() {
                alert('PDF sent successfully!');
            },
            error: function(xhr, status, error) {
                alert('Error sending PDF: ' + error);
            }
        });
    });
}
